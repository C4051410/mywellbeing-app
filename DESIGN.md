# Design and Structure
***

## Separation of Functionality

* The Project has been created with the Three-Tier Architecture in mind. The project
has been seperated into the Presentation Tier (Flet UI Classes), 
Logic Tier (Python service functions), and Data Tier ( Database queries in database/).
* The Database and API calls have been encapsulated within the Logic Tier. This means that
the Front-End never calls directly to either, as it communicates through service modules
that validate the data and handle errors.
* Common UI components like NavBar or UserPfp have been stored in components/ to stop
common code being repeated for each page, and that they all have the same logic.
***

## Use of Directory and Packages

Python files and other files (.csv, .png. .TTF etc.), are stored in suitable folders to 
allow for easy organization of files

### Root Directory:
```
├── main.py               # This is where the main application is run from, bringing all resources together
├── .env                  # Used to store Enviorment Variables like DB and API Keys, to protect them from being stolen
├── .gitignore            # Define which files should and should not be committed to git
├── requirements.txt      # A list of all the python dependencies that need to be installed before running
├── CSC2033_test.yml      # Defines how the CI/CD automated testing runs on Github Actions
├── pyproject.toml        # Stores details like ruff programming style and how the application should be deployed
```
### File Structure:
All Program Files are Located in src/

CI/CD tests are stored in .github/

Screenshots are stored in screenshots/

All .md Files and other non-program files are stored in the project.

#### Within src:
```
├── activities/     # Manages the displayment and creation of activities, including Strava API
├── admin/          # Manages how the admin page is displayed and their controls.
├── assets/         # Stores images and other style choices needed by program
├── auth/           # Manages the authentication of users, logging in and registration of users
├── components/     # Contains UI widgets which are used across multiple pages to maintain consistency
├── database/       # Centralises all database connections to help manage with security
├── home/           # Manages how the homepage is displayed and retrieving information
├── moderator/      # Manages how the moderator page is displayed and their controls
├── nutrition/      # Manages the displayment and creation of nutrition logs.
├── settings/       # Manages the displayment and how the user is able to update information about their account
├── social/         # Manages the displayment of the comparision between users and their stats
├── tests/          # A range of different testing methods including how to run them
```
### Justification For Modularity
The structure of our package is effective, as its successfully separates core features and pages,
meaning that new features can be added with a reduced risk of causing bugs across the application.
It also makes it easier for the developers to navigate and find bugs quicker.