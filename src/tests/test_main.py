

import sys
from datetime import datetime
from unittest.mock import MagicMock, patch, PropertyMock
import pytest
from home.homepage import WorkoutApp
import flet as ft

# Prevent psycopg2 / real DB connection
sys.modules.setdefault("psycopg2", MagicMock())

# Stub internal modules that WorkoutApp doesn't test directly
for mod in [
    "components.userpfp",
    "components.bottom_nav",
    "components.responsive",
    "database.connection",
    "database.user_queries",
    "home.home_queries",
]:
    sys.modules.setdefault(mod, MagicMock())



#Creates a Basic User
base_user = (
    1,          # [0]  id
    "TestUser", # [1]  username
    "test@gmail.com",  # [2]  email
    "user",     # [3]  role
    18,       # [4] age
    "Female",       # [5] gender
    185,       # [6] height
    85,       # [7] current weight
    75,       # [8] target eight
    2500,       # [9]  calories goal
    5,       # [10] current streak
    25,       # [11] longest streak
    datetime.today(),       # [12] last active
    8000,       # [13] steps
    5,          # [14] salts_goal
    150,        # [15] protein_goal
    2000,       # [16] water_goal
)

user_daily_stats       = (1500, 3, 120, 1800)   # calories, salts, protein, water
user_streak            = (base_user[10], base_user[11])                 # current, longest
user_friends_data = [("Alice", "Running", 5), ("Bob", "Cycling", 3)] # two friends examples
user_friends_empty     = [] # empty friends example



#used to prevent error with control and resize
class ResizableMock(ft.Container):
    def resize(self):
        pass


#create mock page for testing
class MockPage:
    def __init__(self, width=360, height=800):
        #default functionality to reduce errors
        self.width  = width
        self.height = height
        self.platform = ft.PagePlatform.WINDOWS
        self.web = False
        self.on_resize = None
        self.controls = []
        self.overlay  = []
        self.title    = ""
        self.window   = MagicMock()

    def add(self, *controls):
        self.controls.extend(controls)

    def clean(self):
        self.controls.clear()

    def update(self):
        pass

    def run_task(self, coro):
        pass

#function to add data to page to test
def make_app(
    user_data=None,
    daily_stats=None,
    friends=None,
    streak=None,
    page_width=360,
    page_height=800):

    #either uses data entered via function or uses default
    user_data   = user_data   or base_user
    daily_stats = daily_stats or user_daily_stats
    friends     = friends     if friends is not None else user_friends_data
    streak      = streak      or user_streak

    # Responsive returns a proportion of page dimensions
    mock_responsive = MagicMock()
    mock_responsive.w.side_effect = lambda pct: page_width  * pct
    mock_responsive.h.side_effect = lambda pct: page_height * pct

    page = MockPage(width=page_width, height=page_height)
    #uses functions with appropriate data for proper testing
    with (
        patch("home.homepage.get_user",                   return_value=user_data),
        patch("home.homepage.retrieve_daily_stats",        return_value=daily_stats),
        patch("home.homepage.retrieve_friends_activities", return_value=friends),
        patch("home.homepage.retrieve_current_streak",     return_value=streak),
        patch("home.homepage.Responsive",                  return_value=mock_responsive),
        patch("home.homepage.Userpfp",                     return_value=ResizableMock()),
        patch("home.homepage.NavBar",                      return_value=ResizableMock()),
    ):

        app = WorkoutApp(page, user_id=1)

    return app, page


#used to test the text appears
class TestTextContent:
    #makes sure the users name appears
    def test_welcome_text_contains_username(self):
        app, _ = make_app()
        assert "TestUser" in app.welcome_text.value

    #makes sure steps appear correctly
    def test_steps_text_shows_step_count(self):
        app, _ = make_app()
        assert "8000" in app.steps_text.value

    # make sure the values appear in the app
    def test_calories_text_shows_consumed_and_goal(self):
        app, _ = make_app()
        assert "1500" in app.calories_text.value
        assert "2500" in app.calories_text.value

    def test_salts_text_shows_values(self):
        app, _ = make_app()
        assert "3"  in app.salts_text.value
        assert "5"  in app.salts_text.value

    def test_protein_text_shows_values(self):
        app, _ = make_app()
        assert "120" in app.protein_text.value
        assert "150" in app.protein_text.value

    def test_water_text_shows_values(self):
        app, _ = make_app()
        assert "1800" in app.water_text.value
        assert "2000" in app.water_text.value
    #makes sure the correct streak appears
    def test_streak_texts_show_correct_numbers(self):
        app, _ = make_app()
        assert "5"  in app.current_streak_text.value
        assert "25" in app.longest_streak_text.value



#tests with results are null to show how it can deal with nulltype
class TestNullSafety:
    #sets all goals to none for testing
    def _user_with_none_goals(self):
        user = list(base_user)
        user[9]  = None   # calories_goal
        user[14] = None   # salts_goal
        user[15] = None   # protein_goal
        user[16] = None   # water_goal
        user[13] = None   # steps
        return tuple(user)

    #makes sure they don't crash the page
    def test_none_goals_do_not_raise(self):
        app, _ = make_app(user_data=self._user_with_none_goals())
        assert app is not None
    #makes sure the goals default
    def test_none_calories_goal_shows_zero(self):
        app, _ = make_app(user_data=self._user_with_none_goals())
        assert "/ 0" in app.calories_text.value

    def test_none_steps_shows_zero(self):
        app, _ = make_app(user_data=self._user_with_none_goals())
        assert "0" in app.steps_text.value


#tests friends widget
class TestFriendsWidget:
    #makes sure the right number of tiles appear
    def test_friends_container_has_list_tiles_when_friends_present(self):
        app, _ = make_app(friends=user_friends_data)
        tiles = app.friends_container.content.controls
        assert len(tiles) == 2
    #makes sure the name and exercise appears correctly
    def test_friend_tile_shows_name_and_activity(self):
        app, _ = make_app(friends=user_friends_data)
        tile = app.friends_container.content.controls[0]
        assert tile.title.value    == "Alice"
        assert tile.subtitle.value == "Running"
    #makes sure the streak is visible
    def test_friend_tile_shows_streak(self):
        app, _ = make_app(friends=user_friends_data)
        tile = app.friends_container.content.controls[0]
        assert "5" in tile.trailing.value
    #makes sure if no friends it appears corretcly
    def test_empty_friends_shows_fallback_message(self):
        app, _ = make_app(friends=user_friends_empty)
        controls = app.friends_container.content.controls
        assert len(controls) == 1
        assert "No Friends" in controls[0].value



#tests widget change size with changing window size,
class TestWidgetSizing:
    def test_steps_container_is_square(self):
        app, _ = make_app()
        assert app.steps_container.width == app.steps_container.height

    def test_foodlog_container_is_square(self):
        app, _ = make_app()
        assert app.foodlog_container.width == app.foodlog_container.height

    def test_streak_container_spans_full_width(self):
        app, _ = make_app()
        # streak container should be ~95% of page width
        assert app.streak_container.width == pytest.approx(360 * 0.95)


#tests that window can be resized properly

class TestResize:
    def _make_responsive_mock(self, page):
        mock_r = MagicMock()
        mock_r.w.side_effect = lambda p: page.width  * p
        mock_r.h.side_effect = lambda p: page.height * p
        return mock_r

    def test_resize_does_not_raise(self):
        app, page = make_app()
        app.update = lambda: None  # prevent Flet walking parent chain
        with patch("home.homepage.Responsive", return_value=self._make_responsive_mock(page)):
            app.resize(MagicMock())

    def test_resize_updates_welcome_text_size(self):
        app, page = make_app()
        app.update = lambda: None  # prevent Flet walking parent chain
        original_size = app.welcome_text.size

        page.width = 720
        with patch("home.homepage.Responsive", return_value=self._make_responsive_mock(page)):
            app.resize(MagicMock())

        assert app.welcome_text.size > original_size

#test 0 values and high to make sure they work no matter the value
@pytest.mark.parametrize("stats,expected_pairs", [
    ((0, 0, 0, 0),
    [("0", "calories_text"),
    ("0", "salts_text"),
    ("0","protein_text"),
     ("0","water_text")]),
    ((9999, 50, 999, 9999),
    [("9999", "calories_text"),
    ("50",   "salts_text"),
    ("999",  "protein_text"),
    ("9999",  "water_text"),]),
])
def test_daily_stat_values_render_correctly(stats, expected_pairs):
    app, _ = make_app(daily_stats=stats)
    for value, attr in expected_pairs:
        assert value in getattr(app, attr).value