from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv

from tools import news_search_tool, scrape_tool

load_dotenv()


@CrewBase
class NewsHelperAgent:
    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config["news_hunter_agent"],
            tools=[news_search_tool, scrape_tool],
        )

    @agent
    def summarizer_agent(self):
        return Agent(config=self.agents_config["summarizer_agent"], tools=[scrape_tool])

    @agent
    def curator_agent(self):
        return Agent(config=self.agents_config["curator_agent"])

    @task
    def content_harvesting_task(self):
        return Task(config=self.tasks_config["content_harvesting_task"])

    @task
    def summarization_task(self):
        return Task(config=self.tasks_config["summarization_task"])

    @task
    def final_report_assembly_task(self):
        return Task(config=self.tasks_config["final_report_assembly_task"])

    @crew
    def crew(self):
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)


result = (
    NewsHelperAgent()
    .crew()
    .kickoff(inputs={"topic": "the war between Ukraine and Russia"})
)

# print("👇" * 50)
# print(result)
# print("👇" * 50)


for task_output in result.tasks_output:
    print(task_output)
