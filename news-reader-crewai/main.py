from dotenv import load_dotenv
from crewai import Crew, Agent, Task, agent
from crewai.project import CrewBase, agent, crew, task

from tools import count_letters

load_dotenv()


@CrewBase
class TranslatorCrew:
    @agent
    def translator_agent(self):
        return Agent(config=self.agents_config["translator_agent"])

    @task
    def translate_task(self):
        return Task(config=self.tasks_config["translate_task"])

    @task
    def retranslate_task(self):
        return Task(config=self.tasks_config["retranslate_task"])

    @agent
    def counter_agent(self):
        return Agent(config=self.agents_config["counter_agent"], tools=[count_letters])

    @task
    def count_task(self):
        return Task(config=self.tasks_config["count_task"])

    @crew
    def assemble_crew(self):
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)


TranslatorCrew().assemble_crew().kickoff(
    inputs={
        "sentence": "I'm gijung I like walking when my surroundings are hard and I will be rich someday"
    }
)
