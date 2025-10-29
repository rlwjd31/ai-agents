# News Reader Agent

- new_hunter_agent: 수석 뉴스 정보 분석가
- content harvesting task:
  - `using search tool`이란 문장을 작성하여 tool calling을 유도함.
  - “Only select actual article pages”: search tool을 사용하기 때문에 가끔 CNN이나 뉴욕타임스 같은데로 들어간다. 즉, 뉴스들을 모아놓은 뉴스 list page로 들어가기 때문에 실제로 기사에 대한 내용이 들어있은 detail page로 들어가게하기위한 문구이다. 즉, `실제 뉴스 기사 전체 내용`을 얻기 위함이다.
  - `URLs containing "/tag/", "/topic/", "/hub/", "/section/ & ❌ Reject the following types of URLs:)`: 실제 뉴스 기사가 아닌 뉴스 리스트를 보여줄 수 있는 path를 제거하여 `실제 뉴스 기사 내용`을 얻기 위함. 그리고 한 번더 명확히 하기 위해 걸러야 하는 url을 예시로 첨부함.
  - `For each **accepted** article URL & Use the scrape tool`: filtering을 통해 걸러진 URL에 대해서 이제 `scrape tool`을 사용하라고 유도
  - `Apply intelligent filtering to remove:` : 지금까지 필터링을 했지만 `scrape tool`을 이용하여 가져온 정보에 대해서 `최신 뉴스, 너무 작은 내용의 기사, scrape이 실패한 기사`를 기준으로 필터링을 진행한다.
  - `Classify each article into appropriate topic categories`: 관련 기사들을 카테고리별로 분류하는 작업
  - `credibility scores`: 기사에 대한 신뢰도 점수를 매겨서 신뢰성 있는 기사를 가져오기 위함.
  - `relevance scores`: 기사에 대해 관련성 점수를 매겨서 관련성 있는 기사만 가져오기 위함.

# Tool 작업

현재 `search_tool`과 `scrape_tool` 두 개가 필요한 상황인데 이는 crewai에서 제공을 해준다.

- search_tool: `google serper search`를 통해서 생성
  refer ⇒ https://docs.crewai.com/en/tools/search-research/serperdevtool
- scrape_tool: html 컨텐트를 다룰 수 있는 `beautifulsoup`와 headless로 페이지를 조작할 수 있는 `playwright`를 이용하여 구현

```python
# tools.py > news_search_tool
from crewai_tools import SerperDevTool

news_search_tool = SerperDevTool(country="kr", n_results=10)

```

```python
# tools.py > scrape_tool
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from crewai.tools import tool

# custom tool이므로 파라미터 type과 docstring을 잘 작성해야 한다.
@tool
def scrape_tool(url: str) -> str:
  """
  Use this when you need to read the content of a website.
  Returns the content of a website, in case the website is not available, it returns 'No content'.
  Input should be a `url` string. for example (https://www.reuters.com/world/asia-pacific/cambodia-thailand-begin-talks-malaysia-amid-fragile-ceasefire-2025-08-04/)
	"""
	with sync_playwrigth as p:
  browser = p.chromium.launch(headless=True)
  page = browser.new_page()
  page.goto(url)
  time.sleep(5)
  html = page.content()
  browser.close()

  soup = BeautifulSoup(html, "html.parser")

  unwanted_tags = [ ... ] # 👉🏻 필요없는 Tag를 html에서 지워주기 위함

  for tag in soup.find_all(unwanted_tags):
          tag.decompose() # 👉🏻 관련 tag와 children 제거

  content = soup.get_text(separator=" ")

  return content if content != "" else "No content"


```

이제 관련된 `agents.yaml`에서 tool을 사용하라고 한 맥락이 있는 agent들과 연결을 하면 된다.

# 각 Task의 output 살펴보기

아래와 같이 모든 동작이 끝난후 살펴보아도 된다.

```python
result = SomeCrew().crew().kickoff(...)

for task_output in result.tasks_output:
  print(task_output)
```

하지만, 이는 가독성이 좋지 않아 그냥 각 task에 `output_file, create_directory` 속성을 주어 해결할 수 있다.

그냥 `Task에 넣는 방식`과 `tasks.yaml`에 작성하는 방법이 있다.

```python
@task
def task1(self):
  return Task(
    description="...",
    expected_output="...",
    markdown=True,
    output_file="output/task1_output.md",
    create_directory=True
  )
```

```yaml
content_harvesting_task:
  description: >
    ...

  expected_output: >
    ...
  markdown: true
  output_file: output/content_harvest.md # 👉🏻 추가
  create_directory: true # 👉🏻 추가
```

이렇게 생성된 output을 통해서 가독성 있고 쉽게 살펴볼 수 있다.

# New Reader Agent를 만들면서...

흠...... 코딩은 거의 없이 ai agent를 만들수 있는 것이 CrewAI의 장점같다.  
하지만, 거의 prompt 작업이 작업 시간의 90%가 걸렸으며 작동자체는 크게 문제가 없었다.  
대신 뭔가 customizing하는데는 langgraph에 비해 훨씬 어렵다는 생각이 들었다.  
복잡한 로직을 담당하는 agent가 아니고 뭔가 디테일하게 신경쓸 일이 없다면 crewai는 좋은 선택이 될 수 있다.  
그리고 점점 느끼는건데 AI를 공부함에 따라 점점 지갑이 사라지는 느낌이다...🥹🥹🥹
