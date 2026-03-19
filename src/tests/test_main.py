import sys
import types
from unittest.mock import MagicMock
import pytest

import flet as ft
ft.run = lambda *args, **kwargs: None
# Mock ALL problematic modules BEFORE importing main
sys.modules['auth'] = types.ModuleType('auth')
sys.modules['auth.authpage'] = types.ModuleType('auth.authpage')
sys.modules['auth.authpage'].authPage = lambda *args, **kwargs: None

sys.modules['python.UI.pages.activities'] = types.ModuleType('activities')
sys.modules['python.UI.pages.activities'].main_activities = lambda *args, **kwargs: "activities"

sys.modules['python.UI.pages.homepage'] = types.ModuleType('homepage')
sys.modules['python.UI.pages.homepage'].main_homepage = lambda *args, **kwargs: "homepage"

sys.modules['python.UI.pages.map'] = types.ModuleType('map')
sys.modules['python.UI.pages.map'].main_map = lambda *args, **kwargs: "map"

sys.modules['python.UI.pages.nutrition'] = types.ModuleType('nutrition')
sys.modules['python.UI.pages.nutrition'].main_nutrition = lambda *args, **kwargs: "nutrition"

sys.modules['python.UI.pages.settings'] = types.ModuleType('settings')
sys.modules['python.UI.pages.settings'].main_settings = lambda *args, **kwargs: "settings"

sys.modules['python.UI.pages.social'] = types.ModuleType('social')
sys.modules['python.UI.pages.social'].main_social = lambda *args, **kwargs: "social"

sys.modules['UI.pages.account_settings'] = types.ModuleType('account_settings')
sys.modules['UI.pages.account_settings'].main_account_settings = lambda *args, **kwargs: "account"

from main import main

class MockPage:
    def __init__(self):
        self.route = "/home"
        self.controls = []
        self.user_id = None
        self.window = MagicMock()
        self.on_route_change = None

    def add(self, component):
        self.controls.append(component)

    def clean(self):
        self.controls = []

    def update(self):
        pass


def test_main_setup():
    page = MockPage()
    main(page)

    assert page.title == "My Wellbeing"
    assert page.window.width == 360
    assert page.window.height == 800
    assert page.user_id == None
    assert not page.on_route_change == None

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