from fastapi import FastAPI
from pydantic import BaseModel
from roi_calculator import calculate_npv_and_score, get_salary_live, get_salary_glassdoor, get_salary_linkedin
from fastapi.middleware.cors import CORSMiddleware

from scrapers.indeed_scraper import get_salary_live
from scrapers.glassdoor_scraper import get_salary_glassdoor
from scrapers.linkedin_scraper import get_salary_linkedin

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class ROIRequest(BaseModel):
    college: str
    major: str
    tuition: float
    aid: float

# Helper: clean salary fetcher
def get_salary(search_term):
    # Try Indeed
    salary_indeed = get_salary_live(search_term)
    if salary_indeed:
        return salary_indeed

    # Try Glassdoor
    salary_glassdoor = get_salary_glassdoor(search_term)
    if salary_glassdoor:
        return salary_glassdoor

    # Try LinkedIn
    salary_linkedin = get_salary_linkedin(search_term)
    if salary_linkedin:
        return salary_linkedin

    # Fallback
    return 50000  # some default median salary

# Route
@app.post("/calculate-roi")
def calculate_roi(request: ROIRequest):
    search_term = f"{request.major} at {request.college}"
    salary = get_salary(search_term)

    # Calculate NPV + score + earnings over time
    npv, score, discounted = calculate_npv_and_score(salary, request.tuition, request.aid)

    return {
        "npv": npv,
        "score": score,
        "earnings_over_time": discounted.tolist()
    }
