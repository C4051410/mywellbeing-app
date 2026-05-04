import pytest
from unittest.mock import patch, MagicMock
from social.social_service import (
    add_friend_by_username,
    comment_on_item,
    get_social_overview,
    delete_comment_item,
    list_friends,
    list_comments,
    like_item,
    unlike_item
)


class TestFriendshipLogic:
    """
    UNIT TESTS: Friendship Management
    Ensures users cannot add themselves and that usernames are cleaned.
    """

    @patch("social.social_service.get_user_by_username")
    @patch("social.social_service.add_friend")
    def test_add_friend(self,mock_add,mock_get_user):
        #creates valid friend return
        mock_get_user.return_value = (2,"MyFriend","My@Friend.com")
        #set add return to True
        mock_add.return_value = True
        #try and add valid friend
        result = add_friend_by_username(1,"MyFriend")
        assert result == "Friend added successfully"
        #check it was called with ids 1 and 2
        mock_add.assert_called_once_with(1,2)

    @patch("social.social_service.get_user_by_username")
    @patch("social.social_service.add_friend")
    def test_add_friend_self_error(self, mock_add, mock_get_user):
        #mock finding a user that has the SAME ID as the requester
        mock_get_user.return_value = (1, "MySelf", "me@test.com")
        #try and add friend with SAME ID
        result = add_friend_by_username(1, "MySelf")
        assert result == "You cannot add yourself"
        #check it wasn't called
        mock_add.assert_not_called()

    @patch("social.social_service.get_user_by_username")
    def test_add_friend_not_found(self, mock_get_user):
        #check for when friend isnt found
        mock_get_user.return_value = None
        result = add_friend_by_username(1, "GhostUser")
        assert result == "User not found"

    @patch("social.social_service.get_friends")
    def test_list_friends_transformation(self, mock_get):
        #mocking raw database rows (tuples)
        mock_get.return_value = [(10, "Buddy", "buddy@test.com"), (11, "Pal", "pal@test.com")]

        friends = list_friends(1)

        assert len(friends) == 2
        assert friends[0]["username"] == "Buddy"
        assert friends[1]["id"] == 11
        assert isinstance(friends[0], dict)



class TestSocialInteractionLogic:
    """
    UNIT TESTS: Social Interactions (Likes/Comments)
    Validates content moderation, length constraints, and ownership.
    """

    @patch("social.social_service.add_comment")
    def test_add_comment(self,mock_add_comment):
        mock_add_comment.return_value = True
        result = comment_on_item(2,"workout",101,"Valid Comment")
        assert result == "Comment added successfully"

    def test_comment_blacklist_moderation(self):
        # 'word1' is in the BLACKLIST
        result = comment_on_item(1, "workout", 101, "This comment has word1")
        assert result == "Comment contains inappropriate language"

    def test_comment_length_validation(self):
        #creates comment longer then the 300 character limit
        long_comment = "a" * 301
        result = comment_on_item(1, "workout", 101, long_comment)
        assert result == "Comment is too long"

    def test_comment_empty_validation(self):
        #check empty comment cant be added
        result = comment_on_item(1, "workout", 101, "   ")
        assert result == "Comment cannot be empty"

    @patch("social.social_service.delete_comment")
    def test_delete_comment_ownership(self, mock_delete):
        #if the query returns False, it means user_id didn't match owner_id
        mock_delete.return_value = False
        result = delete_comment_item(1, 500)
        assert result == "Comment could not be deleted"

    @patch("social.social_service.get_comments")
    def test_list_comments_transformation(self, mock_get_comm):
        #mocking DB row: (id, user_id, username, content, created_at)
        mock_get_comm.return_value = [(1, 99, "UserA", "Great job!", "2026-04-29")]

        comments = list_comments("workout", 500)

        assert comments[0]["content"] == "Great job!"
        assert comments[0]["username"] == "UserA"
        # Checking that the service converted the date to a string as intended
        assert isinstance(comments[0]["created_at"], str)

    @patch("social.social_service.like_target")
    def test_like_item(self, mock_like):
        #test valid like
        mock_like.return_value = True
        result = like_item(1, "workout", 10)
        assert result == "Liked successfully"
        mock_like.assert_called_once()

    @patch("social.social_service.like_target")
    def test_like_item_invalid_type(self, mock_like):
        #check invalid profile type doesnt work
        result = like_item(1, "profile", 10)
        assert result == "Invalid target type"
        mock_like.assert_not_called()

    @patch("social.social_service.unlike_target")
    def test_unlike_item_success(self, mock_unlike):
        mock_unlike.return_value = True
        #test valid unlike
        result = unlike_item(1, "workout", 50)
        assert result == "Like removed successfully"
        mock_unlike.assert_called_once_with(1, "workout", 50)


class TestSocialFeedLogic:
    """
    UNIT TESTS: Feed and Leaderboard
    Ensures data is correctly ranked and truncated for the UI.
    """

    @patch("social.social_service.get_leaderboard")
    @patch("social.social_service.get_social_feed")
    @patch("social.social_service.get_interaction_stats")
    def test_get_social_overview_ranking(self, mock_stats,mock_feed,mock_leader):
        #setup Leaderboard: User 1 is in 2nd place
        mock_leader.return_value = [
            (2, "User Two", 1000),
            (1, "User One", 500),
            (3, "User Three", 250),
            (4, "User Four", 100)
        ]
        #keep feed empty for this test
        mock_feed.return_value = []
        mock_stats.return_value = {}

        data = get_social_overview(1)

        #verify rank calculation
        assert data["rank"]["position"] == 2
        assert data["rank"]["points"] == 500
        #verify leaderboard is sliced to top 3
        assert len(data["leaderboard"]) == 3