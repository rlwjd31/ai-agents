from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

MAX_ARTICLES = 3
news_search_tool = SerperDevTool(country="kr", n_results=MAX_ARTICLES)

