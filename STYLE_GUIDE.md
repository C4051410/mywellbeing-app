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

```python
import os

DATABASE_KEY = os.getenv("DATABASE_URL")
class ClassType:
    def function_example():
        variable_example = 1
        return 1
    
```

***
## Formating

* 4 Space Indentation
* Use Inline Commenting for explaining complex lines of code
* Line length of 188 characters
* Each has a Docstring

***

## Configuration Files

We use ruff to enforce a coding standard across python code
Its information is stored in pyproject.toml.
It includes stating the maximum line length a code should be
and what errors should be picked up. It also sets the 
format and complexity. Used within the GitHub Actions to prevent
code being merged which breaks it rules, this means that we maintain
a similar coding style throughout all the code.

[pyproject.toml](pyproject.toml) and
[.github/workflows/CSC2033_test.yml](.github/workflows/CSC2033_test.yml)

