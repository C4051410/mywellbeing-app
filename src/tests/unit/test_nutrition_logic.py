"""
    This module handles the unit tests for nutrition page
    This tests that the functions used work as intended and
    they return the correct response
"""
from unittest.mock import patch
from datetime import date

import pytest

from nutrition.nutrition_services import (search_food_db, save_foodlog, retrieve_daily_stats,
                                          retrieve_user_goals, save_waterlog, retrieve_foodlogs, retrieve_waterlogs)



@patch('nutrition.nutrition_services.get_foodlog')
class TestRetrieveFoodLogs:
    """
    UNIT TESTS: Tests that food logs are returned correctly
    """
    def test_retrieve_food_logs(self,mock_foodlog):
        #create food logs to be returned
        mock_foodlog.return_value = [["Apple",200,0.1,2,"Snack",date.today()],
                                     ["Steak",500,3.4,15.6,"Dinner",date.today()]]
        foodlogs = retrieve_foodlogs(1)
        #check that both food logs are returned correctly
        assert len(foodlogs) == 2
        assert foodlogs[0][0] == "Apple"
        assert foodlogs[1][0] == "Steak"
    def test_retrieve_food_logs_empty(self,mock_foodlog):
        #test that None returns an empty row
        mock_foodlog.return_value = None
        foodlogs = retrieve_foodlogs(1)
        assert len(foodlogs) == 0

@patch('nutrition.nutrition_services.get_waterlog')
class TestRetrieveWaterLogs:
    """
    UNIT TESTS: Tests that water logs are returned correctly
    """
    def test_retrieve_water_logs(self,mock_waterlog):
        #mock water logs values
        mock_waterlog.return_value = [[1000,date.today()],[2000,date.today()]]
        waterlogs = retrieve_waterlogs(1)
        #make sure water logs are returned and retrieved successfully
        assert len(waterlogs) == 2
        assert waterlogs[0][0] == 1000
        assert waterlogs[1][0] == 2000
    def test_retrieve_water_logs_empty(self,mock_waterlog):
        #check that None returns empty row
        mock_waterlog.return_value = None
        waterlogs = retrieve_waterlogs(1)
        assert len(waterlogs) == 0


class TestFoodSearch:
    """
    UNIT TESTS: Validates the fuzzy search logic using difflib.
    Ensures exact matches and suggestions work without DB interaction.
    """
    #mocks simple food database rather than have full details
    food_db = {"Apple": 52, "Banana": 89, "Chicken Breast": 165}

    def test_search_exact_match(self):
        #should return exact amount if matches exactly
        match_type, result = search_food_db("Apple", self.food_db)
        assert match_type == "exact"
        assert result == 52

    def test_search_suggestion(self):
        #'Appel' should suggest 'Apple' with cutoff 0.6
        match_type, result = search_food_db("Appel", self.food_db)
        assert match_type == "suggestion"
        #returns the correct suggestion
        assert result == "Apple"

    def test_search_no_match(self):
        #makes sure doesn't always return a value if not found
        match_type, result = search_food_db("NoneExistentFood", self.food_db)
        assert match_type is None
        assert result is None


#patches certain functions to block/give mock results,
@patch("nutrition.nutrition_services.commit_foodlog")
@patch("nutrition.nutrition_services.notification")
@patch("nutrition.nutrition_services.retrieve_notification_status")
class TestSaveFoodLog:
    """
    UNIT TESTS: Validates input sanitization for food logging.
    Ensures negative values and missing fields are blocked before DB commit.
    """

    def test_save_food_success(self,mock_status, mock_notify, mock_commit):
        #valid foodlog should be stored successfully
        mock_status.return_value = True
        success, message = save_foodlog("Pizza", 500, 2, 15, 10, 10, date.today(), "Dinner", 1)
        assert success is True
        assert message == "Successful"
        #check the commit_foodlog was only called once
        mock_commit.assert_called_once()

    def test_save_food_negative_values(self,mock_status, mock_notify, mock_commit):
        #checks calories cannot be negative
        success, message = save_foodlog("Pizza", -500, 2, 15, 10, 12, date.today(), "Dinner", 1)
        assert success is False
        assert message == "Values Cannot be Negative"
        #check commit wasnt called
        mock_commit.assert_not_called()

    def test_save_food_missing_fields(self,mock_status, mock_notify, mock_commit):
        #checks values cant be missing or None
        success, message = save_foodlog("", None, 2, 15, 10, 11, date.today(), "Dinner", 1)
        assert success is False
        assert message == "All Fields Required"
        mock_commit.assert_not_called()

#patches certain functions to block/give mock results,
@patch("nutrition.nutrition_services.commit_waterlog")
@patch("nutrition.nutrition_services.notification")
@patch("nutrition.nutrition_services.retrieve_notification_status")
class TestSaveWaterlog:
    """
    UNIT TESTS: Validates input sanitization for waterlog.
    """
    def test_save_waterlog_success(self,mock_status, mock_notify, mock_commit):
        #tests that a valid response returns correct message
        mock_commit.return_value = True
        success, message = save_waterlog(1000,date.today(),1)
        assert success is True
        assert message == "Successful"

    #will test both 0 and negative values
    @pytest.mark.parametrize("value", [0, -1])
    def test_save_waterlog_negative_values(self, mock_status, mock_notify, mock_commit,value):
        success, message = save_waterlog(value, date.today(), 1)
        #check 0 and negative fails
        assert success is False
        assert message == "Values Cannot be Negative or 0"

    #checks that each field will catch if None
    @pytest.mark.parametrize("values", [[None,date.today(),1],[1000,None,1],[1000,date.today(),None]])
    def test_save_waterlog_missing_fields(self,mock_status, mock_notify, mock_commit,values):
        success, message = save_waterlog(values[0],values[1],values[2])
        #check that catches missing fields
        assert success is False
        assert message == "All Fields Required"



@patch("nutrition.nutrition_services.get_daily_stats")
class TestDailyStatsLogic:
    """
    UNIT TESTS: Verifies the calculation logic for daily totals.
    Tests how the service handles None values and multiple database rows.
    """

    def test_retrieve_stats(self, mock_get_stats):
        # mocking DB return: Food data (cals, salt, protein) and Water data
        mock_food = [(200, 1.5, 10.0, 2.0, 50.0), (300, 0.5, 5.0, 1.0, 60.0)]
        mock_water = [(500,), (250,)]
        mock_get_stats.return_value = (mock_food, mock_water)
        #calls on function
        c, s, p, f, carbs, w = retrieve_daily_stats(1, date.today())

        #check the totals add up of daily stats
        assert c == 500  # 200 + 300
        assert s == 2.0  # 1.5 + 0.5
        assert p == 15.0  # 10.0 + 5.0
        assert w == 750  # 500 + 250
        assert f == 3.0
        assert carbs == 110.0

    def test_retrieve_stats_with_nones(self, mock_get_stats):
        # test resilience against NULL values in the database
        mock_food = [(None, 1.0, None, None, None)]
        mock_water = [(100,)]
        mock_get_stats.return_value = (mock_food, mock_water)
        #checks the values default to 0
        c, s, p, f, carbs, w = retrieve_daily_stats(1, date.today())
        assert c == 0
        assert s == 1.0
        assert p == 0.0
        assert w == 100
        assert f == 0.0
        assert carbs == 0.0


@patch("nutrition.nutrition_services.get_user_goals")
class TestUserGoalsLogic:
    """
        UNIT TESTS: Verifies that the correct user goals are returned
        Tests how it deals with empty or none goals.
        """
    def test_retrieve_goals(self,mock_get_goals):
        #mock user goals return
        mock_goals = (2000,6,40,3000)
        mock_get_goals.return_value = mock_goals
        #calls on function
        c,s,p,f,carbs,w = retrieve_user_goals(1)
        assert c == 2000
        assert s == 6.0
        assert p == 40.0
        assert w == 3000
        assert f == 50
        assert carbs == 200

    def test_retrieve_goals_with_nones(self, mock_get_goals):
        mock_goals = (None,6,None,3000)
        mock_get_goals.return_value = mock_goals
        c,s,p,f,carbs,w = retrieve_user_goals(1)
        assert c == 1 #default to 1 to avoid /0
        assert s == 6.0
        assert p == 100.0 #defaults to 100 to avoid /0
        assert w == 3000
        assert f == 50
        assert carbs == 200