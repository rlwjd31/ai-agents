from typing import List
from pydantic import BaseModel
from datetime import date


class Job(BaseModel):
    job_title: str # 공고 제목
    company_name: str # 회사 이름
    job_location: str # 회사 위치
    is_remote_friendly: bool | None = None # 원격 근무 가능 여부
    employment_type: str | None = None # 고용 형태
    compensation: str | None = None # 연봉
    job_posting_url: str # 공고 링크
    job_summary: str # 공고 요약

    key_qualifications: List[str] | None = None # 주요 자격 요건
    job_responsibilities: List[str] | None = None # 담당 업부
    date_listed: date | None = None # 공고 게시일
    required_technologies: List[str] | None = None # 요구 기술 스택 
    core_keywords: List[str] | None = None # 핵심 키워드

    role_seniority_level: str | None = None # 경력 수준
    years_of_experience_required: str | None = None # 요구되는 경력 기간
    minimum_education: str | None = None # 최소 학력
    job_benefits: List[str] | None = None # 직무 혜택
    includes_equity: bool | None = None # 주식 포함 여부
    offers_visa_sponsorship: bool | None = None # 비자 스폰서 제공 여부
    hiring_company_size: str | None = None # 회사 규모
    hiring_industry: str | None = None # 회사 업종
    source_listing_url: str | None = None # 이 공고를 처음 발견한 곳의 링크(출처). e.g. 원티드, 잡코리아
    full_raw_job_description: str | None = None # 전체 원본 공고글


class JobLIst(BaseModel):
    jobs: List[Job]

class RankedJob(BaseModel):
  job: Job
  match_score: int
  reason: str

class RankedJobList(BaseModel):
  ranked_jobs: List[RankedJob]

class ChosenJob(BaseModel):
  job: Job
  selected: bool
  reason: str
