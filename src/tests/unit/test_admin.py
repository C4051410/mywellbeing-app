from unittest.mock import patch


from admin.admin_services import check_admin, retrieve_users_admin, remove_users_admin, make_moderators_admin

#mocks db queries to avoid using actual db
@patch('admin.admin_services.get_admin')
#used to test check_admin
class TestCheckAdmin():
    #tests valid result
    def test_valid_check(self, mock_admin):
        mock_admin.return_value = "admin"
        success = check_admin(1)
        assert success == True
    #tests incorrect role returns false
    def test_incorrect_role(self, mock_admin):
        mock_admin.return_value = "user"
        success = check_admin(1)
        assert success == False
        mock_admin.return_value = "moderator"
        success = check_admin(1)
        assert success == False
    #tests invalid ID returns False
    def test_invalid_id(self, mock_admin):
        mock_admin.return_value = "admin"
        success = check_admin(-1)
        assert success == False
        success = check_admin("Invalid ID")
        assert success == False
    # test is missing field returns false
    def test_missing_fields(self, mock_admin):
        mock_admin.return_value = "admin"
        success = check_admin(None)
        assert success == False

@patch('admin.admin_services.get_users_admin')
#tests retrieve_users_admin
class TestRetrieveUsers():
    #create fake rows which would be returned by db query
    rows = [
        ("Runner1","ILUVRUN@gmail.com","user",2),
        ("ModerationKing","ModerationKing@gmail.com","moderator",3),
    ]
    #test it returns correct rows
    def test_valid_retrieve(self, mock_rows):
        mock_rows.return_value = self.rows
        returned_rows = retrieve_users_admin("")
        assert returned_rows[0] == ("Runner1","ILUVRUN@gmail.com","user",2)
        assert returned_rows[1] == ("ModerationKing","ModerationKing@gmail.com","moderator",3)
        assert len(returned_rows) == 2
    #test empty row returns empty row
    def test_empty_retrieve(self, mock_rows):
        mock_rows.return_value = []
        returned_rows = retrieve_users_admin("")
        assert returned_rows == []
        assert len(returned_rows) == 0

@patch('admin.admin_services.delete_users_admin')
#test remove_users_admin
class TestRemoveUsers():
    #test valid return
    def test_valid_remove(self, mock_admin):
        deleted_user = remove_users_admin(1)
        assert deleted_user == True
    #test missing fields return false
    def test_missing_fields(self, mock_admin):
        deleted_user = remove_users_admin(None)
        assert deleted_user == False
    #test invalid id returns false
    def test_invalid_id(self, mock_admin):
        deleted_user = remove_users_admin(-1)
        assert deleted_user == False
        deleted_user = remove_users_admin("Invalid ID")
        assert deleted_user == False

@patch('admin.admin_services.update_moderators_admin')
#tests make_moderators_admin
class TestUpdateModerators():
    #test valid update
    def test_valid_update(self, mock_admin):
        update_mod = make_moderators_admin(1)
        assert update_mod == True
    #test missing fields return false
    def test_missing_fields(self, mock_admin):
        update_mod = make_moderators_admin(None)
        assert update_mod == False
    #test invalid id returns false
    def test_invalid_id(self, mock_admin):
        update_mod = make_moderators_admin(-1)
        assert update_mod == False
        update_mod = make_moderators_admin("Invalid ID")
        assert update_mod == False

