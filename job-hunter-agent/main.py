from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from crewai.project import CrewBase, crew, agent, task

from models import ChosenJob, JobLIst, RankedJobList
from tools import web_job_search_tool


load_dotenv()


@CrewBase
class JobHunterCrew:
    @agent
    def job_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["job_search_agent"], tools=[web_job_search_tool]
        )

    @agent
    def job_matching_agent(self) -> Agent:
        return Agent(config=self.agents_config["job_matching_agent"])

    @agent
    def resume_optimization_agent(self) -> Agent:
        return Agent(config=self.agents_config["resume_optimization_agent"])

    @agent
    def company_research_agent(self) -> Agent:
        return Agent(config=self.agents_config["company_research_agent"])

    @agent
    def interview_prep_agent(self) -> Agent:
        return Agent(config=self.agents_config["interview_prep_agent"])

    @task
    def job_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_extraction_task"], output_pydantic=JobLIst
        )

    @task
    def job_matching_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_matching_task"], output_pydantic=RankedJobList
        )

    @task
    def job_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_selection_task"], output_pydantic=ChosenJob
        )

    @task
    def resume_rewriting_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_rewriting_task"],
            # 이전 task가 job selection task라서 넣어주지 않아도 자동으로 들어가지만
            # 명확하게 흐름을 알고 싶어 넣어줌.
            context=[self.job_selection_task()],
        )

    @task
    def company_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["company_research_task"],
            context=[self.job_selection_task()],
        )

    @task
    def interview_prep_task(self) -> Task:
        return Task(
            config=self.tasks_config["interview_prep_task"],
            context=[
                self.job_selection_task(),
                self.resume_rewriting_task(),
                self.company_research_task(),
            ],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)


JobHunterCrew().crew().kickoff()
