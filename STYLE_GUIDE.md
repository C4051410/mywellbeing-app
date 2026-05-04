# Style Guide
***

**Naming Conventions**

| Type      | Convention       | Example                              |
|-----------|------------------|--------------------------------------|
| Variables | snake_case       | user_id,path_points                  |
| Functions | snake_case       | retrieve_foodlogs,save_past_activity |
| Classes   | PascalCase       | SocialPage,SettingsPage              |
| Constants | UPPER_CASE_SNAKE | API_KEY, CLIENT_ID                   |

Follows the Python Methodology

***
## Formating

* 4 Space Indentation
* Use Inline Commenting for explaining complex lines of code
* Line length of 88 characters
* Each Function,Class,and File has a Docstring

***

## Configuration Files

We use ruff to enforce a coding standard across python code
Its information is stored in pyproject.toml.
It includes stating the maximum line length a code should be
and what errors should be picked up. It also sets the 
format and complexity. Used within the GitHub Actions to prevent
code being merged which breaks it rules, this means that we maintain
a similar coding style throughout all the code.

