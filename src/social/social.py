'''
File for social page - accessible by clicking 'social' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
from datetime import date, timedelta
from social.social_service import (
    add_friend_by_username,
    remove_friend_by_id,
    like_item,
    unlike_item,
    comment_on_item,
    delete_comment_item,
    list_comments,
    list_friends,
    get_social_overview)

#Sizes of all elements on homepage (as a percent of screen)
page_title_size = 0.1
page_subtitle_size = 0.05
page_desc_size = 0.04
leaderboard_v_size = 0.18
standings_v_size = 0.08
activity_v_size = 0.22
container_width_size = 0.92

class SocialPage(ft.Column):
    def __init__(self, page: ft.Page, user_id):
        super().__init__()

        self.this_page = page
        # Store the current user id
        self.user_id = user_id
        self.r = Responsive(page)

        # Load real social data from the service layer.
        self.user_rank = "-"
        self.user_points = 0
        self.leaderboard_data = []
        self.activity_data = []

        self.page_title = ft.Text(
            value="Social",
            size=self.r.w(page_title_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
            )

        self.page_desc = ft.Text(
            value="Track progress with friends",
            size=self.r.w(page_desc_size),
            color=ft.Colors.GREY
                )
        self.userpfp = Userpfp(page)

        self.rank_container = ft.Container(
            gradient=ft.LinearGradient(begin=ft.alignment.Alignment(-1, 0), end=ft.alignment.Alignment(1, 0),
                                       colors=["#F0BE19", "#F3681D"]),
            border_radius=12,
            padding=16,
            expand=True
        )
        self.render_rank_card()

        self.leaderboard_title = ft.Text(
            value="Leaderboard",
            size=self.r.w(page_subtitle_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
            )

        self.first_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
        )

        self.second_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
        )

        self.third_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
        )

        self.activity_title = ft.Text(
             value="Recent Activity",
             size=self.r.w(page_subtitle_size),
             weight=ft.FontWeight.BOLD,
             color=ft.Colors.BLACK
            )

        self.activity_column = ft.Column(spacing=12, expand=True)

        # Input used to add a friend by username.
        self.friend_username_input = ft.TextField(
            hint_text="Enter a username",
            border_radius=8,
            on_submit=self.handle_add_friend
        )

        # Button for adding a friend.
        self.add_friend_card = ft.Container(
            width=self.r.w(container_width_size),
            padding=20,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text("Add a Friend", size=self.r.w(page_desc_size), weight=ft.FontWeight.BOLD),
                    self.friend_username_input,
                ]
            )
        )

        self.friends_title = ft.Text(
            value="Friends",
            size=self.r.w(page_subtitle_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
        )

        self.friends_list_title = ft.Text(
            value="Friends List",
            size=self.r.w(page_subtitle_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
        )

        # Container that will display the friend list.
        self.friends_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            width=self.r.w(container_width_size),
            border_radius=15,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
            padding=20,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Text("No friends loaded yet.")
        )

        self.nav_bar = NavBar(page)
        main_content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            expand=True,
                            controls=[

                                self.page_title,
                                self.page_desc
                            ]
                        ),
                        self.userpfp
                    ]
                ),
            self.rank_container,
            self.leaderboard_title,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[self.first_container]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[self.second_container]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[self.third_container]),
            self.activity_title,
            self.activity_column,
            self.friends_title,
            self.add_friend_card,
            self.friends_list_title,
            self.friends_container
            ],
            expand=True,
            spacing=12,
            scroll=ft.ScrollMode.HIDDEN
        )
        self.controls =[main_content,self.nav_bar]

        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # Add consistent spacing between sections.
        self.spacing = 12
        # Allow the whole page to scroll.
        self.set_widget_size()
        self.load_social_overview()
        self.load_friends()
        page.on_resize = self.resize


    def load_social_overview(self):
        """
        Load rank, leaderboard, and recent activity from the service layer.
        """
        overview = get_social_overview(self.user_id)
        rank_data = overview["rank"]
        self.user_rank = rank_data["position"] if rank_data["position"] is not None else "-"
        self.user_points = rank_data["points"] if rank_data["points"] is not None else 0

        self.leaderboard_data = [
            {"name": item["username"], "points": item["points"]}
            for item in overview["leaderboard"]
        ]

        # Interaction metadata on each activity item
        self.activity_data = [
            {
                "name": item["username"],
                "activity_type": item["activity_type"],
                "title": item["title"],
                "calories": item["calories"],
                "target_id": item["target_id"],
                "duration_seconds": item["duration_seconds"],
                "start_date": item["start_date"],
                "like_count": item["like_count"],
                "liked_by_user": item["liked_by_user"],
                "comment_count": item["comment_count"]
            }
            for item in overview["activity"]
        ]

        # Refresh the rank card after real data is loaded.
        self.render_rank_card()

        self.load_leaderboard()
        self.load_activity()

    # Render the top rank card showing the user's current rank and points
    def render_rank_card(self):
        rank_value = f"#{self.user_rank}" if self.user_rank != "-" else "-"
        points_value = f"{self.user_points} pts"

        self.rank_container.content = ft.Container(
            expand=True,
            padding=10,
            border_radius=12,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(
                        "Your Rank",
                        size=20,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.WHITE70
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=0,
                                controls=[
                                    ft.Text(
                                        rank_value,
                                        size=35,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE70
                                    ),
                                ]
                            ),
                            ft.Column(
                                spacing=0,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        points_value,
                                        size=35,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            )
        )

    # Build a consistent stat card for workout activity detail
    def build_activity_stat_box(self, label, value, bg_color):
        return ft.Container(
            width=self.r.w(0.26),
            height=self.r.h(0.08),
            bgcolor=bg_color,
            border_radius=14,
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                controls=[
                    ft.Text(
                        label,
                        size=8,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        value,
                        size=12,
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
                ]
            )
        )

    # Convert duration in seconds into a simple human-readable string
    def format_duration(self, total_seconds):
        if not total_seconds:
            return "0m"
        total_seconds = int(total_seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    # Format workout date as today, yesterday, or a short date
    def format_activity_date(self, start_date):
        if not start_date:
            return "Recent"

        try:
            activity_day = start_date.date() if hasattr(start_date, "date") else start_date
        except Exception:
            return "Recent"

        today = date.today()
        if activity_day == today:
            return "Today"
        if activity_day == today - timedelta(days=1):
            return "Yesterday"
        return activity_day.strftime("%d %b")

    # Load leaderboard data into the 3 containers
    def load_leaderboard(self):
        if not self.leaderboard_data:
            self.first_container.content = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(" ---", size=16),
                    ft.Text("0 pts", size=14, color=ft.Colors.GREY_700)
                ]
            )
            self.second_container.content = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(" ---", size=16),
                    ft.Text("0 pts", size=14, color=ft.Colors.GREY_700)
                ]
            )
            self.third_container.content = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(" ---", size=16),
                    ft.Text("0 pts", size=14, color=ft.Colors.GREY_700)
                ]
            )
            return

        sorted_users = sorted(
            self.leaderboard_data,
            key=lambda x: x["points"],
            reverse=True
        )
        containers = [self.first_container, self.second_container, self.third_container]
        medals = ["🥇", "🥈", "🥉"]
        for i in range(3):
            if i < len(sorted_users):
                containers[i].content = ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(medals[i], size=25),
                        ft.Text(
                            f"{sorted_users[i]['name']}",
                            size=16,
                            weight=ft.FontWeight.W_500
                        ),
                        ft.Text(
                            f"{sorted_users[i]['points']} pts",
                            size=14,
                            color=ft.Colors.GREY_700
                        )
                    ]
                )
            else:
                containers[i].content = ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            f"{i + 1}. ---",
                            size=16
                        ),
                        ft.Text(
                            "0 pts",
                            size=14,
                            color=ft.Colors.GREY_700
                        )
                    ]
                )

    # Load activity feed
    def load_activity(self):
        self.activity_column.controls.clear()

        # if there is no activity data
        if not self.activity_data:
            self.activity_column.controls.append(
                ft.Container(
                    width=self.r.w(container_width_size),
                    border_radius=15,
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                    padding=20,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.Alignment(-1, 0),
                        end=ft.alignment.Alignment(1, 0),
                        colors=["#8A2BE2", "#4C6EF5"]
                    ),
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text("No activity yet", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text("Your friends haven't posted anything yet.", size=13, color=ft.Colors.WHITE70),
                        ]
                    )
                )
            )
            return

        for item in self.activity_data:
            like_label = "Unlike" if item["liked_by_user"] else "Like"

            gradient_top = ft.Container(
                padding=20,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.Alignment(-1, 0),
                    end=ft.alignment.Alignment(1, 0),
                    colors=["#8A2BE2", "#4C6EF5"]
                ),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    item["name"],
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                            ]
                        ),
                        ft.Text(
                            self.format_activity_date(item["start_date"]),
                            size=12,
                            color=ft.Colors.WHITE70
                        )
                    ]
                )
            )

            white_bottom = ft.Container(
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=16,
                            controls=[
                                self.build_activity_stat_box(
                                    "Workout",
                                    item["title"],
                                    "#F3F4F6"
                                ),
                                self.build_activity_stat_box(
                                    "Duration",
                                    self.format_duration(item["duration_seconds"]),
                                    "#F3F4F6"
                                ),
                                self.build_activity_stat_box(
                                    "Calories",
                                    str(item["calories"]),
                                    "#F3F4F6"
                                ),
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    f"{item['like_count']} likes • {item['comment_count']} comments",
                                    size=12, color=ft.Colors.GREY_600
                                ),
                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.TextButton(
                                            like_label,
                                            on_click=lambda e, activity=item: self.handle_like_action(activity)
                                        ),
                                        ft.TextButton(
                                            "Comments",
                                            on_click=lambda e, activity=item: self.open_comments_dialog(activity)
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            )

            # combine top and white bottom
            self.activity_column.controls.append(
                ft.Container(
                    width=self.r.w(container_width_size),
                    border_radius=15,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                    padding=0,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Column(spacing=0,controls=[gradient_top, white_bottom]
                    )
                )
            )

    # Load the current user's friends and render them into the friends container
    def load_friends(self):
        friends = list_friends(self.user_id)
        friend_controls = []

        # Show an empty state when the user has no friends.
        if not friends:
            self.friends_container.content = ft.Container(
                width=self.r.w(container_width_size),
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Text("No friends added yet.")
            )
            return

        # Build one row per friend so the user can also remove a friend directly.
        for friend in friends:
            friend_controls.append(
                ft.Container(
                    border=ft.Border(
                        bottom=ft.BorderSide(1, ft.Colors.GREY_300)
                    ),
                    padding=ft.padding.symmetric(vertical=4),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=0,
                                controls=[
                                    ft.Text(friend["username"], weight=ft.FontWeight.BOLD),
                                    ft.Text(friend["email"], color=ft.Colors.GREY_600),
                                ]
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Remove friend",
                                on_click=lambda e, friend_id=friend["id"]: self.handle_remove_friend(friend_id)
                            ),
                        ]
                    )
                )
            )

        self.friends_container.content = ft.Column(
            controls=friend_controls,
            spacing=5
        )

    # Show a snackbar message at page level
    def show_snack(self, message):
        self.this_page.show_dialog(
            ft.SnackBar(
                content=ft.Text(message)
            )
        )

    # Add a friend using the entered username, then refresh the list
    def handle_add_friend(self, e):
        entered_username = self.friend_username_input.value

        # Call the service layer instead of querying the database directly in the UI.
        result_message = add_friend_by_username(self.user_id, entered_username)
        # Show feedback to the user.
        self.show_snack(result_message)
        # Clear the input after submission for a cleaner user experience.
        self.friend_username_input.value = ""
        # Reload both the friend list and the social overview so the page reflects the new friendship immediately.
        self.load_friends()
        self.load_social_overview()

        self.this_page.update()
        self.update()

    # Remove a friend, then refresh the list
    def handle_remove_friend(self, friend_id):
        result_message = remove_friend_by_id(self.user_id, friend_id)
        # Show feedback to the user after the removal attempt.
        self.show_snack(result_message)

        # Refresh both the friend list and the overview
        self.load_friends()
        self.load_social_overview()

        self.this_page.update()
        self.update()

    # Like or unlike one activity item, then refresh the social overview
    def handle_like_action(self, activity_item):
        if activity_item["liked_by_user"]:
            result_message = unlike_item(
                self.user_id,
                activity_item["activity_type"],
                activity_item["target_id"]
            )
        else:
            result_message = like_item(
                self.user_id,
                activity_item["activity_type"],
                activity_item["target_id"]
            )

        self.show_snack(result_message)
        # Refresh the overview so like counts and button state update immediately.
        self.load_social_overview()

        self.this_page.update()
        self.update()

    # Open a dialog that shows comments for one workout activity and to add a new comments
    def open_comments_dialog(self, activity_item):
        comments = list_comments(activity_item["activity_type"], activity_item["target_id"])

        comment_controls = []
        if not comments:
            comment_controls.append(ft.Text("No comments yet."))
        else:
            for comment in comments:
                comment_row_controls = [
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(comment["username"], weight=ft.FontWeight.BOLD),
                            ft.Text(comment["content"]),
                        ]
                    )
                ]

                # Only show the delete button for comments created by the current user.
                if comment["user_id"] == self.user_id:
                    comment_row_controls.append(
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete comment",
                            on_click=lambda e,
                                            comment_id=comment["comment_id"],
                                            activity=activity_item: self.handle_delete_comment(activity, comment_id)
                        )
                    )

                comment_controls.append(
                    ft.Container(
                        padding=ft.padding.symmetric(vertical=4),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=comment_row_controls
                        )
                    )
                )

        comment_input = ft.TextField(
            hint_text="Write a comment..."
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Comments"),
            content=ft.Column(
                controls=comment_controls + [ft.Divider(), comment_input],
                tight=True,
                scroll=ft.ScrollMode.AUTO,
                height=300
            ),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda e: self.close_dialog()
                ),
                ft.ElevatedButton(
                    "Post",
                    on_click=lambda e: self.submit_comment(
                        activity_item["activity_type"],
                        activity_item["target_id"],
                        comment_input.value
                    )
                )
            ]
        )

        # Use Flet's dialog api so the dialog can be opened and removed reliably.
        self.this_page.show_dialog(dialog)

    # Submit a comment, close the dialog and refresh the social overview
    def submit_comment(self, target_type, target_id, content):
        result_message = comment_on_item(self.user_id, target_type, target_id, content)

        # Close the current dialog first.
        self.this_page.pop_dialog()

        # Refresh the overview so comment counts update after posting.
        self.load_social_overview()

        self.this_page.update()
        self.update()
        self.show_snack(result_message)

    # Delete one comment, close the dialog and refresh the social overview.
    def handle_delete_comment(self, activity_item, comment_id):
        result_message = delete_comment_item(self.user_id, comment_id)

        # Close the current dialog first.
        self.this_page.pop_dialog()

        # Refresh the overview so the comment count updates immediately.
        self.load_social_overview()

        self.this_page.update()
        self.update()
        self.show_snack(result_message)

    # Close comments dialog
    def close_dialog(self):
        self.this_page.pop_dialog()

    #Set size of all text on screen
    def set_text_size(self):
        self.page_title.size = self.r.w(page_title_size)
        self.page_desc.size = self.r.w(page_desc_size)
        self.activity_title.size = self.r.w(page_desc_size)
        self.leaderboard_title.size = self.r.w(page_desc_size)


    #Set width and height of all widgets on the screen
    def set_widget_size(self):
        # Give list sections enough height
        self.rank_container.height = self.r.h(leaderboard_v_size)
        self.first_container.height = self.r.h(0.10)
        self.second_container.height = self.r.h(0.10)
        self.third_container.height = self.r.h(0.10)
        #self.friends_container.height = self.r.h(activity_v_size)

        # Keep section widths consistent so cards line up cleanly
        self.rank_container.width = self.r.w(container_width_size)
        self.first_container.width = self.r.w(container_width_size)
        self.second_container.width = self.r.w(container_width_size)
        self.third_container.width = self.r.w(container_width_size)
        self.friends_container.width = self.r.w(container_width_size)
        self.friend_username_input.width = self.r.w(container_width_size)
        self.add_friend_card.width = self.r.w(container_width_size)
    def resize(self, e):
        self.r = Responsive(self.this_page)

        #Resize all text on the page
        self.set_text_size()
        self.set_widget_size()
        self.load_activity()
        self.userpfp.resize()
        self.nav_bar.resize()

        self.update()

def main_social(page: ft.Page, user_id):
    social_page = SocialPage(page, user_id)

    return social_page