import sys
from unittest.mock import MagicMock
import pytest
import flet as ft

# 1. STOP flet from actually running a window during tests
ft.run = lambda *args, **kwargs: None

# Helper to create mocks that return the expected string for our assertions
def create_mock_module(func_name, return_val):
    mock = MagicMock()
    setattr(mock, func_name, lambda *args, **kwargs: return_val)
    return mock

# 2. Mock ALL problematic modules based on your folder structure
sys.modules['auth'] = MagicMock()
sys.modules['auth.authpage'] = MagicMock()
sys.modules['auth.authpage'].authPage = lambda *args, **kwargs: None

sys.modules['home.homepage'] = create_mock_module("main_homepage", "homepage")
sys.modules['activities.activities'] = create_mock_module("main_activities", "activities")
sys.modules['nutrition.nutrition'] = create_mock_module("main_nutrition", "nutrition")
sys.modules['social.social'] = create_mock_module("main_social", "social")
sys.modules['activities.map'] = create_mock_module("main_map", "map")
sys.modules['settings.settings'] = create_mock_module("main_settings", "settings")
sys.modules['settings.account_settings'] = create_mock_module("main_account_settings", "account")

mock_conn = MagicMock()
sys.modules["psycopg2"] = MagicMock()
import database.connection
database.connection.connect = MagicMock(return_value=mock_conn)
# 3. Import main now that mocks are set
from main import main

class MockPage:
    def __init__(self):
        self.route = "/home"
        self.controls = []
        self.overlay = [] 
        self.user_id = None
        self.window = MagicMock()
        self.on_route_change = None
        self.platform = ft.PagePlatform.WINDOWS
        self.web = False
        self.height = 800
        self.width = 360
        self.title = ""

    def add(self, component):
        self.controls.append(component)

    def clean(self):
        self.controls = []

    def update(self):
        pass

    def run_task(self, task):
        pass

def test_main_setup():
    page = MockPage()
    main(page)
    assert page.title == "My Wellbeing"
    assert page.window.width == 360
    assert page.window.height == 800
    assert page.user_id is None
    assert page.on_route_change is not None

@pytest.mark.parametrize("route,expected", [
    ("/home", "homepage"),
    ("/activities", "activities"),
    ("/nutrition", "nutrition"),
    ("/social", "social"),
    ("/settings", "settings"),
    ("/map", "map"),
    ("/account-settings", "account"),
])
def test_routes(route, expected):
    page = MockPage()
    main(page)
    page.user_id = 1
    page.route = route
    page.on_route_change()
    assert expected in page.controls