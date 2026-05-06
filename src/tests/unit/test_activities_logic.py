"""
    This module handles the unit tests for activities page
    This tests that the functions used work as intended and
    they return the correct response
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from activities.activities_services import save_activity, save_past_activity, retrieve_activities


class TestActivityLogging:
    """
    UNIT TESTS: Activity Recording Logic
    Validates date constraints, activity types, and numerical boundaries.
    """

    @patch("activities.activities_services.commit_activity")
    @patch("activities.activities_services.notification")
    @patch("activities.activities_services.retrieve_notification_status")
    def test_save_activity_success(self,mock_status, mock_notify, mock_commit):
        mock_status.return_value = True
        valid_date = datetime.now() - timedelta(hours=1)
        #tests valid activity
        success = save_activity(1, "Run", 5.5, 1800, valid_date)
        assert success is True
        #checks it only calls commit once
        mock_commit.assert_called_once()

    def test_save_activity_invalid_type(self):
        #only 'Run', 'Cycle', 'Walk' are allowed
        #checks for invalid activity type
        success = save_activity(1, "Swimming", 1.0, 600, datetime.now())
        assert success is False

    def test_save_activity_future_date(self):
        #activities cannot be recorded in the future
        future_date = datetime.now() + timedelta(days=1)
        success = save_activity(1, "Run", 5.0, 1800, future_date)
        assert success is False

    def test_save_activity_invalid_date(self):
        success = save_activity(1, "Swimming", 1.0, 600, "10 Oclock September 20th")
        assert success is False

    #goes through and tests invalid numbers
    @pytest.mark.parametrize("dist, duration", [
        (-1.0, 100),  # Negative distance
        (5.0, -100),  # Negative duration
        ("five", 100)  # Wrong type
    ])
    def test_save_activity_input_validation(self, dist, duration):
        success = save_activity(1, "Run", dist, duration, datetime.now())
        assert success is False


class TestPastActivityLogging:
    """
    UNIT TESTS: Manual/Past Activity Entries
    Tests complex field sets including calories and reps.
    """

    @patch("activities.activities_services.commit_past_activity")
    @patch("activities.activities_services.notification")
    @patch("activities.activities_services.retrieve_notification_status")
    def test_save_past_activity_success(self,mock_status, mock_notify, mock_commit):
        mock_status.return_value = True
        #tests a valid save past activity
        success = save_past_activity(1, "Gym Session", 300, 3600, 50, 0.0, datetime.now())
        assert success is True
        mock_commit.assert_called_once()

    def test_save_past_activity_missing_fields(self):
        # Testing the 'any(field is None)' logic
        success = save_past_activity(1, "Gym", None, 3600, 50, 0.0, datetime.now())
        assert success is False

    #goes through and check that each value fails if invalid type
    @pytest.mark.parametrize("dist, duration, reps, calories", [
        (-1.0, 100,100,100), #negative distance
        (100, -1.0, 100, 100), #negative duration
        (100, 100, -1.0, 100), #negative reps
        (100, 100, 100, -1.0), #negative calories
    ])
    def test_save_past_activity_input_validation(self, dist, duration, reps, calories):
        success = save_past_activity(1, "Gym", dist, duration, reps, calories,datetime.now())
        assert success is False

    #test for a future date
    def test_save_past_activity_future_date(self):
        future_date = datetime.now() + timedelta(days=1)
        success = save_past_activity(1, "Gym", 200, 3600,0,0,future_date)
        assert success is False
    #test for invalid date
    def test_save_past_activity_invalid_date(self):
        success = save_past_activity(1, "Gym", 200, 3600,0,0,"2 O'Clock May 6th")
        assert success is False

class TestActivityRetrieval:
    """
    UNIT TESTS: Activity Data Retrieval
    Ensures user_id validation happens before database querying.
    """

    @patch("activities.activities_services.get_activities")
    def test_retrieve_activities_valid_id(self, mock_get):
        mock_get.return_value = [("Run", 5.0), ("Walk", 2.0)]
        results = retrieve_activities(1)
        #check correct number results are returned
        assert len(results) == 2
        #check its only called once
        mock_get.assert_called_once_with(1)

    def test_retrieve_activities_invalid_id(self):
        # Should return empty list immediately for bad IDs
        #checks that incorrect id types are rejected
        assert retrieve_activities(-1) == []
        assert retrieve_activities("invalid") == []