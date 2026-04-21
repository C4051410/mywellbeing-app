# Testing
***

## CI/CD

We use Github Actions to test our application for errors each time a commit occurs.
Github Actions uses the yml file to run each of the pytest within tests to check
that when code is updated it doesnt break the tests set out, allowing us to detect
easily if a piece of code has broken a test.

## How To Run Tests

1.  **Create and Activate the Virtual Enviorment**:
    
   ```bash
   .\venv\Scripts\activate     # Windows
   ```
    
2.  **Download the Requirements**:

   ```bash
   pip install -r requirements.txt
   ```
3.  **Run The Tests**:
   ```bash
   pytest src/tests
   ```

## Login and Registration Testing

## Homepage Testing

These tests are done to make sure that the homepage is correctly displayed,
as there is not much content, it is mainly checking that the page appears correctly


### Pytest

| Test Name | What it Tests                                   |
|--|-------------------------------------------------|
| TestTextContent | Tests that content will appear on Homepage      |
| TestNullSafety | Test that Null values wont crash the app        |
| TestFriendsWidget | Tests that friends Widget responds appropriatley |
| TestWidgetSizing | Tests that widgets resize correctly             |
|     TestResize             | Tests that page will resize correctly           |

## Activities Page Testing

## Nutrition Page Testing

## Social Page Testing

## Settings Page Testing

## Database Testing