# Scrapy settings for your project
BOT_NAME = 'youtube'

SPIDER_MODULES = ['Youtube.spiders']
NEWSPIDER_MODULE = 'Youtube.spiders'

# Bypass robots.txt
ROBOTSTXT_OBEY = False

# User-Agent rotation
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy_proxies.RandomProxy': 100,
}

# Proxies
PROXY_LIST = 'C:\\Users\\DELL\\Downloads\\helena\\helena\\Youtube\\Youtube\\proxy_list.txt'  # Replace with the actual path to your proxy list file
PROXY_MODE = 0  # Randomly select a proxy from the list

# Request headers
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://www.youtube.com',
}

# Download delay
DOWNLOAD_DELAY = 3
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Selenium for JavaScript rendering
from shutil import which
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS = ['--headless']  # Run Chrome in headless mode

DOWNLOADER_MIDDLEWARES.update({
    'scrapy_selenium.SeleniumMiddleware': 800,
})

# Enable HTTP cache (optional for debugging)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
