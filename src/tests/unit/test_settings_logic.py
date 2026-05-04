from unittest.mock import patch

import bcrypt
import pytest

from settings.settings_services import update_password, update_goals, retrieve_notification_status, \
    update_notification_status, delete_account


#used to prevent functions within which could cause errors
@patch('settings.settings_services.retrieve_current_password')
@patch('settings.settings_services.commit_update_password')
#used to test password update
class TestPasswordUpdate():
    #sets values used in tests
    st_pwsd = "Password1!"
    hs_pswd = bcrypt.hashpw(st_pwsd.encode("utf-8"), bcrypt.gensalt(12))
    cu_pswd = "Password1!"
    nw_pswd = "Password2!"
    cn_pswd = "Password2!"

    #tests a valid update
    def test_valid_update(self,mock_commit,mock_retrieve):
        #used to mock return of password with set value
        mock_retrieve.return_value = self.hs_pswd
        #provides a successful update example
        success, message = update_password(1,self.cu_pswd,
                                           self.nw_pswd,self.cn_pswd)
        #checks results are true and message is correct
        assert success == True
        assert message == "Password Updated"

    #checks it catches missing fields
    def test_missing_field(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.cu_pswd
        #returns None as missing fields
        success, message = update_password(1,
                                           None,
                                           None,
                                           None)
        #checks it fails and displays right message
        assert success == False
        assert message == "All Fields Required"

    #checks for when password is incorrect
    def test_password_incorrect(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        #password doesnt match that returned from db
        success, message = update_password(1,
                                           "WrongPass1!",
                                           self.nw_pswd,
                                           self.cn_pswd)
        assert success == False
        assert message == "Current Password Incorrect"

    #checks for when new password is the same as old
    def test_same_password(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        #new password is the same as last
        success, message = update_password(1,
                                           self.cu_pswd,
                                           self.cu_pswd,
                                           self.cu_pswd)
        assert success == False
        assert message == "New Password Cant Be Same as Old"

    #checks password is the correct length
    def test_password_length(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        #password is too short
        success, message = update_password(1,
                                           self.cu_pswd,
                                           "ToShrt!",
                                           "ToShrt!")
        assert success == False
        assert message == "Password must be at least 8 characters long"

    #makes sure that minimum number of each type appears
    def test_password_character(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        #password without lowercase
        success, message = update_password(1,
                                           self.cu_pswd,
                                           "NOLOWER!",
                                           "NOLOWER!")
        assert success == False
        assert message == "Password must contain at least 1 Uppercase,lowercase and special character"
        #password without uppercase
        success, message = update_password(1,
                                           self.cu_pswd,
                                           "noupper!",
                                           "noupper!")
        assert success == False
        assert message == "Password must contain at least 1 Uppercase,lowercase and special character"
        #password without special character
        success, message = update_password(1,
                                           self.cu_pswd,
                                           "NoSpecial",
                                           "NoSpecial")
        assert success == False
        assert message == "Password must contain at least 1 Uppercase,lowercase and special character"


@patch('settings.settings_services.commit_update_goals')
#tests goal update
class TestGoalUpdate():
    #sets values
    calories = 2500
    water = 2600
    weekly_goal = 5
    #tests a valid update
    def test_valid_update(self,mock_goals):
        # Mock a successful goal update
        mock_goals.return_value = True
        #valid inputs for update goal
        success,message = update_goals(1,self.calories,self.water,self.weekly_goal)
        #checks it returns true and correct message
        assert success == True
        assert message == "Goals Updated"

    #checks if missing fields are caught
    def test_missing_field(self,mock_goals):
        #None used to represent missing fields
        success,message = update_goals(1,None,None,None)
        #checks it false and correct message
        assert success == False
        assert message == "All Fields Required"

    def test_invalid_goals(self,mock_goals):
        #checks that negative values arent allowed
        success,message = update_goals(1,-1,-1, -1)
        assert success == False
        assert message == "Calories and Water Must Be Greater Than or Equal To 0"
        # Checks that activity goal must stay in between 0-7
        success, message = update_goals(1, 2000, 2000, 8)
        assert success == False
        assert message == "Weekly Activity Goal Must Be Between 0 and 7"
        #checks incorrect type isnt allowed
        success, message = update_goals(1,"Invalid","Invalid", "Invalid")
        assert success == False
        assert success == False
        assert message == "Invalid Value"

@patch('settings.settings_services.get_notification_status')
@patch('settings.settings_services.commit_notification_status')
class TestNotificationStatus():
    #check that it works when intended
    def test_valid_retrieve(self,mock_commit,mock_notification_status):
        #used to mock successful response
        mock_notification_status.return_value = True
        success = retrieve_notification_status(1)
        #check it returns true
        assert success == True
    #check that it doesn't allow for invalid responses
    def test_invalid_retrieve(self,mock_commit,mock_notification_status):
        #check None returns false
        mock_notification_status.return_value = None
        success = retrieve_notification_status(1)
        assert success == False
        #check invalid user_ids are caught and return false
        success = retrieve_notification_status(-1)
        assert success == False
        success = retrieve_notification_status("User")
        assert success == False
    #check that update works as intended
    def test_valid_update(self,mock_commit,mock_notification_status):
        #check both true and false return True to show successful
        success = update_notification_status(1,True)
        assert success == True
        success = update_notification_status(1,False)
        assert success == True

    def test_invalid_update(self,mock_commit,mock_notification_status):
        #Check None is rejected
        success = update_notification_status(1,None)
        assert success == False
        #check user_id is valid
        success = update_notification_status(-1,True)
        assert success == False
        success = update_notification_status("User",True)
        assert success == False

@patch('settings.settings_services.delete_user_account_db')
class TestDeleteUserAccount():
    def test_valid_delete(self,mock_delete_user_account):
        #check for when the account is deleted successfully
        mock_delete_user_account.return_value = True
        success, message = delete_account(1)
        assert success == True
        assert message == "Account Deleted Successfully"
    def test_invalid_delete(self,mock_delete_user_account):
        #check that user id has to be vali
        mock_delete_user_account.return_value = True
        success,message = delete_account(-1)
        assert success == False
        assert message == "Invalid User Id"
        success,message = delete_account("User")
        assert success == False
        assert message == "Invalid Value"
        #check for when there is an issue with DB
        mock_delete_user_account.return_value = False
        success,message = delete_account(1)
        assert success == False
        assert message == "Failed to Delete Account"





