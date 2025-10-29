from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class NewsHelperAgent:
    @agent
    def news_hunter_agent(self):
        return Agent(config=self.agents_config["news_hunter_agent"])

    @task
    def content_harvesting_task(self):
        return Task(config=self.tasks_config["content_harvesting_task"])

    @agent
    def summarizer_agent(self):
        return Agent(config=self.agents_config["summarizer_agent"])

    @task
    def summarization_task(self):
        return Task(config=self.tasks_config["summarization_task"])

    @agent
    def curator_agent(self):
        return Agent(config=self.agents_config["curator_agent"])

    @task
    def final_report_assembly_task(self):
        return Task(config=self.tasks_config["final_report_assembly_task"])

    @crew
    def crew(self):
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)
