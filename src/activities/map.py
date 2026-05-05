import math
import time
import asyncio
from datetime import datetime
import flet as ft
import flet_map as ftm
from flet_geolocator import Geolocator
from plyer import notification
from activities.activities_services import save_activity


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(
        dlon / 2) ** 2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def main_map(page: ft.Page):
    # --- State Variables ---
    path_points = []
    total_dist = 0.0
    is_tracking = False

    # Timer & Location variables
    activity_start_time = 0.0
    total_time_seconds = 0.0
    current_gps_loc = ftm.MapLatitudeLongitude(54.9783, -1.6178)  # Default fallback

    # --- UI Elements ---
    distance_value = ft.Text(value="0.00", size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
    distance_label = ft.Text(value="KILOMETERS", size=12, color=ft.Colors.GREY_700, weight=ft.FontWeight.BOLD)

    # Live Stopwatch & Speed Elements
    timer_value = ft.Text(value="00:00:00", size=24, weight=ft.FontWeight.BOLD)
    speed_value = ft.Text(value="0.0 km/h", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600)

    # Activity Selector
    activity_dropdown = ft.Dropdown(
        value="Run",
        options=[
            ft.dropdown.Option("Walk"),
            ft.dropdown.Option("Run"),
            ft.dropdown.Option("Cycle"),
        ],
        width=150,
        height=45,
        content_padding=10,
        text_size=14,
        border_radius=10
    )

    marker_layer = ftm.MarkerLayer(markers=[])
    polyline_layer = ftm.PolylineLayer(
        polylines=[ftm.PolylineMarker(coordinates=[], color=ft.Colors.BLUE, stroke_width=4)]
    )

    map_ctrl = ftm.Map(
        expand=True,
        initial_center=current_gps_loc,
        initial_zoom=14,
        layers=[
            ftm.TileLayer(url_template="https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png"),
            polyline_layer,
            marker_layer,
        ]
    )

    # --- CORE LOGIC ---
    def on_position_change(e):
        nonlocal total_dist, is_tracking, current_gps_loc
        lat = e.latitude if hasattr(e, 'latitude') else e.position.latitude
        lon = e.longitude if hasattr(e, 'longitude') else e.position.longitude

        current_gps_loc = ftm.MapLatitudeLongitude(lat, lon)
        marker_layer.markers.clear()
        marker_layer.markers.append(
            ftm.Marker(content=ft.Icon(ft.Icons.MY_LOCATION, color=ft.Colors.BLUE, size=30),
                       coordinates=current_gps_loc))

        if is_tracking:
            page.run_task(map_ctrl.move_to,get_offset_location(current_gps_loc))

            if path_points:
                prev = path_points[-1]
                total_dist += calculate_distance(prev.latitude, prev.longitude, current_gps_loc.latitude,
                                                 current_gps_loc.longitude)

            path_points.append(current_gps_loc)
            distance_value.value = f"{total_dist:.2f}"

            if len(path_points) > 1:
                polyline_layer.polylines[0].coordinates = list(path_points)
        page.update()
    #create geolocator to update position
    gl = Geolocator(
        on_position_change=on_position_change,
        on_error=lambda e: print(f"GPS Error: {e.data}")
    )

    # Background task to tick the stopwatch every second!
    async def run_stopwatch():
        while page.route in ["/map", "/map/"]:
            if is_tracking:
                elapsed = total_time_seconds + (time.time() - activity_start_time)

                h = int(elapsed // 3600)
                m = int((elapsed % 3600) // 60)
                s = int(elapsed % 60)
                timer_value.value = f"{h:02d}:{m:02d}:{s:02d}"

                if elapsed > 0:
                    speed = total_dist / (elapsed / 3600)
                    speed_value.value = f"{speed:.1f} km/h"

                try:
                    page.update()
                except Exception:
                    pass
            await asyncio.sleep(1)

    page.run_task(run_stopwatch)

    # --- BUTTON HANDLERS ---
    def go_back(e):
        page.go("/activities")

    def get_offset_location(loc, offset=-0.006):
        """Return a point slightly north so the marker appears above the dashboard"""
        return ftm.MapLatitudeLongitude(loc.latitude + offset, loc.longitude)

    async def recenter_map(e):
        await map_ctrl.move_to(get_offset_location(current_gps_loc), zoom=14)
        page.update()

    async def start_tracking(e):
        nonlocal is_tracking, activity_start_time
        is_tracking = True
        activity_start_time = time.time()

        start_btn.visible = False
        tracking_row.visible = True
        paused_row.visible = False
        activity_dropdown.disabled = True
        page.update()

        if gl is not None:
            status = await gl.get_permission_status()
            if "denied" in str(status).lower():
                await gl.request_permission()
            try:
                await gl.get_current_position()
            except Exception as err:
                print(f"GPS Searching: {err}")
        else:
            class MockEvent:
                latitude = 54.9783
                longitude = -1.6178

            on_position_change(MockEvent())

    def pause_tracking(e):
        nonlocal is_tracking, total_time_seconds
        is_tracking = False
        total_time_seconds += time.time() - activity_start_time

        tracking_row.visible = False
        paused_row.visible = True
        page.update()

    def resume_tracking(e):
        nonlocal is_tracking, activity_start_time
        is_tracking = True
        activity_start_time = time.time()

        paused_row.visible = False
        tracking_row.visible = True
        page.update()

    def finish_and_save(e):
        nonlocal is_tracking, total_dist, total_time_seconds, activity_start_time

        if is_tracking:
            total_time_seconds += time.time() - activity_start_time
            is_tracking = False

        final_distance = total_dist
        final_seconds = int(total_time_seconds)
        selected_activity = activity_dropdown.value

        save_activity(
            user_id=page.user_id,
            activity_type=selected_activity,
            distance_km=round(final_distance, 2),
            duration_seconds=final_seconds,
            start_date=datetime.now()
        )

        page.overlay.append(ft.SnackBar(
            content=ft.Text(f"{selected_activity} Saved! Dist: {final_distance:.2f}km | Time: {final_seconds}s",
                            weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.GREEN,
            open=True
        ))

        path_points.clear()
        total_dist = 0.0
        total_time_seconds = 0.0
        distance_value.value = "0.00"
        timer_value.value = "00:00:00"
        speed_value.value = "0.0 km/h"
        activity_dropdown.disabled = False

        if polyline_layer.polylines:
            polyline_layer.polylines[0].coordinates.clear()

        paused_row.visible = False
        tracking_row.visible = False
        start_btn.visible = True

        page.go("/activities")

    # --- UI LAYOUT ---

    top_back_button = ft.Container(
        content=ft.FloatingActionButton(
            content=ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            on_click=go_back,
            mini=True
        ),
        top=40,
        left=20
    )

    recenter_button = ft.Container(
        content=ft.FloatingActionButton(
            content=ft.Icon(ft.Icons.MY_LOCATION, color=ft.Colors.BLUE_600),
            bgcolor=ft.Colors.WHITE,
            on_click=recenter_map,
            mini=True
        ),
        top=40,
        right=20
    )

    start_btn = ft.FloatingActionButton(content=ft.Text("START", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        icon=ft.Icons.FIBER_MANUAL_RECORD, bgcolor=ft.Colors.BLUE, width=150,
                                        on_click=start_tracking)
    pause_btn = ft.FloatingActionButton(content=ft.Text("PAUSE", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        icon=ft.Icons.PAUSE, bgcolor=ft.Colors.GREY_800, width=150,
                                        on_click=pause_tracking)
    tracking_row = ft.Row(controls=[pause_btn], alignment=ft.MainAxisAlignment.CENTER, visible=False)
    resume_btn = ft.FloatingActionButton(content=ft.Text("RESUME", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                         bgcolor=ft.Colors.GREEN, width=140, on_click=resume_tracking)
    finish_btn = ft.FloatingActionButton(content=ft.Text("FINISH", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                         bgcolor=ft.Colors.RED, width=140, on_click=finish_and_save)
    paused_row = ft.Row(controls=[resume_btn, finish_btn], alignment=ft.MainAxisAlignment.CENTER, visible=False,
                        spacing=15)

    map_dashboard = ft.Container(
        content=ft.Column([
            ft.Row([activity_dropdown], alignment=ft.MainAxisAlignment.CENTER),
            ft.Column([distance_label, distance_value], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),

            ft.Row([
                ft.Column([ft.Icon(ft.Icons.TIMER, color=ft.Colors.GREY_500), timer_value],
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_300),
                ft.Column([ft.Icon(ft.Icons.SPEED, color=ft.Colors.BLUE_500), speed_value],
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),

            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            start_btn, tracking_row, paused_row
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.BorderRadius(top_left=30, top_right=30, bottom_left=0, bottom_right=0), padding=30,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK26)
    )

    # FIX: Pinned the map container to all 4 corners so it never collapses!
    return ft.Stack(
        controls=[
            ft.Container(content=map_ctrl, top=0, bottom=0, left=0, right=0),
            top_back_button,
            recenter_button,
            ft.Container(content=map_dashboard, bottom=0, left=0, right=0)
        ],
        expand=True
    )