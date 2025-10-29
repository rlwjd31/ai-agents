import time

from crewai.tools import tool
from crewai_tools import SerperDevTool
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# beautifulsoup은 html을 다루고 조작하는 library
load_dotenv()

MAX_ARTICLES = 3
news_search_tool = SerperDevTool(country="kr", n_results=MAX_ARTICLES)


@tool
def scrape_tool(url: str) -> str:
    """
    Use this when you need to read the content of a website.
    Returns the content of a website, in case the website is not available, it returns 'No content'.
    Input should be a `url` string. for example (https://www.reuters.com/world/asia-pacific/cambodia-thailand-begin-talks-malaysia-amid-fragile-ceasefire-2025-08-04/)
    """
    print(f"Scrapping URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        time.sleep(5)
        html = page.content()
        browser.close()

        soup = BeautifulSoup(html, "html.parser")

        unwanted_tags = [
            "header",
            "footer",
            "nav",
            "aside",
            "script",
            "style",
            "noscript",
            # "iframe", # naver blog에서는 body > iframe으로 iframe을 제거
            "form",
            "button",
            "input",
            "select",
            "textarea",
            "img",
            "svg",
            "canvas",
            "audio",
            "video",
            "embed",
            "object",
        ]

        for tag in soup.find_all(unwanted_tags):
            tag.decompose()

        content = soup.get_text(separator=" ")

        return content if content != "" else "No content"

# url = (
#     "https://www.chosun.com/english/national-en/2025/10/28/ECPWADRPTBCOTKXLSIE3OCHWME/"
# )
# print(scrape_tool(url))


