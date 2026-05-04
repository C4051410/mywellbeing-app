from unittest.mock import patch

from moderator import moderator_services
from moderator.moderator_services import check_mod, retrieve_posts_moderator, remove_posts_moderator


#mocks queries to avoid using actual db
@patch('moderator.moderator_services.get_mod')
#tests check_mod
class TestCheckModerator():
    #test valid result
    def test_valid_check(self, mock_get_mod):
        mock_get_mod.return_value = "moderator"
        success = check_mod(1)
        assert success == True
    #tests missing fields return false
    def test_missing_fields(self,mock_get_mod):
        mock_get_mod.return_value = "moderator"
        success = check_mod(None)
        assert success == False
    # test incorrect roles returns false
    def test_incorrect_role(self,mock_get_mod):
        mock_get_mod.return_value = "user"
        success = check_mod(1)
        assert success == False
        mock_get_mod.return_value = "admin"
        success = check_mod(1)
        assert success == False
    #test invalid ids return false
    def test_invalid_id(self,mock_get_mod):
        mock_get_mod.return_value = "moderator"
        success = check_mod(-1)
        assert success == False
        success = check_mod("Invalid ID")
        assert success == False

@patch('moderator.moderator_services.get_posts_moderators')
#test retrieve_posts_moderator
class TestRetrievePosts():
    #creates fake response to function
    rows = [
        ("Pizza","PizzaKing1",2),
        ("Pushups","AbsQueen",3),
        ("Great Run","CommentJack",4)
    ]
    #tests rows are properly returned
    def test_valid_retrieve(self, mock_get_posts_moderators):
        mock_get_posts_moderators.return_value = self.rows
        returned_rows = retrieve_posts_moderator("")
        assert returned_rows[0] == ("Pizza","PizzaKing1",2)
        assert returned_rows[1] == ("Pushups","AbsQueen",3)
        assert returned_rows[2] == ("Great Run","CommentJack",4)
        assert len(returned_rows) == 3

    #tests empty row returns an empty row
    def test_empty_retrieve(self, mock_get_posts_moderators):
        mock_get_posts_moderators.return_value = []
        returned_rows = retrieve_posts_moderator("")
        assert returned_rows == []
        assert len(returned_rows) == 0

@patch('moderator.moderator_services.delete_posts_moderator')
#tests remove_posts_moderator
class TestRemovePosts():
    #test that valid result
    def test_valid_remove(self, mock_delete_posts_moderator):
        deleted_post = remove_posts_moderator(1,"food")
        assert deleted_post == True
        deleted_post = remove_posts_moderator(2,"work")
        assert deleted_post == True
        deleted_post = remove_posts_moderator(3,"comment")
        assert deleted_post == True
    #tests empty id returns false
    def test_empty_id(self, mock_delete_posts_moderator):
        deleted_post = remove_posts_moderator(None,"food")
        assert deleted_post == False
    #tests invalid id returns false
    def test_invalid_id(self, mock_delete_posts_moderator):
        deleted_post = remove_posts_moderator(-1,"food")
        assert deleted_post == False
        deleted_post = remove_posts_moderator("Invalid ID","food")
        assert deleted_post == False
    #tests invalid source returns false
    def test_invalid_source(self, mock_delete_posts_moderator):
        deleted_post = remove_posts_moderator(1,"NotSource")
        assert deleted_post == False

