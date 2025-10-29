# CrewAI basic(Crew, Agent, Task)
crewai에서 agent, task에 넣어주는 goal, role, backstory, description, expected_output은 어쩌고 보면 prompt에 속하면 일종의 페르소나와 같다고 생각하면 된다.
CrewAI에서는 3가지 중요한 개념이 존재한다.

- `Crew`
- `Agent`
- `Task`

## Agent 생성

Agent는 아래와 같은 역할을 수행하는 `독립적인 역할을 수행`하는 주체이다.

- 특정 작업 수행
- 자신의 역할과 목표에 기반한 의사결정
- Tool을 활용하여 목표 달성
- 다른 에이전트와의 소통 및 협업
- 상호작용에 대한 기억 유지
- 허용될 경우 작업 위임

crew는 `CrewBase`데코레이터를 통해서 정의해주어야 한다.  
`@agent` decorator와 Agent class를 return하여 정의할 수 있다.

```python
# main.py
from crewai import Crew, agent
from crewai.project import CrewBase

@CrewBase
class TranslatorCrew:

  @agent
  def translator_agent(self):
    return Agent(
      goal="To be a good and useful translator to avoid misunderstandings.",
      role="Translator to translate from English to Italian",
      backstory="You grew up between New York and Palermo, you can speak two languages fluently, and you can detect the cultural differences.",
    )

```

위와 같이 inline으로 하드코딩하는 것보단 yaml로 따로 빼서 정의할 수 있는 것이 깔끔하다.

```yaml
# config/agents.yaml
translator_agent:
  role: >
    Translator to translate from English to Italian
  goal: >
    To be a good and useful translator to avoid misunderstandings.
  backstory: >
    You grew up between New York and Palermo, you can speak two languages fluently, and you can detect the cultural differences.
```

이 때 파일명은 `crewawi`에서 정해진 naming 규칙을 따라야 한다.  
config에 인자를 넣어주면 Crewai에 의해 자동으로 config하위에 있는 agents.yaml에 접근하여 설정들을 넣어준다.

```python
# main.py
from dotenv import load_dotenv
from crewai import Agent
from crewai.project import CrewBase, agent

load_dotenv()

@CrewBase
class TranslatorCrew:
    @agent
    def translator_agent(self):
        return Agent(config=self.agents_config["translator_agent"])
```

## Task 생성

Task는 작업을 관리하고 생성하는 방법에 대한 `안내서`로 agent가 완료해야하는 `구체적인 과제` 이다.  
task에 대한 yaml도 `tasks.yaml`로 정의되어 있으며 이는 `self.tasks_config`를 통해서 가져올 수 있다.  
tasks.yaml에 작성한 작업 내용은 `translator_agent`가 수행한다. 즉, translator_agent에게 수행해야할 작업을 알려주는 명세서와 같다.  

```yaml
# config/tasks.yaml
translate_task:
  description: >
    Translate {sentence} from English to Italian without making mistakes.
  expected_output: >
    A well formatted translation from English to Italian using proper capitalization of names and places.
  agent: translator_agent

```

```python
from dotenv import load_dotenv
from crewai import Agent, Task, agent
from crewai.project import CrewBase, agent, task

@CrewBase
class TranslatorCrew:
    @agent
    def translator_agent(self):
        return Agent(config=self.agents_config["translator_agent"])
    
    @task
    def translate_task(self):
		    return Task(config=self.tasks_config["translate_task"])
		
```

## Crew 생성

Crew는 일련의 작업을 달성하기 위해 함께 협력하는 `에이전트들의 그룹`을 나타내며 각 crew는 `작업 실행`, `에이전트 간 협업`, `전체 워크플로우`에 대한 전략을 정의한다.  
agent, task를 생성하는 것과 같다. 하지만 crew는 agent들의 묶음으로 agent들과 agent이 수행해야하는 task를 넣어주면 된다.  
@agent, @task decorator를 통해 self.agents, self.tasks에 담기므로 이를 crew 클래스의 인자로 넘겨주어 crew를 만들 수 있다.  

```python
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, agent
from crewai.project import CrewBase, agent, crew, task

load_dotenv()

@CrewBase
class TranslatorCrew:
    @agent
    def translator_agent(self):
        return Agent(config=self.agents_config["translator_agent"])

    @task
    def translate_task(self):
      return Task(
        config=self.tasks_config["translate_task"]
      )
    
    @crew
    def assemble_crew(self):
      return Crew(
        agents=self.agents,
        tasks=self.tasks,
        verbose=True
      )
```

## Agent 실행

Crewai에서 crew를 실행하여 선언한 agent, task들을 수행할 수 있다. 이 때 `kickoff`를 통해서 시작할 수 있다.  
여기서 `sentence`에는 tasks.yaml에 작성한 `{sentence}` 에 값을 넣어준다.  

```python
TranslatorCrew().assemble_crew().kickoff(
    inputs={
        "sentence": "I'm gijung I like walking when my surroundings are hard and I will be rich someday"
    }
)
```

이제 `uv run main.py`를 통해서 Agent들이 어떻게 작업하는지 볼 수 있다.  

### 다른 task할당해 보기

재 번역을 수행하는 task를 동일한 agent에게 수행시켜보자. 따라서 yaml file의 agent에는 동일하게 작성하고 `description, expected_output`은 다르게 작성하자.

```yaml
retranslate_task:
  description: >
    Translate "{sentence}" from Italian to Greek without making mistakes.
  expected_output: >
    A well formatted translation from Italian to Greek using proper capitalization of names and places.
  agent: translator_agent
```

```python
@CrewBase
class TranslatorCrew:
  ... //
  
  @task
  def translate_task(): ...
  
  @task
  def retranslate_task(self):
    return Task(
      config=self.tasks_config["retranslate_task"]
    )
  ... //
```

## Tool

Tool은 말 그대로 AI Agent가 쓰는 도구라고 생각하면 된다.   

Tool은 AI Agent가 할 수 없는 것을 하게 만들어준다. 예를 들어 AI Agent는 질의에 대한 답변을 수행할 수는 있지만, `날씨 조회`, `DB검색`등 코드 실행과 같은 것은 AI Agent가 할 수 없고 개발자가 직접 코딩을 통해 해결할 수 있다. 따라서 이러한 기능들을 코드로 만들고 필요한 순간에 Ai Agent가 호출하여 tool에 대한 결과를 context에 넣어 답변의 정확도와 신뢰성을 높일 수 있다.  

위의 예제에서 `sentence`라는 input_variables를 이용하여 해당 문장의 길이를 구하는 `tool function`을 만들어보자.   

이 때 아래의 주의사항이 있다.  

- 함수의 `파라미터명`, `type`을 명확히 작성해야 한다.
- docstring에 함수에 대한 설명을 작성해야 한다.

함수에 대한 명세서를 이렇게 작성해야 하는 이유는 CrewAI가 이를 보고 함수에 대해 올바른 schema를 작성할 수 있기 때문이다.  

```python
from crewai.tools import tool

# tools.py
# docstring과 인자의 이름, type을 제대로 작성해야 CrewAI가 함수에 대한 schema를 정확히 생성할 수 있다.
@tool
def count_letters(sentence: str) -> int:
    """
    This function is to count the amount of letters in a sentence.
    The input is a 'sentence' string.
    The output is a number
    """

    return len(sentence)

```

### Counter Agent & Task 생성

tool function을 처리하기 위한 `counter_agent`를 페르소나와 함께 생성해보자.

```yaml
# agents.yaml
counter_agent:
  role: >
    To count the length of things.
  goal: >
    To be a good counter that never lies or makes things up.
  backstory: >
    You are a genius counter.
```

```yaml
# tasks.yaml
count_task:
  description: >
    Count the amount of letters in a sentence.
  expected_output: >
    The number of letters in a sentence.
  agent: counter_agent
```

```python
# main.py
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, agent
from crewai.project import CrewBase, agent, crew, task
from tools import count_letters

load_dotenv()

@CrewBase
class TranslatorCrew:
    ...

    @agent
    def counter_agent(self):
        return Agent(
          config=self.agents_config["counter_agent"],
          tools=[count_letters]
        )

    @task
    def count_task(self):
        return Task(config=self.tasks_config["count_task"])

    ...

TranslatorCrew().assemble_crew().kickoff(
    inputs={
        "sentence": "I'm gijung I like walking when my surroundings are hard and I will be rich someday"
    }
)

```


## Task workflow
crewai에서 task의 output을 다른 task의 input으로 넣어주는지 궁금했는데. 그냥 task의 선언 순서에 따라 input과 output이 흐른다.  

- task1의 output
- task2의 input = task1의 output

> 💡 따라서 task의 순서를 잘 배치하여 원하는 task의 input으로 넣어주면 된다.  
> 이에 따라 content_harvesting_task의 output은 summarization_task의 input으로 들어가게 되므로 `description: Take each of the URLs from the previous task and generate a summary for each articles`라는 문장을 작성할 수 있다. `previous tasks`는 `content_harvest_task`의 output을 의미하며 llm이 알아먹는다.
> 

```python
@CrewBase
class SomeAgent:
  @agent
  def agent1(self):
    ...
    
  @agent
	def agent2(self):
	  ...
	  
	@task
	def task1(self):
	  ...
	  
	@task
	def task2(self):
	  ...
```