import pytest
from datetime import date
from tools.calculations import calculate_tfsa_contribution_room, TFSA_LIMITS


class TestCalculateTFSAContributionRoom:
    """Test cases for TFSA contribution room calculation."""

    def test_calculate_room_single_year(self):
        """Should calculate correctly for person who turned 18 current year."""
        current_year = date.today().year
        result = calculate_tfsa_contribution_room(year_turned_18=current_year)
        
        assert result.total_contribution_room == TFSA_LIMITS[current_year]
        assert len(result.yearly_breakdown) == 1
        assert result.yearly_breakdown[current_year] == TFSA_LIMITS[current_year]
        assert len(result.assumptions) > 0

    def test_calculate_room_multiple_years(self):
        """Should calculate correctly for multiple years."""
        result = calculate_tfsa_contribution_room(year_turned_18=2020)
        
        expected_total = sum(TFSA_LIMITS[year] for year in range(2020, date.today().year + 1))
        assert result.total_contribution_room == expected_total
        
        # Check yearly breakdown
        for year in range(2020, date.today().year + 1):
            assert year in result.yearly_breakdown
            assert result.yearly_breakdown[year] == TFSA_LIMITS[year]

    def test_calculate_room_from_2009(self):
        """Should calculate correctly from TFSA inception year."""
        result = calculate_tfsa_contribution_room(year_turned_18=2009)
        
        expected_total = sum(TFSA_LIMITS[year] for year in range(2009, date.today().year + 1))
        assert result.total_contribution_room == expected_total
        assert 2009 in result.yearly_breakdown

    def test_calculate_room_future_year_raises_error(self):
        """Should raise ValueError for future years."""
        future_year = date.today().year + 1
        
        with pytest.raises(ValueError, match="year_turned_18 cannot be in the future"):
            calculate_tfsa_contribution_room(year_turned_18=future_year)

    def test_calculate_room_2015(self):
        """Should correctly handle the year with increased limit (2015)."""
        result = calculate_tfsa_contribution_room(year_turned_18=2015)
        
        # 2015 had a limit of 10000
        assert result.yearly_breakdown[2015] == 10000
        
        # Calculate expected total from 2015 to current year
        expected_total = sum(TFSA_LIMITS[year] for year in range(2015, date.today().year + 1))
        assert result.total_contribution_room == expected_total

    def test_result_has_assumptions(self):
        """Should include assumptions in the result."""
        result = calculate_tfsa_contribution_room(year_turned_18=2020)
        
        assert isinstance(result.assumptions, list)
        assert len(result.assumptions) > 0
        assert any("resident" in assumption.lower() for assumption in result.assumptions)
        assert any("contribution" in assumption.lower() for assumption in result.assumptions)

    def test_calculate_room_2010(self):
        """Should calculate correctly for 2010."""
        result = calculate_tfsa_contribution_room(year_turned_18=2010)
        
        # Verify all years from 2010 to current are included
        current_year = date.today().year
        assert len(result.yearly_breakdown) == (current_year - 2010 + 1)
        
        # Verify specific years
        assert result.yearly_breakdown[2010] == 5000
        assert result.yearly_breakdown[2013] == 5500
        assert result.yearly_breakdown[2015] == 10000
