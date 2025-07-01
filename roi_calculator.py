import pandas as pd
import numpy as np

# Import your Indeed scraper
from scrapers.indeed_scraper import get_salary_live

# If you have Glassdoor and LinkedIn scrapers, import them here
# from scrapers.glassdoor_scraper import get_salary_glassdoor
# from scrapers.linkedin_scraper import get_salary_linkedin

# Load fallback data (BLS wages)
bls_df = pd.read_csv("bls_wages.csv")


def predict_lifetime_earnings(entry_salary, annual_growth=0.03, years=40):
    """
    Calculate projected earnings over time with annual growth.
    """
    return np.array([
        entry_salary * (1 + annual_growth) ** y
        for y in range(years)
    ])


def discount_cashflows(earnings, rate=0.03):
    """
    Discount future earnings to present value.
    """
    return earnings / ((1 + rate) ** np.arange(1, len(earnings) + 1))


def calculate_npv(earnings, cost):
    """
    Net present value = sum of discounted earnings - cost.
    """
    return earnings.sum() - cost


def calculate_score(npv, debt_ratio=0.3, job_stability=0.9):
    """
    Calculate a 0-100 "Worth It Score".
    """
    percentile = min(max(npv / 1_000_000, 0), 1)
    return (
        0.7 * (percentile * 100) +
        0.15 * (1 - debt_ratio) * 100 +
        0.15 * job_stability * 100
    )


def calculate_npv_and_score(entry_salary, tuition, aid):
    """
    Main helper function to:
    - predict earnings
    - discount them
    - calculate NPV
    - calculate score
    """
    earnings = predict_lifetime_earnings(entry_salary)
    discounted = discount_cashflows(earnings)
    cost = tuition - aid
    npv = calculate_npv(discounted, cost)
    score = calculate_score(npv)
    return npv, score, discounted
