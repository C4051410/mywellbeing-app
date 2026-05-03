import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from nutrition.nutrition_services import search_food_db, save_foodlog, retrieve_daily_stats, retrieve_user_goals


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
        success, message = save_foodlog("Pizza", 500, 2, 15, date.today(), "Dinner", 1)
        assert success is True
        assert message == "Successful"
        #check the commit_foodlog was only called once
        mock_commit.assert_called_once()

    def test_save_food_negative_values(self,mock_status, mock_notify, mock_commit):
        #checks calories cannot be negative
        success, message = save_foodlog("Pizza", -500, 2, 15, date.today(), "Dinner", 1)
        assert success is False
        assert message == "Values Cannot be Negative"
        #check commit wasnt called
        mock_commit.assert_not_called()

    def test_save_food_missing_fields(self,mock_status, mock_notify, mock_commit):
        #checks values cant be missing or None
        success, message = save_foodlog("", None, 2, 15, date.today(), "Dinner", 1)
        assert success is False
        assert message == "All Fields Required"
        mock_commit.assert_not_called()


@patch("nutrition.nutrition_services.get_daily_stats")
class TestDailyStatsLogic:
    """
    UNIT TESTS: Verifies the calculation logic for daily totals.
    Tests how the service handles None values and multiple database rows.
    """

    def test_retrieve_stats(self, mock_get_stats):
        # mocking DB return: Food data (cals, salt, protein) and Water data
        mock_food = [(200, 1.5, 10.0), (300, 0.5, 5.0)]
        mock_water = [(500,), (250,)]
        mock_get_stats.return_value = (mock_food, mock_water)
        #calls on function
        c, s, p, w = retrieve_daily_stats(1, date.today())

        #check the totals add up of daily stats
        assert c == 500  # 200 + 300
        assert s == 2.0  # 1.5 + 0.5
        assert p == 15.0  # 10.0 + 5.0
        assert w == 750  # 500 + 250

    def test_retrieve_stats_with_nones(self, mock_get_stats):
        # test resilience against NULL values in the database
        mock_food = [(None, 1.0, None)]
        mock_water = [(100,)]
        mock_get_stats.return_value = (mock_food, mock_water)
        #checks the values default to 0
        c, s, p, w = retrieve_daily_stats(1, date.today())
        assert c == 0
        assert s == 1.0
        assert p == 0.0
        assert w == 100

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
        c,s,p,w = retrieve_user_goals(1)
        assert c == 2000
        assert s == 6.0
        assert p == 40.0
        assert w == 3000
    def test_retrieve_goals_with_nones(self, mock_get_goals):
        mock_goals = (None,6,None,3000)
        mock_get_goals.return_value = mock_goals
        c,s,p,w = retrieve_user_goals(1)
        assert c == 1 #default to 1 to avoid /0
        assert s == 6.0
        assert p == 1.0 #defaults to 1 to avoid /0
        assert w == 3000