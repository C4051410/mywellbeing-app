"""
Social Service Layer
This file contains the business logic for the social module.
It sits between the UI and the database queries.
"""
import os

import resend

from settings.settings_services import retrieve_notification_status
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
    delete_comment,
    get_social_feed,
    get_leaderboard, get_interaction_stats
)

# Basic moderation list for comments.
# This is only a placeholder example for now.
BLACKLIST = {"word1", "word2"}
CURRENT_DIR = os.path.dirname(__file__)
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
    if not user_id:
        return "Invalid user_id"
    try:
        if int(user_id) < 0:
            return "Invalid user_id"
    except ValueError:
        return "Invalid user_id"
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
    return "Error adding friend"

def remove_friend_by_id(user_id, friend_id):
    """
    Remove an existing friend relationship.
    """
    if not user_id or not friend_id:
        return "Invalid ids"
    try:
        if int(user_id) < 0 or int(friend_id) < 0:
            return "Invalid ids"
    except ValueError:
        return "Invalid ids"
    result = remove_friend(user_id, friend_id)
    if result is True:
        return "Friend removed successfully"
    return "Error removing friend"

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


# Social Interaction - like and comments
def like_item(user_id, target_type, target_id,owner_id):
    """
    Add a like to one workout activity item.
    """
    if not user_id or not target_type or not target_id or not owner_id:
        return "All fields required"
    try:
        if int(user_id) < 0 or int(owner_id) < 0 or int(target_id) <0:
            return "Invalid ids"
    except ValueError:
        return "Invalid ids"

    if target_type != "workout":
        return "Invalid target type"

    result = like_target(user_id, target_type, target_id)
    if result is True:
        #check if user has notification on
        if retrieve_notification_status(owner_id):
            # try and email the user
            try:
                # will be replaced if full deployment occurred
                email = "m.austoni2@newcastle.ac.uk"
                #get posters username
                username = get_user_by_id(owner_id)[1]
                # get the friends username
                friend = get_user_by_id(user_id)[1]
                # find the directory to the html and retrieve it
                template_path = os.path.join(CURRENT_DIR, "like.html")
                with open(template_path, 'r') as file:
                    content = file.read()
                # Replace the placeholder with the actual variable
                content = content.replace("{{friend}}", friend)
                content = content.replace("{{username}}", username)
                # try and send the email
                resend.Emails.send({
                    "from": "MyWellBeing <reminders@resend.dev>",
                    "to": email,
                    "subject": "New Like",
                    "html": content
                })
            except Exception as e:
                print(e)
        return "Liked successfully"
    return str(result)

def unlike_item(user_id, target_type, target_id):
    """
    Remove a like from one workout activity item.
    """
    if not user_id or not target_type or not target_id:
        return "All fields required"
    try:
        if int(user_id) < 0 or int(target_id) < 0:
            return "Invalid ids"
    except ValueError:
        return "Invalid ids"
    if target_type != "workout":
        return "Invalid target type"

    result = unlike_target(user_id, target_type, target_id)
    if result is True:
        return "Like removed successfully"
    return "Error removing like"


def comment_on_item(user_id, target_type, target_id, content,owner_id):
    """
    Add a comment to one workout activity item.
    """
    if target_type != "workout":
        return "Invalid target type"

    if not content or not content.strip():
        return "Comment cannot be empty"

    cleaned_content = content.strip()

    if len(cleaned_content) > 300:
        return "Comment is too long"

    if contains_blacklisted_word(cleaned_content):
        return "Comment contains inappropriate language"

    result = add_comment(user_id, target_type, target_id, cleaned_content)
    if result is True:
        # check if user has notification on
        if retrieve_notification_status(owner_id):
            #try and send an email to the user
            try:
                #will be replaced if full deployment occurred
                email = "m.austoni2@newcastle.ac.uk"
                #get posters username
                username = get_user_by_id(owner_id)[1]
                #get the friends username and comment
                friend = get_user_by_id(user_id)[1]
                comment = str(content)
                #find the directory to the html and retrieve it
                template_path = os.path.join(CURRENT_DIR, "comment.html")
                with open(template_path, 'r') as file:
                    content = file.read()
                # Replace the placeholder with the actual variable
                content = content.replace("{{friend}}", friend)
                content = content.replace("{{comment}}", comment)
                content = content.replace("{{username}}", username)
                #try and send the email
                resend.Emails.send({
                    "from": "MyWellBeing <reminders@resend.dev>",
                    "to": email,
                    "subject": "New comment",
                    "html": content
                })
            except Exception as e:
                print(e)
        return "Comment added successfully"
    return str(result)

def list_comments(target_type, target_id):
    """
    Return comments formatted for the UI.
    """
    rows = get_comments(target_type, target_id)
    comments = []
    for row in rows:
        comments.append({
            "comment_id": row[0],
            "user_id": row[1],
            "username": row[2],
            "content": row[3],
            "created_at": str(row[4])
        })
    return comments

def delete_comment_item(user_id, comment_id):
    """
    Delete comment item if it belongs to the current user.
    """
    result = delete_comment(comment_id, user_id)
    if result is True:
        return "Comment deleted successfully"
    if result is False:
        return "Comment could not be deleted"
    return str(result)


# Social page data
def get_social_overview(user_id):
    """
    Build the data needed by the Social UI page.
    """
    leaderboard_rows = get_leaderboard(user_id)
    activity_rows = get_social_feed(user_id)
    current_rank = None
    current_points = 0
    leaderboard = []

    # Format leaderboard rows and find the current user's position
    for index, row in enumerate(leaderboard_rows):
        entry = {
            "rank": index + 1,
            "user_id": row[0],
            "username": row[1],
            "points": row[2]
        }
        leaderboard.append(entry)
        if row[0] == user_id:
            current_rank = index + 1
            current_points = row[2]

    #get all ids the activities from activity_rows
    target_ids = [row[4] for row in activity_rows]
    #retrieve all the stats for each activity and produces a dictionary
    stats = get_interaction_stats(user_id, target_ids) if target_ids else {}

    activity = []
    for row in activity_rows:
        #retrieves the target id of activity
        target_id = row[4]
        #retrieves the stats of the post or fallback to default
        post_stats = stats.get(target_id, {"like_count": 0, "liked_by_user": False, "comment_count": 0})
        # adds activity to list
        activity.append({
            "activity_type": row[0],
            "username": row[1],
            "title": row[2],
            "calories": row[3],
            "target_id": target_id,
            "owner_user_id": row[5],
            "duration_seconds": row[6],
            "start_date": row[7],
            "like_count": post_stats["like_count"],
            "liked_by_user": post_stats["liked_by_user"],
            "comment_count": post_stats["comment_count"]
        })
        #return rank, leaderboard top 3 and activities
    return {
        "rank": {
            "position": current_rank,
            "points": current_points
        },
        "leaderboard": leaderboard[:3],
        "activity": activity
    }