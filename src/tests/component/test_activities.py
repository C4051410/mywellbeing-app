"""import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import pytest

#used to stop functions and components which could stop tests from working
sys.modules.setdefault("psycopg2", MagicMock())

for mod in [
    "components.bottom_nav",
    "components.responsive",
    "database.connection",
    "activities.activity_queries",
    "activities.strava_api",
]:
    sys.modules.setdefault(mod, MagicMock())

import flet as ft



# a fixed start time to test with dates
fake_start_time = datetime(2026, 3, 10, 12, 0, 0)

#returns a date that falls within the current week
def _this_week(days_ago=0):
    return fake_start_time - timedelta(days=days_ago)
#returns a date that falls outside of the week
def _last_week():
    return fake_start_time - timedelta(days=7)

#creates database row
def make_db_row(title="Morning Run", activity_type="Run", dist=5.0,
                date=None, secs=1800, calories=300, reps=0, source="manual"):
    return (title, activity_type, dist, date or _this_week(), secs, calories, reps, source)


#prevent errors withs controls and resize
class ResizableMock(ft.Container):
    def resize(self):
        pass

#creates mock page for testing
class MockPage:
    def __init__(self, width=360, height=800, user_id=1):
        self.width    = width
        self.height   = height
        self.platform = ft.PagePlatform.WINDOWS
        self.web      = False
        self.on_resize = None
        self.controls  = []
        self.overlay   = []
        self.title     = ""
        self.window    = MagicMock()
        self.user_id   = user_id
        self.snack_bar = None
        self.activity_detail = None

    def add(self, *controls):       self.controls.extend(controls)
    def clean(self):                self.controls.clear()
    def update(self):               pass
    def run_task(self, coro):       pass
    def go(self, route):            self.route = route



#used to add data to page
def make_activities(
    db_rows=None,
    strava_rows=None,
    has_strava_tokens=False,
    user_id=1,
    fake_now=None,):
    #adds custom data or default if non entered
    db_rows      = db_rows      if db_rows      is not None else []
    strava_rows  = strava_rows  if strava_rows  is not None else []
    fake_now     = fake_now     or fake_start_time

    #returns proportions of page
    mock_responsive = MagicMock()
    mock_responsive.w.side_effect = lambda pct: 360 * pct
    mock_responsive.h.side_effect = lambda pct: 800 * pct

    page = MockPage(user_id=user_id)

    #used to mock the return function
    with (
        patch("activities.activities.get_activities",           return_value=db_rows),
        patch("activities.activities.get_saved_activities",     return_value=strava_rows),
        patch("activities.activities.format_strava_activities", return_value=strava_rows),
        patch("activities.activities.load_tokens_for_user",     return_value={"token": "x"} if has_strava_tokens else None),
        patch("activities.activities.save_tokens_for_user",     return_value=None),
        patch("activities.activities.connect_strava",           return_value={}),
        patch("activities.activities.Responsive",               return_value=mock_responsive),
        patch("activities.activities.NavBar",                   return_value=ResizableMock()),
        patch("activities.activities.datetime") as mock_dt,
    ):
        #fix datetime values so that they work properly
        mock_dt.now.return_value = fake_now
        mock_dt.min = datetime.min
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        from activities.activities import ActivitiesPage
        app = ActivitiesPage(page)

    app.update = lambda: None
    return app, page

#used to build a page with an activity detail
def make_detail(activity=None):
    page = MockPage()
    page.activity_detail = activity

    with patch("activities.activities.NavBar", return_value=ResizableMock()):
        from activities.activities import ActivityDetailPage
        detail = ActivityDetailPage(page)

    detail.update = lambda: None
    return detail, page


#makes sure the format time function works correctly
class TestFormatTime:
    def app(self):
        app, _ = make_activities()
        return app

    def test_zero_seconds(self):
        assert self.app().format_time(0) == "0s"

    def test_seconds_only(self):
        assert self.app().format_time(45) == "45s"

    def test_minutes_and_seconds(self):
        assert self.app().format_time(90) == "1m 30s"

    def test_hours_and_minutes(self):
        assert self.app().format_time(3661) == "1h 1m"

    def test_exact_one_hour(self):
        assert self.app().format_time(3600) == "1h 0m"

    def test_exact_one_minute(self):
        assert self.app().format_time(60) == "1m 0s"




#make sure the activities feed appears
class TestActivityFeed:
    def feed_column(self, app):
        content_col = app.controls[0]
        feed_container = content_col.controls[-1]
        return feed_container.content
    #makes an empty activities list only displays the header
    def test_empty_state_rendered_when_no_activities(self):
        app, _ = make_activities(db_rows=[])
        feed = self.feed_column(app)
        assert len(feed.controls) == 2
        assert isinstance(feed.controls[0], ft.Text)
        assert isinstance(feed.controls[1], ft.Container)

    #makes sure a single populated displays the activity and header
    def test_populated_feed_has_header_plus_tiles(self):
        rows = [make_db_row()]
        app, _ = make_activities(db_rows=rows)
        feed = self.feed_column(app)
        assert isinstance(feed.controls[0], ft.Text)
        assert len(feed.controls) == 2
    #makes sure a multi populated displays the activities and header
    def test_multiple_activities_allappear(self):
        rows = [make_db_row(title=f"Run {i}") for i in range(3)]
        app, _ = make_activities(db_rows=rows)
        feed = self.feed_column(app)
        assert len(feed.controls) == 1 + len(rows)



class TestActivityDetailPage:
    FULL_ACTIVITY = {
        "title":      "Morning Run",
        "type":       "Run",
        "date":       "Mar 10, 12:00",
        "time":       "30m 0s",
        "dist":       "5.00",
        "calories":   "300",
        "heart_rate": "145",
        "reps":       "0",
        "source":     "manual",
    }
    #Collect all stat row label strings from the detail page.
    def stat_labels(self, detail):
        content_col = detail.controls[0]
        stats_container = content_col.controls[1]
        stats_col = stats_container.content
        labels = []
        for container in stats_col.controls:
            row = container.content
            label_row = row.controls[0]
            label_text = label_row.controls[1].value
            labels.append(label_text)
        return labels
    #makes sure the fields that should always be present are present
    def test_always_present_fields_shown(self):
        detail, _ = make_detail(activity=self.FULL_ACTIVITY)
        labels = self.stat_labels(detail)
        assert "Type"     in labels
        assert "Date"     in labels
        assert "Duration" in labels
        assert "Calories" in labels
        assert "Source" in labels

    #tests that they only appear when they should
    def test_heart_rate_shown_when_present(self):
        detail, _ = make_detail(activity=self.FULL_ACTIVITY)
        labels = self.stat_labels(detail)
        assert "Avg Heart Rate" in labels

    def test_zero_distance_hidden(self):
        act = {**self.FULL_ACTIVITY, "dist": "0.00"}
        detail, _ = make_detail(activity=act)
        labels = self.stat_labels(detail)
        assert "Distance" not in labels

    def test_nonzero_distance_shown(self):
        detail, _ = make_detail(activity=self.FULL_ACTIVITY)
        labels = self.stat_labels(detail)
        assert "Distance" in labels

    def test_no_activity_shows_error_text(self):
        detail, _ = make_detail(activity=None)
        assert isinstance(detail.controls[0], ft.Text)
        assert "No activity" in detail.controls[0].value



@pytest.mark.parametrize("seconds,expected", [
    (0,     "0s"),
    (1,     "1s"),
    (59,    "59s"),
    (60,    "1m 0s"),
    (3600,  "1h 0m"),
    (3661,  "1h 1m"),
    (7322,  "2h 2m"),
])
def test_format_time_parametrised(seconds, expected):
    app, _ = make_activities()
    assert app.format_time(seconds) == expected """