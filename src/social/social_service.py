"""
Social Service Layer
This file contains the business logic for the social module.
It sits between the UI and the database queries.
"""

from social.social_queries import (
    get_user_by_username,
    get_user_by_id,
    add_friend,
    remove_friend,
    get_friends,
    like_target,
    unlike_target,
    add_comment,
    get_comments,
    get_social_feed,
    get_leaderboard
)

# Basic moderation list for comments.
# This is only a placeholder example for now.
BLACKLIST = {"word1", "word2"}

def contains_blacklisted_word(text):
    """
    Check if text contains banned words.
    """
    lowered = text.lower()
    for word in BLACKLIST:
        if word in lowered:
            return True
    return False


# Friend management
def add_friend_by_username(user_id, friend_username):
    """
    Add friend using username.
    """
    # Basic validation before touching the database
    if not friend_username or not friend_username.strip():
        return "Friend username is required"
    # Remove accidental spaces from input
    cleaned_username = friend_username.strip()
    friend = get_user_by_username(cleaned_username)
    if not friend:
        return "User not found"
    friend_id = friend[0]

    # Prevent users from adding themselves
    if str(friend_id) == str(user_id):
        return "You cannot add yourself"
    result = add_friend(user_id, friend_id)
    if result is True:
        return "Friend added successfully"
    return str(result)


def remove_friend_by_id(user_id, friend_id):
    """
    Remove an existing friend relationship.
    """
    result = remove_friend(user_id, friend_id)
    if result is True:
        return "Friend removed successfully"
    return str(result)


def list_friends(user_id):
    """
    Return friend list formatted for UI.
    """
    rows = get_friends(user_id)
    friends = []
    for row in rows:
        friends.append({
            "id": row[0],
            "username": row[1],
            "email": row[2]
        })
    return friends


# # Social Interaction - like and comments
# def like_item(user_id, target_type, target_id):
#     if target_type not in ("workout", "meal"):
#         return "Invalid target type"
#     result = like_target(user_id, target_type, target_id)
#     if result is True:
#         return "Liked successfully"
#     return str(result)
#
#
# def unlike_item(user_id, target_type, target_id):
#     if target_type not in ("workout", "meal"):
#         return "Invalid target type"
#     result = unlike_target(user_id, target_type, target_id)
#     if result is True:
#         return "Unliked successfully"
#     return str(result)
#
#
# def comment_on_item(user_id, target_type, target_id, content):
#     if target_type not in ("workout", "meal"):
#         return "Invalid target type"
#     if not content or not content.strip():
#         return "Comment cannot be empty"
#     if len(content.strip()) > 300:
#         return "Comment is too long"
#     if contains_blacklisted_word(content):
#         return "Comment contains inappropriate language"
#     result = add_comment(user_id, target_type, target_id, content.strip())
#     if result is True:
#         return "Comment added successfully"
#     return str(result)
#
#
# def list_comments(target_type, target_id):
#     rows = get_comments(target_type, target_id)
#     comments = []
#     for row in rows:
#         comments.append({
#             "comment_id": row[0],
#             "user_id": row[1],
#             "username": row[2],
#             "content": row[3],
#             "created_at": str(row[4])
#         })
#     return comments
#
#
# # Social page data
# def get_social_overview(user_id):
#     """
#     Main function used by the Social UI page.
#     """
#     current_user = get_user_by_id(user_id)
#     full_leaderboard = get_leaderboard(limit=None)
#     top_three = full_leaderboard[:3]
#     activity_rows = get_social_feed(user_id)
#
#     # Default values in case the user is not found
#     current_username = None
#     current_rank = None
#
#     if current_user:
#         current_username = current_user[1]
#
#         # Find the current user's position
#         for index, row in enumerate(full_leaderboard):
#             if row[0] == current_username:
#                 current_rank = index + 1
#                 break
#
#     # Format leaderboard rows for UI
#     leaderboard = []
#     for index, row in enumerate(top_three):
#         leaderboard.append({
#             "rank": index + 1,
#             "username": row[0],
#             "score": row[1]
#         })
#
#     # Format activity feed rows for UI
#     activity = []
#     for row in activity_rows:
#         activity.append({
#             "activity_type": row[0],
#             "username": row[1],
#             "title": row[2],
#             "calories": row[3],
#             "target_id": row[4],
#             "owner_user_id": row[5]
#         })
#
#     return {
#         "rank": {
#             "position": current_rank,
#             "username": current_username
#         },
#         "leaderboard": leaderboard,
#         "activity": activity
#     }
