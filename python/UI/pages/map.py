import os
import csv
import math
from datetime import datetime
import flet as ft
import flet_map as ftm
from flet_geolocator import Geolocator


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

    # --- UI Elements ---
    distance_value = ft.Text(value="0.00", size=48, weight=ft.FontWeight.BOLD)
    distance_label = ft.Text(value="KILOMETERS", size=12, color=ft.Colors.GREY_700, weight=ft.FontWeight.BOLD)

    marker_layer = ftm.MarkerLayer(markers=[])
    polyline_layer = ftm.PolylineLayer(
        polylines=[ftm.PolylineMarker(coordinates=[], color=ft.Colors.DEEP_ORANGE, stroke_width=4)]
    )

    map_ctrl = ftm.Map(
        expand=True,
        initial_center=ftm.MapLatitudeLongitude(54.9783, -1.6178),  # Newcastle
        initial_zoom=14,
        layers=[
            ftm.TileLayer(url_template="https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png"),
            polyline_layer,
            marker_layer,
        ]
    )

    # --- Tracking Logic ---
    def on_position_change(e):
        nonlocal total_dist, is_tracking

        # Safely get coordinates depending on if it's real GPS or our mock desktop event
        lat = e.latitude if hasattr(e, 'latitude') else e.position.latitude
        lon = e.longitude if hasattr(e, 'longitude') else e.position.longitude

        new_loc = ftm.MapLatitudeLongitude(lat, lon)

        # Always update your current location marker
        marker_layer.markers.clear()
        marker_layer.markers.append(
            ftm.Marker(content=ft.Icon(ft.Icons.MY_LOCATION, color=ft.Colors.BLUE, size=30), coordinates=new_loc)
        )
        map_ctrl.center = new_loc

        # Only accumulate distance and draw the line if we hit "START" or "RESUME"
        if is_tracking:
            if path_points:
                prev = path_points[-1]
                total_dist += calculate_distance(prev.latitude, prev.longitude, new_loc.latitude, new_loc.longitude)

            path_points.append(new_loc)
            distance_value.value = f"{total_dist:.2f}"

            if len(path_points) > 1:
                polyline_layer.polylines[0].coordinates = list(path_points)

        page.update()

    # ==========================================
    # PLATFORM CHECK: Prevent Red Box on Desktop
    # ==========================================
    gl = None
    if page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS] or page.web:
        if not any(isinstance(c, Geolocator) for c in page.overlay):
            gl = Geolocator(on_position_change=on_position_change)
            page.overlay.append(gl)
        else:
            gl = next(c for c in page.overlay if isinstance(c, Geolocator))
            gl.on_position_change = on_position_change

    # --- Navigation Back Button ---
    async def go_back(e):
        await page.push_route("/activities")

    # --- Button Handlers ---
    async def start_tracking(e):
        nonlocal is_tracking
        is_tracking = True

        # Update UI: Hide Start, Show Pause
        start_btn.visible = False
        tracking_row.visible = True
        paused_row.visible = False
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
            print("Desktop Mode: GPS Disabled. Placing dummy marker.")

            class MockEvent:
                latitude = 54.9783
                longitude = -1.6178

            on_position_change(MockEvent())

    def pause_tracking(e):
        nonlocal is_tracking
        is_tracking = False

        # Update UI: Hide Pause, Show Resume & Finish
        tracking_row.visible = False
        paused_row.visible = True
        page.update()

    def resume_tracking(e):
        nonlocal is_tracking
        is_tracking = True

        # Update UI: Hide Resume & Finish, Show Pause
        paused_row.visible = False
        tracking_row.visible = True
        page.update()

    def finish_and_save(e):
        nonlocal is_tracking, total_dist
        is_tracking = False

        final_distance = total_dist

        # --- DATA SAVING LOGIC ---
        file_path = "activities_history.csv"
        file_exists = os.path.isfile(file_path)

        # Open the CSV file in 'a' (append) mode
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write headers if the file is brand new
            if not file_exists:
                writer.writerow(["Date", "Distance_KM"])

            # Get the current date and time
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Save the new run data
            writer.writerow([current_date, round(final_distance, 2)])

        print(f"ACTIVITY SAVED to CSV! Total Distance: {final_distance:.2f} km")

        # Show a success pop-up to the user
        page.overlay.append(
            ft.SnackBar(
                content=ft.Text(f"Activity Saved! Distance: {final_distance:.2f} km", weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.GREEN, open=True)
        )

        # Reset the map and data for the next run
        path_points.clear()
        total_dist = 0.0
        distance_value.value = "0.00"
        if polyline_layer.polylines:
            polyline_layer.polylines[0].coordinates.clear()

        # Update UI: Reset to Start button
        paused_row.visible = False
        tracking_row.visible = False
        start_btn.visible = True
        page.update()

    # --- UI Assembly ---
    top_back_button = ft.Container(
        content=ft.FloatingActionButton(
            icon=ft.Icons.ARROW_BACK,
            bgcolor=ft.Colors.WHITE,
            on_click=go_back,
            mini=True
        ),
        alignment=ft.Alignment.TOP_LEFT,
        padding=ft.padding.only(top=40, left=20)
    )

    # 1. The Start Button
    start_btn = ft.FloatingActionButton(
        content=ft.Text("START", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        icon=ft.Icons.FIBER_MANUAL_RECORD, bgcolor=ft.Colors.DEEP_ORANGE, width=150, on_click=start_tracking
    )

    # 2. The Tracking Row (Only shows PAUSE)
    pause_btn = ft.FloatingActionButton(
        content=ft.Text("PAUSE", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        icon=ft.Icons.PAUSE, bgcolor=ft.Colors.GREY_800, width=150, on_click=pause_tracking
    )
    tracking_row = ft.Row(controls=[pause_btn], alignment=ft.MainAxisAlignment.CENTER, visible=False)

    # 3. The Paused Row (Shows RESUME and FINISH)
    resume_btn = ft.FloatingActionButton(
        content=ft.Text("RESUME", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        bgcolor=ft.Colors.DEEP_ORANGE, width=140, on_click=resume_tracking
    )
    finish_btn = ft.FloatingActionButton(
        content=ft.Text("FINISH", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        bgcolor=ft.Colors.GREEN, width=140, on_click=finish_and_save
    )
    paused_row = ft.Row(controls=[resume_btn, finish_btn], alignment=ft.MainAxisAlignment.CENTER, visible=False,
                        spacing=15)

    map_dashboard = ft.Container(
        content=ft.Column(
            controls=[
                ft.Column([distance_label, distance_value], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                          spacing=0),
                start_btn,
                tracking_row,
                paused_row
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.BorderRadius(top_left=30, top_right=30, bottom_left=0, bottom_right=0),
        padding=30,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.BLACK26)
    )

    return ft.Stack(
        controls=[
            map_ctrl,
            top_back_button,
            ft.Container(content=map_dashboard, alignment=ft.Alignment.BOTTOM_CENTER, bottom=0, left=0, right=0)
        ],
        expand=True
    )