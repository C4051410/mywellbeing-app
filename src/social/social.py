'''
File for social page - accessible by clicking 'social' on nav bar
'''

import flet as ft

from components.userpfp import Userpfp
from components.bottom_nav import NavBar
from components.responsive import Responsive
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
page_desc_size = 0.03
leaderboard_v_size = 0.18
standings_v_size = 0.08
activity_v_size=0.18

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

        self.rank_container = ft.Container(bgcolor=ft.Colors.ORANGE_200, border_radius=10, padding=20,
                                                   content=ft.Row(
                                                                  controls=[
                                                                      ft.Text(f"Rank #{self.user_rank}", size=20,
                                                                              weight=ft.FontWeight.BOLD),
                                                                      ft.Text(f"{self.user_points} pts", size=18)]))
        self.leaderboard_title = ft.Text(
            value="Leaderboard",
            size=self.r.w(page_desc_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
            )

        self.first_container = ft.Container(
             border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
             border_radius=8,
             padding=10
             )

        self.second_container = ft.Container(
             border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
             border_radius=8,
             padding=10
             )

        self.third_container = ft.Container(
             border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
             border_radius=8,
             padding=10
             )

        self.activity_title = ft.Text(
             value="Recent Activity",
             size=self.r.w(page_desc_size),
             weight=ft.FontWeight.BOLD,
             color=ft.Colors.BLACK
            )

        self.activity_container = ft.Container(
             border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
             border_radius=8,
             padding=10
            )

        # Input used to add a friend by username.
        self.friend_username_input = ft.TextField(
            label="Friend username",
            hint_text="Enter a username",
            border_radius=8
        )

        # Button for adding a friend.
        self.add_friend_button = ft.ElevatedButton(
            content = ft.Text("Add Friend"),
            on_click = self.handle_add_friend
        )

        self.friends_title = ft.Text(
            value="Friends",
            size=self.r.w(page_desc_size),
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
        )

        # Container that will display the friend list.
        self.friends_container = ft.Container(
            border=ft.Border.all(width=2, color=ft.Colors.GREY_400),
            border_radius=8,
            padding=10,
            content=ft.Text("No friends loaded yet.")
        )

        self.nav_bar = NavBar(page)
        main_content = ft.Column(controls = [
            ft.Row(
                controls=[
                    ft.Column(
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
            self.first_container,
            self.second_container,
            self.third_container,
            self.activity_title,
            self.activity_container,
            self.friends_title,
            self.friend_username_input,
            self.add_friend_button,
            self.friends_container],expand=True, scroll=ft.ScrollMode.HIDDEN)
        self.controls =[main_content,self.nav_bar]

        self.expand = True
        # Stretch controls horizontally so containers line up more naturally.
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
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
                "activity": f"{item['activity_type']}: {item['title']} ({item['calories']} cal)",
                "time": "Recent",
                "activity_type": item["activity_type"],
                "target_id": item["target_id"],
                "like_count": item["like_count"],
                "liked_by_user": item["liked_by_user"],
                "comment_count": item["comment_count"]
            }
            for item in overview["activity"]
        ]

        # Refresh the rank card after real data is loaded.
        self.rank_container.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    f"Rank #{self.user_rank}",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(f"{self.user_points} pts", size=18)
            ]
        )

        self.load_leaderboard()
        self.load_activity()

    # Load leaderboard data into the 3 containers
    def load_leaderboard(self):
        if not self.leaderboard_data:
            self.first_container.content = ft.Text("No leaderboard data yet.")
            self.second_container.content = ft.Text("2. ___")
            self.third_container.content = ft.Text("3. ___")
            return

        sorted_users = sorted(
            self.leaderboard_data,
            key=lambda x: x["points"],
            reverse=True
        )
        containers = [self.first_container, self.second_container, self.third_container]
        for i in range(3):
            if i < len(sorted_users):
                containers[i].content = ft.Text(
                    f"{i + 1}. {sorted_users[i]['name']} - {sorted_users[i]['points']} pts"
                )
            else:
                containers[i].content = ft.Text(f"{i + 1}. ---")



    # Load activity feed into activity container
    def load_activity(self):
        activity_controls = []

        if not self.activity_data:
            self.activity_container.content = ft.Container(
                alignment=ft.Alignment.CENTER,
                content=ft.Text("No recent friend activity data yet.")
            )
            return

        for item in self.activity_data:
            like_label = "Unlike" if item["liked_by_user"] else "Like"

            activity_controls.append(
                ft.Container(
                    border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
                    padding=ft.padding.symmetric(vertical=6),
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.ListTile(
                                title=ft.Text(item["name"]),
                                subtitle=ft.Text(item["activity"]),
                                trailing=ft.Text(item["time"])
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"{item['like_count']} likes • {item['comment_count']} comments"
                                    ),
                                    ft.Row(
                                        spacing=6,
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
            )

        # Keep the activity list scrollable inside its container.
        self.activity_container.content = ft.Column(
            controls=activity_controls,
            spacing=5,
        )

    # Load the current user's friends and render them into the friends container
    def load_friends(self):
        friends = list_friends(self.user_id)
        friend_controls = []

        # Show an empty state when the user has no friends.
        if not friends:
            self.friends_container.content = ft.Container(
                alignment=ft.Alignment.CENTER,
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
            spacing=5,
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
                comment_controls.append(
                    ft.Container(
                        padding=ft.padding.symmetric(vertical=4),
                        content=ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(comment["username"], weight=ft.FontWeight.BOLD),
                                ft.Text(comment["content"]),
                            ]
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
                    on_click=lambda e: self.close_dialog(dialog)
                ),
                ft.ElevatedButton(
                    "Post",
                    on_click=lambda e: self.submit_comment(
                        dialog,
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
    def submit_comment(self, dialog, target_type, target_id, content):
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
    def close_dialog(self, dialog):
        self.this_page.pop_dialog()

    #Set size of all text on screen
    def set_text_size(self):
        self.page_title.size = self.r.w(page_title_size)
        self.page_desc.size = self.r.w(page_desc_size)
        self.activity_title.size = self.r.w(page_desc_size)
        self.leaderboard_title.size = self.r.w(page_desc_size)


    #Set width and height of all widgets on the screen
    def set_widget_size(self):
        #leaderboard widget - rectangle
        self.rank_container.height = self.r.h(leaderboard_v_size)
        #Standings widgets - rectangle
        self.first_container.height = self.r.h(standings_v_size)
        self.second_container.height = self.r.h(standings_v_size)
        self.third_container.height = self.r.h(standings_v_size)
        #Friends activity widget - rectangle
        self.activity_container.height = self.r.h(activity_v_size)
        # Friends list widget
        self.friends_container.height = self.r.h(activity_v_size)

    def resize(self, e):
        self.r = Responsive(self.this_page)

        #Resize all text on the page
        self.set_text_size()
        self.set_widget_size()

        self.userpfp.resize()
        self.nav_bar.resize()

        self.update()

def main_social(page: ft.Page, user_id):
    social_page = SocialPage(page, user_id)

    return social_page