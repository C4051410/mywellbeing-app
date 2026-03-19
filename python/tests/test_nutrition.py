import sys
import types
from unittest.mock import MagicMock
import pytest

import flet as ft
ft.run = lambda *args, **kwargs: None

# Mock DB logics as cant use proper connection
mock_db = MagicMock()
mock_conn = MagicMock()
mock_cur = MagicMock()

mock_db.connect.return_value = mock_conn
mock_conn.cursor.return_value = mock_cur

#create mock list of food logs
mock_food_row = [("Chicken Burger", 800, 3.2, 25.0, "Dinner", "2026-03-18"),
                 ("Chicken Salad", 400, 1.2, 35.0, "Lunch", "2026-03-17")]
mock_water_rows = [
    (500, "2026-03-16"),
    (250, "2026-03-15")
]
# used to create
def get_mock_responses():
    yield mock_food_row              # retrieve_posts (food)
    yield mock_water_rows            # retrieve_posts (water)
    yield [(500, 2.5, 10)]           # retrieve_daily_stats (food)
    yield [(1000,)]                  # retrieve_daily_stats (water)
    yield [(2000, 6.0, 15.0, 2000)]   # retrieve_user_goals

# This helper ensures every test gets a FRESH generator
def fresh_side_effect(*args, **kwargs):
    # We create a new generator instance if one doesn't exist for this call sequence
    if not hasattr(fresh_side_effect, "gen"):
        fresh_side_effect.gen = get_mock_responses()
    try:
        return next(fresh_side_effect.gen)
    except StopIteration:
        # Reset for the next test function
        fresh_side_effect.gen = get_mock_responses()
        return next(fresh_side_effect.gen)

mock_cur.fetchall.side_effect = fresh_side_effect

# used to mock logic to avoid having to access uncessary content
sys.modules['psycopg2'] = mock_db
sys.modules['UI.components.userpfp'] = MagicMock()
sys.modules['UI.components.bottom_nav'] = MagicMock()
sys.modules['UI.components.responsive'] = MagicMock()

import python.UI.pages.nutrition as nutrition_module
from python.UI.pages.nutrition import main_nutrition
nutrition_module.conn = mock_conn
#used to create a mock flet page
class MockPage:
    def __init__(self):
        self.controls = []
    def update(self):
        pass
# provides a fresh page each time to every function
@pytest.fixture
def nutrition_page():
    page = MockPage()
    return main_nutrition(page,user_id=1)


def test_nutrition_initial_load(nutrition_page):
    #test that daily stats are created and displayed
    #access stats_card via scrollable
    scrollable = nutrition_page.controls[0]
    stats_card = scrollable.controls[1]

    #retrieves the rows in stats_card
    row_cal_pro = stats_card.content.controls[2]
    row_sal_wtr = stats_card.content.controls[3]
    #retrieve text values in for each stat
    cal_text = row_cal_pro.controls[0].controls[1].value  # The Text control with numbers
    protein_text = row_cal_pro.controls[1].controls[1].value
    salt_text = row_sal_wtr.controls[0].controls[1].value
    water_text = row_sal_wtr.controls[1].controls[1].value
    #tests that what is displayed is what is created
    assert "500 / 2000" in cal_text
    assert "10.00 / 15.00" in protein_text
    assert "2.50 / 6.00" in salt_text
    assert "1000 / 2000" in water_text

def test_logs_display_correctly(nutrition_page):
    #tests that logs are displayed properly
    #retrieve foodlogs from the page
    scrollable = nutrition_page.controls[0]
    food_list = scrollable.controls[4].controls[0]
    burger_tile = food_list.controls[0]
    cal_tile = burger_tile.controls[0]
    sal_tile = burger_tile.controls[1]
    pro_tile = burger_tile.controls[2]


    #retrieve waterlogs from the page
    water_tile = scrollable.controls[5]
    water_list = water_tile.controls[0]

    # Verify Food Log (First item should be "Chicken Burger")
    assert burger_tile.title == "Chicken Burger"
    assert burger_tile.subtitle == "2026-03-18 Dinner"
    assert cal_tile.subtitle == "800"
    assert sal_tile.subtitle == "3.2"
    assert pro_tile.subtitle == "25.0"

    # Verify Water Log (First item should be "500 ml")
    assert "500 ml" in water_list.controls[0].title
    assert "2026-03-16" in water_list.controls[0].subtitle