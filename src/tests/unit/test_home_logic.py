from datetime import datetime

import pytest
from unittest.mock import patch
from home.home_services import retrieve_user_stats, retrieve_friends_activities


class TestHomeLogic:
    """
    UNIT TESTS: Home Screen Logic
    Ensures that the dashboard defaults correctly if the database returns
    empty results or invalid IDs.
    """

    @patch("home.home_services.get_user_stats")
    def test_retrieve_username_success(self, mock_get_user):
        #real ID returns real name
        mock_get_user.return_value = ["TestUser",5,25,2500,2000]
        usrnme,cnt_stk,lgt_stk,cal_gol,cal_total = retrieve_user_stats(1)
        assert usrnme == "TestUser"
        assert cnt_stk == 5
        assert lgt_stk == 25
        assert cal_gol == 2500
        assert cal_total == 2000

    @patch("home.home_services.get_user_stats")
    def test_retrieve_username_fallback(self, mock_get_user):
        #test fallback when ID is valid but database has no record
        mock_get_user.return_value = None
        assert retrieve_user_stats(1) == ["DefaultUsername",1,1,0,1]

    #tests all possible types of bad id's
    @pytest.mark.parametrize("bad_id", [None, -1, "abc"])
    def test_retrieve_username_invalid_id(self, bad_id):
        #returns DefaultUsername without even calling the database
        assert retrieve_user_stats(bad_id) == ["DefaultUsername",1,1,0,1]

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
