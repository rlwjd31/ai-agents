from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from crewai.project import CrewBase, crew, agent, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

from models import ChosenJob, JobLIst, RankedJobList
from tools import web_search_tool


load_dotenv()

# knowledge directory를 설정해주어야 알아서 읽어들임
resume_knowledge_for_match = TextFileKnowledgeSource(
    file_paths=["resume.txt"],
    collection_name="resume_for_match",
)

resume_knowledge_for_optimization = TextFileKnowledgeSource(
    file_paths=["resume.txt"],
    collection_name="resume_for_optimization",
)

resume_knowledge_for_research = TextFileKnowledgeSource(
    file_paths=["resume.txt"],
    collection_name="resume_for_research",
)

resume_knowledge_for_interview = TextFileKnowledgeSource(
    file_paths=["resume.txt"],
    collection_name="resume_for_interview",
)


@CrewBase
class JobHunterCrew:
    @agent
    def job_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["job_search_agent"], tools=[web_search_tool]
        )

    @agent
    def job_matching_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["job_matching_agent"],
            knowledge_sources=[resume_knowledge_for_match],
        )

    @agent
    def resume_optimization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_optimization_agent"],
            knowledge_sources=[resume_knowledge_for_optimization],
        )

    @agent
    def company_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["company_research_agent"],
            knowledge_sources=[resume_knowledge_for_research],
            tools=[web_search_tool],
        )

    @agent
    def interview_prep_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["interview_prep_agent"],
            knowledge_sources=[resume_knowledge_for_interview],
        )

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


input_variables = {
    "level": "신입",
    "position": "프론트엔드 개발자",
    "location": "대한민국",
}

results = JobHunterCrew().crew().kickoff(inputs=input_variables)

for task_output in results.tasks_output:
    print(task_output.pydantic)
