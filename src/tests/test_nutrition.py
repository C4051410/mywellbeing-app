import sys
import types
from unittest.mock import MagicMock


sys.modules['src.database'] = MagicMock()
sys.modules['src.database.connection'] = MagicMock()

# 2. Clear out the mocks from test_main so we use the REAL nutrition code
for mod in ['nutrition.nutrition', 'nutrition']:
    if mod in sys.modules:
        del sys.modules[mod]

import pytest
import flet as ft

# 3. Standard Mocks for DB and UI components
ft.run = lambda *args, **kwargs: None
mock_db = MagicMock()
mock_conn = MagicMock()
mock_cur = MagicMock()
mock_db.connect.return_value = mock_conn
mock_conn.cursor.return_value = mock_cur

# Mock data rows
mock_food_row = [("Chicken Burger", 800, 3.2, 25.0, "Dinner", "2026-03-18")]
mock_water_rows = [(500, "2026-03-16")]

def get_mock_responses():
    yield mock_food_row             # food logs
    yield mock_water_rows           # water logs
    yield [(500, 2.5, 10)]          # daily stats (food)
    yield [(1000,)]                 # daily stats (water)
    yield [(2000, 6.0, 15.0, 2000)] # user goals

def fresh_side_effect(*args, **kwargs):
    if not hasattr(fresh_side_effect, "gen"):
        fresh_side_effect.gen = get_mock_responses()
    try:
        return next(fresh_side_effect.gen)
    except StopIteration:
        fresh_side_effect.gen = get_mock_responses()
        return next(fresh_side_effect.gen)

mock_cur.fetchall.side_effect = fresh_side_effect

# Mock dependencies
sys.modules['psycopg2'] = mock_db
sys.modules['UI.components.userpfp'] = MagicMock()
sys.modules['UI.components.bottom_nav'] = MagicMock()
sys.modules['UI.components.responsive'] = MagicMock()

# 4. Now import the real logic
import nutrition.nutrition as nutrition_module
from nutrition.nutrition import main_nutrition

# Inject mock connection into the module
nutrition_module.conn = mock_conn

class MockPage:
    def __init__(self):
        self.controls = []
        self.height = 800
        self.width = 360
    def update(self):
        pass

@pytest.fixture
def nutrition_page():
    nutrition_module.conn = mock_conn
    page = MockPage()
    return main_nutrition(page, user_id=1)

def test_nutrition_initial_load(nutrition_page):
    assert not isinstance(nutrition_page, str)
    scrollable = nutrition_page.controls[0]
    stats_card = scrollable.controls[1]
    row_cal_pro = stats_card.content.controls[2]
    cal_text = row_cal_pro.controls[0].controls[1].value
    assert "500 / 2000" in cal_text

def test_logs_display_correctly(nutrition_page):
    scrollable = nutrition_page.controls[0]
    food_list = scrollable.controls[4].controls[0]
    burger_tile = food_list.controls[0]
    assert burger_tile.title == "Chicken Burger"
    assert "2026-03-18" in burger_tile.subtitle