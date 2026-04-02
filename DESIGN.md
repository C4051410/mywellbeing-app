# Design and Structure
***

**Seperation of Functionality**

* Classes are used in the creation of Flet pages
* Functions are used to call upon these classes in other python files
* Backend and Frontend tasks are seperated to avoid a conflict and adds
a layer of protection and security.

***

**Use of Directory and Packages**

Python files and other files (.csv, .png. .TTF etc.), are stored in suitable folders to 
allow for easy organization of files

* src is used to store all program files, where .github is used to store CI/CD
* activities store all files related to the fitness page
* admin stores all files related to the admin page
* assets stores all design assets like images and fonts
* auth is used to manage authentication of users, backend and front
* components store elements which are used across multiple pages like navigation bar
* database is used for files which use the database
* home store files related to the home page
* moderator store all files related to the moderator page
* nutrition stores all files related to the nutrition page
* settings store all files related to the settings page
* tests store all files used in the testing of the application