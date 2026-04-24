from unittest.mock import patch

import bcrypt
import pytest

from settings.settings_services import update_password

@patch('settings.settings_services.retrieve_current_password')
@patch('settings.settings_services.commit_update_password')
class Test_Password_Update():
    st_pwsd = "Password1!"
    hs_pswd = bcrypt.hashpw(st_pwsd.encode("utf-8"), bcrypt.gensalt(12))
    cu_pswd = "Password1!"
    nw_pswd = "Password2!"
    cn_pswd = "Password2!"

    def test_valid_update(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        success, message = update_password(1,self.cu_pswd,
                                           self.nw_pswd,self.cn_pswd)
        assert success == True
        assert message == "Password Updated"
    def test_missing_field(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.cu_pswd
        success, message = update_password(1,
                                           None,
                                           None,
                                           None)
        assert success == False
        assert message == "All Fields Required"

    def test_password_incorrect(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        success, message = update_password(1,
                                           "WrongPass1!",
                                           self.nw_pswd,
                                           self.cn_pswd)
        assert success == False
        assert message == "Current Password Incorrect"

    def test_same_password(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        success, message = update_password(1,
                                           self.cu_pswd,
                                           self.cu_pswd,
                                           self.cu_pswd)
        assert success == False
        assert message == "New Password Cant Be Same as Old"

    def test_password_length(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        success, message = update_password(1,
                                           self.cu_pswd,
                                           "ToShrt!",
                                           "ToShrt!")
        assert success == False
        assert message == "Password must be at least 8 characters long"

    def test_password_character(self,mock_commit,mock_retrieve):
        mock_retrieve.return_value = self.hs_pswd
        success, message = update_password(1,
                                           self.cu_pswd,
                                           "NOLOWER!",
                                           "NOLOWER!")
        assert success == False
        assert message == "Password must contain at least 1 Uppercase,lowercase and special character"

        success, message = update_password(1,
                                           self.cu_pswd,
                                           "noupper!",
                                           "noupper!")
        assert success == False
        assert message == "Password must contain at least 1 Uppercase,lowercase and special character"

        success, message = update_password(1,
                                           self.cu_pswd,
                                           "NoSpecial",
                                           "NoSpecial")
        assert success == False
        assert message == "Password must contain at least 1 Uppercase,lowercase and special character"


