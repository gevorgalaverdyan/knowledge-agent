from datetime import date

from schemas.chat import CalculationToolResult

TFSA_LIMITS = {
    2009: 5000,
    2010: 5000,
    2011: 5000,
    2012: 5000,
    2013: 5500,
    2014: 5500,
    2015: 10000,
    2016: 5500,
    2017: 5500,
    2018: 5500,
    2019: 6000,
    2020: 6000,
    2021: 6000,
    2022: 6000,
    2023: 6500,
    2024: 7000,
    2025: 7000
}

"""
Tool: TFSA contribution room Calculator
"""
def calculate_tfsa_contribution_room(
    year_turned_18: int,
) -> CalculationToolResult:
    current_year = date.today().year

    if year_turned_18 > current_year:
        raise ValueError("year_turned_18 cannot be in the future")
     
    total = 0
    yearly_breakdown={}

    for year in range(year_turned_18, current_year+1):
        amount = TFSA_LIMITS[year]
        total += amount
        yearly_breakdown[year] = amount
    
    return CalculationToolResult(
        total_contribution_room=total, 
        yearly_breakdown=yearly_breakdown, 
        assumptions=[
            "Canadian resident for all eligible years",
            "No prior TFSA contributions",
            "No withdrawals",
            "CRA annual limits used"
        ])