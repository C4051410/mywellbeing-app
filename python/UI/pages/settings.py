'''
File for settings page - accessible by clicking 'settings' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive

# Sizes of all elements on homepage (as a percent of screen)
page_title_size = 0.1
page_desc_size = 0.03

class SettingsPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.r = Responsive(page)
        self.this_page = page

        # --- HEADER ---
        self.page_title = ft.Text(value="Settings", size=self.r.w(page_title_size), color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
        self.page_desc = ft.Text(value="Manage your profile and goals", size=self.r.w(page_desc_size), color=ft.Colors.GREY)
        self.userpfp = Userpfp(page)

        # --- INPUT FIELDS ---
        num_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        float_filter = ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$", replacement_string="")

        # Profile Inputs (Loading from session if available)
        self.age_input = ft.TextField(label="Age", value=page.session.store.get("age") or "", input_filter=num_filter, height=50, expand=True)
        self.gender_input = ft.Dropdown(label="Gender", value=page.session.store.get("gender") or "Male", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")], height=50, expand=True)
        self.height_input = ft.TextField(label="Height (cm)", value=page.session.store.get("height") or "", input_filter=float_filter, height=50, expand=True)
        self.weight_input = ft.TextField(label="Weight (kg)", value=page.session.store.get("weight") or "", input_filter=float_filter, height=50, expand=True)

        # New TDEE Inputs
        self.body_fat_input = ft.TextField(label="Body Fat % (Optional)", value=page.session.store.get("body_fat") or "", input_filter=float_filter, height=50, expand=True)
        self.activity_input = ft.Dropdown(
            label="Activity Level",
            value=page.session.store.get("activity_level") or "Moderate",
            options=[
                ft.dropdown.Option("Sedentary", text="Sedentary (Little/No Exercise)"),
                ft.dropdown.Option("Light", text="Light (Exercise 1-3 days/wk)"),
                ft.dropdown.Option("Moderate", text="Moderate (Exercise 3-5 days/wk)"),
                ft.dropdown.Option("Active", text="Active (Exercise 6-7 days/wk)"),
                ft.dropdown.Option("Very Active", text="Very Active (Hard daily exercise)")
            ],
            height=50, expand=True
        )

        # Target Inputs
        self.cal_goal_input = ft.TextField(label="Calories (kcal)", value=page.session.store.get("cal_goal") or "2500", input_filter=num_filter, height=50, expand=True)
        self.water_goal_input = ft.TextField(label="Water (ml)", value=page.session.store.get("water_goal") or "2000", input_filter=num_filter, height=50, expand=True)
        self.protein_goal_input = ft.TextField(label="Protein (g)", value=page.session.store.get("protein_goal") or "50.0", input_filter=float_filter, height=50, expand=True)
        self.salts_goal_input = ft.TextField(label="Salts (g)", value=page.session.store.get("salts_goal") or "6.0", input_filter=float_filter, height=50, expand=True)

        # TDEE Calculate Button
        self.calc_tdee_btn = ft.ElevatedButton(
            content=ft.Row([ft.Icon(ft.Icons.CALCULATE, color=ft.Colors.BLUE_600), ft.Text("Auto-Calculate Calories", color=ft.Colors.BLUE_600, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_50, shape=ft.RoundedRectangleBorder(radius=8)),
            height=45,
            on_click=self.calculate_tdee
        )

        # --- UI CARDS ---
        self.profile_card = ft.Container(
            bgcolor=ft.Colors.WHITE, border_radius=10, padding=15, shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column([
                ft.Text("PERSONAL PROFILE", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                ft.Row([self.age_input, self.gender_input]),
                ft.Row([self.height_input, self.weight_input]),
                ft.Row([self.activity_input]),
                ft.Row([self.body_fat_input])
            ])
        )

        self.targets_container = ft.Container(
            bgcolor=ft.Colors.WHITE, border_radius=10, padding=15, shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column([
                ft.Text("DAILY GOALS", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                self.calc_tdee_btn,
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                ft.Row([self.cal_goal_input, self.water_goal_input]),
                ft.Row([self.protein_goal_input, self.salts_goal_input])
            ])
        )

        self.save_button = ft.ElevatedButton(
            content=ft.Text("Save Settings", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            style=ft.ButtonStyle(bgcolor=ft.Colors.DEEP_ORANGE, shape=ft.RoundedRectangleBorder(radius=20)),
            width=200, height=45, on_click=self.save_settings
        )

        self.nav_bar = NavBar(page)

        # --- LAYOUT ASSEMBLY ---
        header_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Column(expand=True, controls=[self.page_title, self.page_desc]), self.userpfp])
        scrollable_content = ft.Column(
            controls=[header_row, self.profile_card, self.targets_container, ft.Container(content=self.save_button, alignment=ft.Alignment.CENTER, padding=10)],
            scroll=ft.ScrollMode.HIDDEN, expand=True, spacing=20
        )

        self.controls = [ft.Container(content=scrollable_content, expand=True, padding=ft.padding.all(15)), self.nav_bar]
        self.expand = True
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.set_text_size()
        page.on_resize = self.resize

    # --- TDEE CALCULATOR LOGIC ---
    def calculate_tdee(self, e):
        # Validate inputs first
        if not self.age_input.value or not self.weight_input.value or not self.height_input.value:
            self.this_page.overlay.append(ft.SnackBar(content=ft.Text("Please fill out Age, Height, and Weight first!"), bgcolor=ft.Colors.RED, open=True))
            self.this_page.update()
            return

        age = float(self.age_input.value)
        weight = float(self.weight_input.value)
        height = float(self.height_input.value)
        gender = self.gender_input.value
        body_fat = float(self.body_fat_input.value) if self.body_fat_input.value else None

        # 1. Calculate Basal Metabolic Rate (BMR)
        bmr = 0
        if body_fat:
            # Katch-McArdle Formula (More accurate if body fat is known)
            lean_mass = weight * (1 - (body_fat / 100))
            bmr = 370 + (21.6 * lean_mass)
        else:
            # Mifflin-St Jeor Equation (Standard)
            if gender == "Male":
                bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

        # 2. Apply Activity Multiplier
        multipliers = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Very Active": 1.9
        }
        activity = self.activity_input.value
        tdee = bmr * multipliers.get(activity, 1.2)

        # 3. Update the UI Input
        self.cal_goal_input.value = str(int(tdee))

        self.this_page.overlay.append(ft.SnackBar(content=ft.Text(f"TDEE Calculated: {int(tdee)} kcal/day"), bgcolor=ft.Colors.GREEN, open=True))
        self.this_page.update()

    def save_settings(self, e):
        # Save Profile Data
        self.this_page.session.store.set("age", self.age_input.value)
        self.this_page.session.store.set("gender", self.gender_input.value)
        self.this_page.session.store.set("height", self.height_input.value)
        self.this_page.session.store.set("weight", self.weight_input.value)
        self.this_page.session.store.set("body_fat", self.body_fat_input.value)
        self.this_page.session.store.set("activity_level", self.activity_input.value)

        # Save Target Data
        self.this_page.session.store.set("cal_goal", self.cal_goal_input.value)
        self.this_page.session.store.set("water_goal", self.water_goal_input.value)
        self.this_page.session.store.set("protein_goal", self.protein_goal_input.value)
        self.this_page.session.store.set("salts_goal", self.salts_goal_input.value)

        self.this_page.overlay.append(ft.SnackBar(content=ft.Text("Settings successfully saved!", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREEN, open=True))
        self.this_page.update()

    def set_text_size(self):
        self.page_title.size = self.r.w(page_title_size)
        self.page_desc.size = self.r.w(page_desc_size)

    def resize(self, e):
        self.r = Responsive(self.this_page)
        self.set_text_size()
        self.userpfp.resize()
        self.nav_bar.resize()
        self.update()

def main_settings(page: ft.Page):
    return SettingsPage(page)