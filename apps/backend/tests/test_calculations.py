"""
Unit tests for TFSA calculation tools in tools/calculations.py
"""
import pytest
from datetime import date
from tools.calculations import calculate_tfsa_contribution_room, TFSA_LIMITS


class TestCalculateTFSAContributionRoom:
    """Tests for calculate_tfsa_contribution_room function"""
    
    def test_calculate_single_year(self):
        """Test calculation for someone who turned 18 this year"""
        current_year = date.today().year
        result = calculate_tfsa_contribution_room(current_year)
        
        assert result.total_contribution_room == TFSA_LIMITS[current_year]
        assert len(result.yearly_breakdown) == 1
        assert result.yearly_breakdown[current_year] == TFSA_LIMITS[current_year]
        assert len(result.assumptions) > 0
    
    def test_calculate_multiple_years(self):
        """Test calculation for someone who turned 18 in 2010"""
        result = calculate_tfsa_contribution_room(2010)
        current_year = date.today().year
        
        # Calculate expected total
        expected_total = sum(TFSA_LIMITS[year] for year in range(2010, current_year + 1))
        
        assert result.total_contribution_room == expected_total
        assert len(result.yearly_breakdown) == current_year - 2010 + 1
        
        # Verify each year's contribution is correct
        for year in range(2010, current_year + 1):
            assert result.yearly_breakdown[year] == TFSA_LIMITS[year]
    
    def test_calculate_from_2009(self):
        """Test calculation from the first TFSA year (2009)"""
        result = calculate_tfsa_contribution_room(2009)
        current_year = date.today().year
        
        # Calculate expected total from 2009 to current year
        expected_total = sum(TFSA_LIMITS[year] for year in range(2009, current_year + 1))
        
        assert result.total_contribution_room == expected_total
        assert result.yearly_breakdown[2009] == 5000
    
    def test_calculate_includes_assumptions(self):
        """Test that calculation includes all required assumptions"""
        result = calculate_tfsa_contribution_room(2015)
        
        assert len(result.assumptions) == 4
        assert "Canadian resident" in result.assumptions[0]
        assert "No prior TFSA contributions" in result.assumptions[1]
        assert "No withdrawals" in result.assumptions[2]
        assert "CRA annual limits" in result.assumptions[3]
    
    def test_calculate_future_year_raises_error(self):
        """Test that future year raises ValueError"""
        current_year = date.today().year
        future_year = current_year + 1
        
        with pytest.raises(ValueError, match="year_turned_18 cannot be in the future"):
            calculate_tfsa_contribution_room(future_year)
    
    def test_calculate_year_2015_includes_10000_limit(self):
        """Test that 2015's special $10,000 limit is included"""
        result = calculate_tfsa_contribution_room(2015)
        
        assert result.yearly_breakdown[2015] == 10000
    
    def test_calculate_total_matches_sum_of_breakdown(self):
        """Test that total equals sum of yearly breakdown"""
        result = calculate_tfsa_contribution_room(2012)
        
        calculated_sum = sum(result.yearly_breakdown.values())
        assert result.total_contribution_room == calculated_sum
    
    def test_calculate_recent_years_2020_2025(self):
        """Test calculation for someone who turned 18 in 2020"""
        result = calculate_tfsa_contribution_room(2020)
        current_year = date.today().year
        
        # Verify recent year limits are correct
        assert result.yearly_breakdown[2020] == 6000
        assert result.yearly_breakdown[2021] == 6000
        assert result.yearly_breakdown[2022] == 6000
        assert result.yearly_breakdown[2023] == 6500
        assert result.yearly_breakdown[2024] == 7000
        if current_year >= 2025:
            assert result.yearly_breakdown[2025] == 7000


class TestTFSALimits:
    """Tests to verify TFSA_LIMITS dictionary is correct"""
    
    def test_limits_has_all_years(self):
        """Test that TFSA_LIMITS has entries from 2009 to 2025"""
        current_year = date.today().year
        expected_years = list(range(2009, min(2026, current_year + 1)))
        
        for year in expected_years:
            assert year in TFSA_LIMITS, f"Year {year} missing from TFSA_LIMITS"
    
    def test_limits_2009_to_2012(self):
        """Test that 2009-2012 limits are $5,000"""
        for year in range(2009, 2013):
            assert TFSA_LIMITS[year] == 5000
    
    def test_limits_2013_2014(self):
        """Test that 2013-2014 limits are $5,500"""
        assert TFSA_LIMITS[2013] == 5500
        assert TFSA_LIMITS[2014] == 5500
    
    def test_limit_2015_special(self):
        """Test that 2015 limit is $10,000 (special year)"""
        assert TFSA_LIMITS[2015] == 10000
    
    def test_limits_2016_2018(self):
        """Test that 2016-2018 limits are $5,500"""
        for year in range(2016, 2019):
            assert TFSA_LIMITS[year] == 5500
    
    def test_limits_2019_2022(self):
        """Test that 2019-2022 limits are $6,000"""
        for year in range(2019, 2023):
            assert TFSA_LIMITS[year] == 6000
    
    def test_limit_2023(self):
        """Test that 2023 limit is $6,500"""
        assert TFSA_LIMITS[2023] == 6500
    
    def test_limits_2024_2025(self):
        """Test that 2024-2025 limits are $7,000"""
        assert TFSA_LIMITS[2024] == 7000
        assert TFSA_LIMITS[2025] == 7000
