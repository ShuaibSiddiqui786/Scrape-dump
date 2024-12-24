import scrapy
from pymongo import MongoClient
import datetime
import logging

# MongoDB connection
client = MongoClient("mongodb+srv://shuaibsiddiqui:ydnXoIUKxCOwqJYl@cluster0.edsz1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/")
db = client.youtube  # Database name

class YouTubeSpider(scrapy.Spider):
    name = "youtube"
    allowed_domains = ["youtube.com"]

    def __init__(self, prompt=None, *args, **kwargs):
        super(YouTubeSpider, self).__init__(*args, **kwargs)
        if not prompt:
            raise ValueError("Prompt is required to perform a YouTube search.")
        self.prompt = prompt  # Accept prompt from external input

    def start_requests(self):
        # Construct the search URL dynamically based on the prompt
        search_url = f"https://www.youtube.com/results?search_query={self.prompt}"
        yield scrapy.Request(url=search_url, callback=self.parse)

    def insertToDb(self, title, link, views, upload_date):
        collection = db['videos']
        doc = {
            "title": title,
            "link": link,
            "views": views,
            "upload_date": upload_date,
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
        }
        try:
            inserted = collection.insert_one(doc)
            return inserted.inserted_id
        except Exception as e:
            self.log(f"Error inserting to MongoDB: {e}", level=logging.ERROR)

    def parse(self, response):
        # Extract video cards
        video_cards = response.css('ytd-video-renderer')

        if not video_cards:
            self.log("No video cards found. Ensure YouTube's DOM structure is correct.", level=logging.WARNING)

        for card in video_cards:
            title = card.css('#video-title::attr(title)').get()
            link = card.css('#video-title::attr(href)').get()
            if link:
                # Ensure link does not point to disallowed paths
                if any(disallowed in link for disallowed in [
                    "/api/", "/comment", "/feeds/videos.xml", "/get_video", 
                    "/get_video_info", "/get_midroll_info", "/live_chat", 
                    "/login", "/qr", "/results", "/signup", "/t/terms", 
                    "/timedtext_video", "/verify_age", "/watch_ajax", 
                    "/watch_fragments_ajax", "/watch_popup", 
                    "/watch_queue_ajax", "/youtubei/"
                ]):
                    self.log(f"Skipping disallowed link: {link}", level=logging.INFO)
                    continue
                link = response.urljoin(link)

            views = card.css('#metadata-line span::text').get()
            upload_date = card.css('#metadata-line span:nth-child(2)::text').get()

            # Insert into MongoDB
            self.insertToDb(
                title.strip() if title else 'No Title',
                link,
                views.strip() if views else 'No Views',
                upload_date.strip() if upload_date else 'No Upload Date'
            )

        # Follow pagination
        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page:
            # Ensure next page does not lead to disallowed paths
            if not any(disallowed in next_page for disallowed in [
                "/api/", "/comment", "/feeds/videos.xml", "/get_video", 
                "/get_video_info", "/get_midroll_info", "/live_chat", 
                "/login", "/qr", "/results", "/signup", "/t/terms", 
                "/timedtext_video", "/verify_age", "/watch_ajax", 
                "/watch_fragments_ajax", "/watch_popup", 
                "/watch_queue_ajax", "/youtubei/"
            ]):
                self.log("Following pagination to next page.", level=logging.INFO)
                yield response.follow(next_page, callback=self.parse)
            else:
                self.log(f"Skipping disallowed next page: {next_page}", level=logging.INFO)
