from unittest.mock import patch

import bcrypt
import pytest

from auth.auth_services import login_user, register_user, check_setup_complete, save_setup

"""
    UNIT TESTS: Validates the authentication logic in auth_services.py.
    Covers credential validation, field checks, and error message triggering.
"""
@patch('auth.auth_services.login')
@patch('auth.auth_services.notification')
class TestLogin():
    #create valid variables to be used throught
    email = 'testingemail@outlook.com'
    password = 'PASSword1!'
    hashed_password = bcrypt.hashpw(password.encode("utf-8"),
                      bcrypt.gensalt(12)).decode("utf-8")
    user = (1,'TestUser','testingemail@outlook.com',hashed_password)
    def test_valid_login(self,mock_notification, mock_login):
        #mock return to be user
        mock_login.return_value = self.user
        success,message = login_user(self.email,self.password)
        #check success is True and message is correct
        assert success is True
        assert message == self.user

    def test_missing_fields(self,mock_notification, mock_login):
        mock_login.return_value = self.user
        #check when fields are empty/none
        success,message = login_user(None,None)
        assert success is False
        assert message == 'Please Enter All Fields'

    def test_invalid_email(self,mock_notification, mock_login):
        #checks that invalid emails do not pass
        mock_login.return_value = self.user
        success,message = login_user("emailgmail.com",self.password)
        assert success is False
        assert message == 'Invalid Email'
        success,message = login_user("email@gmail.c",self.password)
        assert success is False
        assert message == 'Invalid Email'
    def test_user_not_found(self,mock_notification, mock_login):
        #checks that is user not found returns false with message
        mock_login.return_value = ()
        success,message = login_user(self.email,self.password)
        assert success is False
        assert message == 'User Not Found'
    def test_incorrect_password(self,mock_notification, mock_login):
        mock_login.return_value = self.user
        success,message = login_user(self.email,"WrongPassword1")
        assert success is False
        assert message == 'Invalid Password'

@patch('auth.auth_services.register')
@patch('auth.auth_services.notification')
@patch('auth.auth_services.get_existing_user')
@patch('auth.auth_services.resend.Emails.send')
class TestRegister():
    username = "TestUser"
    email = 'testingemail@outlook.com'
    password = 'Password1!'
    def test_valid_register(self,mock_email,mock_get, mock_notification, mock_register):
        #used to check valid registration with correct values
        mock_get.return_value = (None,None)
        mock_register.return_value = 1
        success,message = register_user(self.username,self.email,self.password)
        assert success is True
        assert message == 1
    def test_missing_fields(self,mock_email,mock_get, mock_notification, mock_register):
        #used to check when fields are empty it returns false
        mock_get.return_value = (None,None)
        mock_register.return_value = 1
        success,message = register_user(None,None,None)
        assert success is False
        assert message == 'Please Enter All Fields'
    def test_invalid_email(self,mock_email,mock_get, mock_notification, mock_register):
        #used to check when email is incorrect format and returns false
        mock_get.return_value = (None,None)
        mock_register.return_value = 1
        success, message = register_user(self.username,"emailgmail.com", self.password)
        assert success is False
        assert message == 'Please enter a valid email'
        success, message = register_user(self.username,"email@gmail.c", self.password)
        assert success is False
        assert message == 'Please enter a valid email'

    #will cycle through all the incorrect passwords
    @pytest.mark.parametrize("password, expected_msg",[
        ("tooshrt","Password must be at least 8 characters long"),
        ("nocaps1!","Password must at least one uppercase letter, one lowercase letter, one number and one special character"),
        ("NOLOWER1!","Password must at least one uppercase letter, one lowercase letter, one number and one special character"),
        ("NoNumber!","Password must at least one uppercase letter, one lowercase letter, one number and one special character"),
        ("NoSpecial1","Password must at least one uppercase letter, one lowercase letter, one number and one special character")
    ])
    def test_invalid_password(self,mock_email,mock_get, mock_notification, mock_register,password,expected_msg):
        #used to test all ways the password could be incorrect
        mock_get.return_value = (None,None)
        mock_register.return_value = 1
        success, message = register_user(self.username,self.email,password)
        assert success is False
        assert message == expected_msg
    def test_user_already_exists(self,mock_email,mock_get, mock_notification, mock_register):
        #check if user already exists
        mock_get.return_value = ("TestUser",None)
        mock_register.return_value = 1
        success,message = register_user(self.username, self.email,self.password)
        assert success is False
        assert message == 'User Already Exists'
    def test_email_already_exists(self,mock_email,mock_get, mock_notification, mock_register):
        #check if email already exists
        mock_get.return_value = (None,"testingemail@outlook.com")
        mock_register.return_value = 1
        success,message = register_user(self.username, self.email,self.password)
        assert success is False
        assert message == 'Email Already Exists'

@patch('auth.auth_services.get_user_setup')
class TestCheckSetup():
    def test_complete_setup(self,mock_get):
        #test valid setup
        mock_get.return_value = (1,)
        setup = check_setup_complete(1)
        assert setup == True
    def test_incomplete_setup(self,mock_get):
        #test when setup isn't valid
        mock_get.return_value = None
        setup = check_setup_complete(1)
        assert setup == False
    def test_missing_fields(self,mock_get):
        #test when setup is missing field
        setup = check_setup_complete(None)
        assert setup == False
    def test_invalid_id(self,mock_get):
        #tests when id is not valid
        setup = check_setup_complete(-1)
        assert setup == False
        setup = check_setup_complete("Not Valid")
        assert setup == False
@patch('auth.auth_services.commit_setup')
class TestSaveSetup():
    def test_complete_setup(self,mock_commit):
        #test valid setup
        setup = save_setup(1,18,"Male",185,
                           85,75,2500,
                           5.0,100,4000)
        assert setup == True
    def test_missing_setup(self,mock_commit):
        #test setup when fields are missing it fails
        setup = save_setup(None,None,None,None,
                           None,None,None,
                           None,None,None,)
        assert setup == False
    def test_invalid_fields(self,mock_commit):
        #test when fields are invalid
        setup = save_setup(-1,-1,"Male",-1,-1.0,-1.0,-1,-1.0,-1.0,-1)
        assert setup == False
        setup = save_setup("Invalid","Invalid", "Male",
                           "Invalid","Invalid","Invalid",
                           "Invalid","Invalid","Invalid",
                           "Invalid")
        assert setup == False