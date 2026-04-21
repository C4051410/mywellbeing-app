# Design and Structure
***

## Seperation of Functionality

* Classes are used in the creation of Flet pages
* Functions are used to call upon these classes in other python files
* Backend and Frontend tasks are seperated to avoid a conflict and adds
a layer of protection and security. Backend functions include calling upon
the database and other sensitive functions. Frontend includes displaying variables
and flet objects.

***

## Use of Directory and Packages

Python files and other files (.csv, .png. .TTF etc.), are stored in suitable folders to 
allow for easy organization of files

### Main Programs:
```
├── main.py               # Where Main Application is Launched
├── .env                  # Used to store Enviorment Variables like DB keys
├── .gitignore            # Define which files not to store on Git
├── requirements.txt      # Python dependencies needed to run application
├── CSC2033_test.yml      # Defines how CICD test are run
├── pyproject.toml        # Blueprint of how application works
```
### File Structure:
All Program Files are Located in src/

CI/CD tests are stored in .github/

Screenshots are stored in screenshots/

All .md Files and other non-program files are stored in the project.

#### Within src:
```
├── activities/     # Stores all files related to the activities page
├── admin/          # Stores all files related to the admin page
├── assets/         # Stores images/fonts used in program
├── auth/           # Stores all files realted to login/registration
├── components/     # Stores all files that are used throughout all pages
├── database/       # Stores all files that are used to access the database
├── home/           # Stores all files related to the homepage
├── moderator/      # Stores all files related to the moderator page
├── nutrition/      # Stores all files related to the nutrition page
├── settings/       # Stores all files related to the settings page
├── social/         # Stores all files related to the Social Page
├── tests/          # Stores files used in testing
```
