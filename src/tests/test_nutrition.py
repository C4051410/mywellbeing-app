

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



#stores users stats to be tested
user_daily_stats = (1500.0, 3.0, 120.0, 1800.0)

#stores users goal to be tested
user_stats_goal = (2500.0, 5.0, 150.0, 2000.0)

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
    page_height=800,
):
    #adds custom data or default if non entered
    daily_stats = daily_stats if daily_stats is not None else user_daily_stats
    user_goals  = user_goals  if user_goals  is not None else user_stats_goal
    food_rows   = food_rows   if food_rows   is not None else user_food_rows
    water_rows  = water_rows  if water_rows  is not None else user_water_rows

    mock_responsive = MagicMock()
    mock_responsive.w.side_effect = lambda pct: page_width  * pct
    mock_responsive.h.side_effect = lambda pct: page_height * pct

    page = MockPage(width=page_width, height=page_height)

    # Patch open() to prevent FileNotFoundError for foods.csv.
    # NutritionPage catches FileNotFoundError gracefully, so this just
    # ensures food_db stays empty — we inject fake_food_db in tests that
    # need it.
    mock_open = MagicMock(side_effect=FileNotFoundError)

    with (
        patch("nutrition.nutrition.retrieve_daily_stats", return_value=daily_stats),
        patch("nutrition.nutrition.retrieve_user_goals",  return_value=user_goals),
        patch("nutrition.nutrition.retrieve_foodlog",     return_value=food_rows),
        patch("nutrition.nutrition.retrieve_waterlog",    return_value=water_rows),
        patch("nutrition.nutrition.save_foodlog",         return_value=None),
        patch("nutrition.nutrition.save_waterlog",        return_value=None),
        patch("nutrition.nutrition.Responsive",           return_value=mock_responsive),
        patch("nutrition.nutrition.Userpfp",              return_value=ResizableMock()),
        patch("nutrition.nutrition.NavBar",               return_value=ResizableMock()),
        patch("builtins.open",                            mock_open),
    ):
        from nutrition.nutrition import NutritionPage
        app = NutritionPage(page, user_id=1)

    app.update = lambda: None   # prevent Flet parent-chain walk on .update()
    return app, page



#used to test the stats cards
class TestStatsCard:
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
    def test_foodlog_tiles_match_db_rows(self):
        app, _ = make_nutrition(food_rows=user_food_rows)
        tiles = app.foodlog_list.controls
        assert len(tiles) == len(user_food_rows)

    def test_foodlog_tile_shows_food_name(self):
        app, _ = make_nutrition(food_rows=user_food_rows)
        # ExpansionTile title is the food name from the DB row
        assert app.foodlog_list.controls[0].title == "Chicken"

    def test_waterlog_tiles_match_db_rows(self):
        app, _ = make_nutrition(water_rows=user_water_rows)
        tiles = app.waterlog_list.controls
        assert len(tiles) == len(user_water_rows)

    def test_empty_foodlog_shows_no_tiles(self):
        app, _ = make_nutrition(food_rows=[])
        assert len(app.foodlog_list.controls) == 0

    def test_empty_waterlog_shows_no_tiles(self):
        app, _ = make_nutrition(water_rows=[])
        assert len(app.waterlog_list.controls) == 0



#tests food search function
class TestFoodSearch:
    def _app_with_food_db(self):
        app, page = make_nutrition()
        app.food_db = fake_food_db
        app.main_page = page
        # find_food_values() calls .update() on individual TextFields and
        # main_page — patch them all to prevent Flet's parent-chain walk
        app.calories_input.update  = lambda: None
        app.salts_input.update     = lambda: None
        app.proteins_input.update  = lambda: None
        page.update                = lambda: None
        return app, page

    def test_exact_match_fills_calories(self):
        app, _ = self._app_with_food_db()
        app.food_input.value = "banana"
        app.find_food_values(None)
        assert app.calories_input.value == "89"

    def test_exact_match_fills_salts(self):
        app, _ = self._app_with_food_db()
        app.food_input.value = "banana"
        app.find_food_values(None)
        assert app.salts_input.value == "0.0"

    def test_exact_match_fills_proteins(self):
        app, _ = self._app_with_food_db()
        app.food_input.value = "banana"
        app.find_food_values(None)
        assert app.proteins_input.value == "1.1"

    def test_exact_match_is_case_insensitive(self):
        """food_input strips and lowercases, so 'Banana' should still match."""
        app, _ = self._app_with_food_db()
        app.food_input.value = "Banana"
        app.find_food_values(None)
        assert app.calories_input.value == "89"

    def test_unknown_food_does_not_fill_inputs(self):
        """A completely unknown short string should leave inputs unchanged."""
        app, _ = self._app_with_food_db()
        app.food_input.value = "xy"   # too short for fuzzy match (len <= 2)
        app.find_food_values(None)
        assert app.calories_input.value == ""

    def test_apply_suggestion_sets_food_input(self):
        """apply_suggestion() should update food_input and re-run the lookup."""
        app, _ = self._app_with_food_db()
        app.apply_suggestion("banana")
        assert app.food_input.value == "Banana"
        assert app.calories_input.value == "89"



#tests 0/null divide errors
class TestNullSafety:

    @pytest.mark.xfail(strict=True, reason="ZeroDivisionError — add (goal or 1) guard in nutrition.py")
    def test_zero_calorie_goal_does_not_raise(self):
        make_nutrition(user_goals=(0.0, 5.0, 150.0, 2000.0))

    @pytest.mark.xfail(strict=True, reason="ZeroDivisionError — add (goal or 1) guard in nutrition.py")
    def test_zero_water_goal_does_not_raise(self):
        make_nutrition(user_goals=(2500.0, 5.0, 150.0, 0.0))


#tests boundary of values
@pytest.mark.parametrize("stats,goals,attr,expected", [
    ((0.0, 0.0, 0.0, 0.0), (2500.0, 5.0, 150.0, 2000.0), "calories_text", "0"),
    ((2500.0, 5.0, 150.0, 2000.0), (2500.0, 5.0, 150.0, 2000.0), "calories_text", "2500"),
    ((1000.0, 2.5, 80.0, 900.0), (2500.0, 5.0, 150.0, 2000.0), "water_text", "900"),
])
def test_stat_values_render_correctly(stats, goals, attr, expected):
    app, _ = make_nutrition(daily_stats=stats, user_goals=goals)
    assert expected in getattr(app, attr).value