from datetime import datetime

import pytest
from unittest.mock import patch
from home.home_services import retrieve_username, retrieve_friends_activities, retrieve_current_streaks


class TestHomeLogic:
    """
    UNIT TESTS: Home Screen Logic
    Ensures that the dashboard defaults correctly if the database returns
    empty results or invalid IDs.
    """

    @patch("home.home_services.get_username")
    def test_retrieve_username_success(self, mock_get_user):
        #real ID returns real name
        mock_get_user.return_value = "JohnDoe"
        result = retrieve_username(1)
        assert result == "JohnDoe"

    @patch("home.home_services.get_username")
    def test_retrieve_username_fallback(self, mock_get_user):
        #test fallback when ID is valid but database has no record
        mock_get_user.return_value = None
        assert retrieve_username(1) == "DefaultUsername"

    #tests all possible types of bad id's
    @pytest.mark.parametrize("bad_id", [None, -1, "abc"])
    def test_retrieve_username_invalid_id(self, bad_id):
        #returns DefaultUsername without even calling the database
        assert retrieve_username(bad_id) == "DefaultUsername"

    @patch("home.home_services.get_friends_activities")
    def test_retrieve_friends_activities(self, mock_get_friends):
        #tests that it returns all friends activities
        mock_get_friends.return_value = [("Dave", "Swimming", 5),("Dan","Run",25)]
        result = retrieve_friends_activities(1, datetime.today())
        assert result == [("Dave", "Swimming", 5),("Dan", "Run", 25)]

    @patch("home.home_services.get_friends_activities")
    def test_retrieve_friends_activities_empty(self, mock_get_friends):
        #ensures UI gets an empty list instead of None
        mock_get_friends.return_value = None
        result = retrieve_friends_activities(1, datetime.today())
        assert result == []


    @patch("home.home_services.get_current_streaks")
    def test_retrieve_streaks_crash_prevention(self, mock_get_streaks):
        #tests that if streak is empty return 0 rather then empty to avoid crash
        mock_get_streaks.return_value = None
        result = retrieve_current_streaks(1)

        assert result == [0, 0]
        assert result[0] == 0
        assert result[1] == 0

    @patch("home.home_services.get_current_streaks")
    def test_retrieve_streaks_success(self, mock_get_streaks):
        # show successful retrieval of streak
        mock_get_streaks.return_value = [3, 5]
        result = retrieve_current_streaks(1)
        assert result == [3, 5]