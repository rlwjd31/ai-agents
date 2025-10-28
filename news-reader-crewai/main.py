# crewai의 main concepy
"""
1. Crew: 일련의 작업을 달성하기 위해 함께 협력하는 `에이전트들의 그룹`을 나타내며 각 crew는 `작업 실행`, `에이전트 간 협업`, `전체 워크플로우`에 대한 전략을 정의함.
2. Agent: 아래와 같은 역할을 수행하는 독립적인 역할을 수행한다.
  - 특정 작업 수행
  - 자신의 역할과 목표에 기반한 의사결정
  - Tool을 활용하여 목표 달성
  - 다른 에이전트와의 소통 및 협업
  - 상호작용에 대한 기억 유지
  - 허용될 경우 작업 위임
3. Task: 작업을 관리하고 생성하는 방법에 대한 안내서 -> "agent한테 ~ 좀 해줘"
         즉, `Agent가 완료하는 구체적인 과제`이다.
"""


from dotenv import load_dotenv

load_dotenv()

from crewai import Crew, Agent, Task

