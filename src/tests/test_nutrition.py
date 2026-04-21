

import sys
from unittest.mock import MagicMock, patch, call
import pytest


#used to stop functions and components which would stop test from working
sys.modules.setdefault("psycopg2", MagicMock())
sys.modules.setdefault("flet_permission_handler", MagicMock())
sys.modules.setdefault("plyer", MagicMock())
sys.modules.setdefault("plyer.notification", MagicMock())

for mod in [
    "components.userpfp",
    "components.bottom_nav",
    "components.responsive",
    "database.connection",
    "database.user_queries",
    "nutrition.nutrition_queries",
]:
    sys.modules.setdefault(mod, MagicMock())

import flet as ft
from nutrition.nutrition import NutritionPage



#stores users stats to be tested
user_daily_stats = (1500.0, 3.0, 120.0, 1800.0)

#stores users goal to be tested
user_stats_goal = (2500.0, 5.0, 150.0, 2000.0)

#stores results when goals are none in database
user_stats_goal_null = (1.0,1.0,1.0,1.0)

#stores rows of food entries to be tested
user_food_rows = [
    ("Chicken", 300, 1.2, 30.0, "Lunch", "2026-01-01"),
    ("Rice",    200, 0.5, 5.0,  "Dinner", "2026-01-01"),
]

#stores rows of water entries to be tested
user_water_rows = [
    (500, "2026-01-01"),
    (300, "2026-01-01"),
]

#used to store a fake db to test stored foods
fake_food_db = {
    "banana": {"name": "Banana", "calories": "89",  "salts": "0.0", "proteins": "1.1"},
    "chicken": {"name": "Chicken", "calories": "239", "salts": "0.8", "proteins": "27.0"},
}

#used to prevent errors with controls and resize
class ResizableMock(ft.Container):
    def resize(self):
        pass

#create mock page for testing
class MockPage:
    def __init__(self, width=360, height=800):
        self.width   = width
        self.height  = height
        self.platform = ft.PagePlatform.WINDOWS
        self.web     = False
        self.on_resize = None
        self.controls  = []
        self.overlay   = []
        self.title     = ""
        self.window    = MagicMock()

    def add(self, *controls):
        self.controls.extend(controls)

    def clean(self):
        self.controls.clear()

    def update(self):
        pass

    def run_task(self, coro):
        pass



#used to add data to page
def make_nutrition(
    daily_stats=None,
    user_goals=None,
    food_rows=None,
    water_rows=None,
    page_width=360,
    page_height=800,):
    #adds custom data or default if non entered
    daily_stats = daily_stats if daily_stats is not None else user_daily_stats
    user_goals  = user_goals  if user_goals  is not None else user_stats_goal
    food_rows   = food_rows   if food_rows   is not None else user_food_rows
    water_rows  = water_rows  if water_rows  is not None else user_water_rows

    #returns proportions of page
    mock_responsive = MagicMock()
    mock_responsive.w.side_effect = lambda pct: page_width  * pct
    mock_responsive.h.side_effect = lambda pct: page_height * pct

    page = MockPage(width=page_width, height=page_height)

    #prevent file not found error when trying to open non-existent csv file
    mock_open = MagicMock(side_effect=FileNotFoundError)
    #used to mock the return of functions
    with (
        patch("nutrition.nutrition.retrieve_daily_stats", return_value=daily_stats),
        patch("nutrition.nutrition.retrieve_user_goals",  return_value=user_goals),
        patch("nutrition.nutrition.retrieve_foodlog",     return_value=food_rows),
        patch("nutrition.nutrition.retrieve_waterlog",    return_value=water_rows),
        patch("nutrition.nutrition.Responsive",           return_value=mock_responsive),
        patch("nutrition.nutrition.Userpfp",              return_value=ResizableMock()),
        patch("nutrition.nutrition.NavBar",               return_value=ResizableMock()),
        patch("builtins.open",                            mock_open),
    ):

        app = NutritionPage(page, user_id=1)

    app.update = lambda: None
    return app, page



#used to test the stats cards
class TestStatsCard:
    #is used to check that the correct text is displayed for each stat
    def test_calories_text_shows_consumed_and_goal(self):
        app, _ = make_nutrition()
        assert "1500" in app.calories_text.value
        assert "2500" in app.calories_text.value
    def test_protein_text_shows_consumed_and_goal(self):
        app, _ = make_nutrition()
        assert "120" in app.protein_text.value
        assert "150" in app.protein_text.value
    def test_salts_text_shows_consumed_and_goal(self):
        app, _ = make_nutrition()
        assert "3"  in app.salts_text.value
        assert "5"  in app.salts_text.value
    def test_water_text_shows_consumed_and_goal(self):
        app, _ = make_nutrition()
        assert "1800" in app.water_text.value
        assert "2000" in app.water_text.value
    #checks to make sure the progress bar is correct for the values entered
    def test_calories_progress_bar_ratio(self):
        # 1500 / 2500 = 0.6
        app, _ = make_nutrition()
        assert app.calories_bar.value == pytest.approx(1500 / 2500)

    def test_protein_progress_bar_ratio(self):
        app, _ = make_nutrition()
        assert app.protein_bar.value == pytest.approx(120 / 150)

    def test_salts_progress_bar_ratio(self):
        app, _ = make_nutrition()
        assert app.salts_bar.value == pytest.approx(3 / 5)

    def test_water_progress_bar_ratio(self):
        app, _ = make_nutrition()
        assert app.water_bar.value == pytest.approx(1800 / 2000)



##used to test display food and water logs
class TestLogDisplay:
    #makes sure the number of food entries are correct + the header
    def test_foodlog_tiles_match_db_rows(self):
        app, _ = make_nutrition(food_rows=user_food_rows)
        tiles = app.foodlog_list.controls
        assert len(tiles) == len(user_food_rows) + 1 #for header
    #makes sure the food title is present
    def test_foodlog_tile_shows_food_header(self):
        app, _ = make_nutrition(food_rows=user_food_rows)
        assert app.foodlog_list.controls[0].value == "ALL RECENT FOOD LOGS"
    #makes sure the food values are present
    def test_foodlog_tile_shows_food(self):
        app, _ = make_nutrition(food_rows=user_food_rows)
        #makes sure all values in the title appear
        tile_text = app.foodlog_list.controls[1].content.title.value
        assert "Chicken" in tile_text
        assert "2026-01-01" in tile_text
        assert "Lunch" in tile_text
        #makes sure all values in the subtitle appear
        subtile_text = app.foodlog_list.controls[1].content.subtitle.value
        assert "30.0" in subtile_text
        assert "1.2" in subtile_text
        assert "300" in subtile_text

    #makes sure the water log is correct + header
    def test_waterlog_tiles_match_db_rows(self):
        app, _ = make_nutrition(water_rows=user_water_rows)
        tiles = app.waterlog_list.controls
        assert len(tiles) == len(user_water_rows) + 1
    def test_foodlog_tile_shows_water_header(self):
        app, _ = make_nutrition(food_rows=user_food_rows)
        assert app.waterlog_list.controls[0].value == "ALL RECENT WATER LOGS"
    def test_waterlog_tile_shows_water_value(self):
        app, _ = make_nutrition(water_rows=user_water_rows)
        tile_text = app.waterlog_list.controls[1].content.title.value
        assert "500ml" in tile_text
        assert "2026-01-01" in tile_text
    #makes sure empty foodlog shows only title and empty message
    def test_empty_foodlog(self):
        app, _ = make_nutrition(food_rows=[])
        assert len(app.foodlog_list.controls) == 2
    #makes sure empty waterlog shows only title and empty message
    def test_empty_waterlog_shows_no_tiles(self):
        app, _ = make_nutrition(water_rows=[])
        assert len(app.waterlog_list.controls) == 2




#tests when goals are empty
class TestEmptySafety:
    #makes sure app doesn't crash when default
    def test_none_goals_do_not_raise(self):
        app, _ = make_nutrition(user_goals=user_stats_goal_null)
        assert app is not None
    #makes sure app does display default values
    def test_none_goal_shows_default(self):
        app, _ = make_nutrition(user_goals=user_stats_goal_null)
        assert app.calories_text.value == "1500 / 1"


#tests boundary of values
@pytest.mark.parametrize("stats,goals,attr,expected", [
    ((0.0, 0.0, 0.0, 0.0), (2500.0, 5.0, 150.0, 2000.0), "calories_text", "0"),
    ((2500.0, 5.0, 150.0, 2000.0), (2500.0, 5.0, 150.0, 2000.0), "calories_text", "2500"),
    ((1000.0, 2.5, 80.0, 900.0), (2500.0, 5.0, 150.0, 2000.0), "water_text", "900"),
])
def test_stat_values_render_correctly(stats, goals, attr, expected):
    app, _ = make_nutrition(daily_stats=stats, user_goals=goals)
    assert expected in getattr(app, attr).value