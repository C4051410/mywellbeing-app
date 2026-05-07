# Features and Functionality

***
## Minimum Requirements
### Database Integration
We have implemented a remote database using Neon, to allow users to be able to access the database
from anywhere with an internet access. This also means that the app updates in real time, meaning 
users can see others posts and information as it occurs.

[src/database](src/database)
### Access Control
We have 3 types of user roles, admin, moderators and users. Admins have the powers to manage users
and moderators being able to delete accounts and promote others to moderators.
Users cant change other users data, with the most restricted access.

[src/admin](src/admin)
### Three Tier Architecture
* The Project has been created with the Three-Tier Architecture in mind. The project
has been seperated into the Presentation Tier (Flet UI Classes), 
Logic Tier (Python service functions), and Data Tier ( Database queries in database/).
* The Database and API calls have been encapsulated within the Logic Tier. This means that
the Front-End never calls directly to either, as it communicates through service modules
that validate the data and handle errors.

[src/](src/)
### UN Sustainable Goals
The application promotes the UN goals as it encourages Good Health and Wellbeing.
The app provides a links to the website on the homepage and emails also contain links.

[src/home/homepage.py](src/home/homepage.py)

## Enable User Intearction
The application allows for user interaction by allowing them to track their activities and
nutrition values, while also being able to view others on the social page.

[src/activities](src/activities), [src/nutrition](src/nutrition) and [src/social](src/social)

## Intermediate Requirements
### Alert/Notification
* The application uses two types of notifications. The first is plyer.notifications, which is used
to create notifications which appear on the users actual device, which is used for when they 
log in/register and create new activities and nutrition logs.
* The second type is Resend. This is an email notification system, which is used to send emails 
to the email related to the user. This is done when the user registers a new account, deletes
their account, or when they have not signed in for 20 hours, reminding them to keep their streak

[src/auth/auth_services.py](src/auth/auth_services.py), 
[src/activities/activities_services.py](src/activities/activities_services.py), 
[src/nutrition/nutrition_services.py](src/nutrition/nutrition_services.py) and 
[src/settings/settings_services.py](src/settings/settings_services.py)

### Further User Roles
We created a moderator role as an extended role, they are allowed to view and delete users posts,
acting as a back-up in case any posts are released which contain foul langauge or anything inappropriate

[src/moderator](src/moderator)

### Dashboards
There are multiple dashboards showing the users stats and posts. The user can get an overview from the homepage,
They can get more detailed views in activities, nutrition and social pages.

[src/home/homepage.py](src/home/homepage.py),
[src/activities/activities.py](src/activities/activities.py),
[src/nutrition/nutrition.py](src/nutrition/nutrition.py) and
[src/social/social.py](src/social/social.py)

### Game Mechanics
We have implemented two gamification techniques
* We created a duolingo like streak system, where the user is required to enter an activity each day
to keep their streak going, encouraging them to come back to the app each day.
* We have also implemented a leaderboard system which encourages users to try and beat their friends to
be the highest scoring player.

[src/activities/activities_services.py](src/activities/activities_services.py) and 
[src/social](src/social)

### Deployment System
Rather then using Docker, we have used flet's own built in deployment tool, using flet build to create
an isolated executable for a range of different platforms, like IOS, Andorid and Windows, this not only allows
our app to run separately from the code, but it can be suited for each system providing a better user experience.
To define how the executable is made, we use pyproject to determine what notifications and dependencies are needed.

[pyproject.toml](pyproject.toml)

## Advanced Requirements
### Location Based Features
We use flets geolocator in order to find the users current location, we then use this to allow users
to track live runs and cycles by getting their current gps coordinates and tracking the distance they travel
over the entire journey. This provides users with an alternative way to track their exercises.

[src/activities/map.py](src/activities/map.py)

### Further User Roles
Admin and Moderators are provided with an alternative page to streamline what they are required to do.
There page provides the tools that they need to access and alter the data, creating an isolation from normal
users preventing them from being accessed via the regular app.

[src/admin/admin.py](src/admin/admin.py) and 
[src/moderator/moderator.py](src/moderator/moderator.py)

### External API's and Services
We use a wide range of different API's and Services
#### API
* We use Strava API to allow users to connect their strava account to our application, allowing them to store
strava activities to create a nice synergy between the two applications
* We also use Resend API as mentioned above to create email notifications to send to users.

[src/activities/activities_services](src/activities/activities_services.py)

#### Services
* We use Flet to create our application, as it's a great service to allow python and flutter to communicate
with each other, allowing use to create a responsive application which works on multiple platforms.
* To create our end-to-end testing, we use appium to allow us to create UI testing by using the tools
to open and run our application on an emulator, using Appium Inspector to find the flutter objects to make sure
the test works as intended.
* We also use GitHub Actions to create a CI/CD cycle to run testing pipelines on every push. This ensures
that each push we made had to past the tests before merging into main.

[src/tests/e2e/](src/tests/e2e/) and [.github/workflows/CSC2033_test.yml](.github/workflows/CSC2033_test.yml)
### Data Science
* We use data science in our data setup, as it is used to figure out the target calories count based on the 
target weight by using the amount of exercise they do with the BMI.
* We also use it to figure out the scores of the leaderboard, multiplying a range of values
to figure out the users total score.
* Also in map we use maths to find the distance between the points on the map to calculate the distance
ran while also calculating the speed of the user as well.

[src/auth/setup.py](src/auth/setup.py) 
[src/social/social_queries.py](src/social/social_queries.py) and
[src/activities/map.py](src/activities/map.py)
