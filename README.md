# CSC2033 Project Team 34

| **Criteria**                                 | **Where to Find It (File Paths, Links, or Explanations)** |
|----------------------------------------------|-----------------------------------------------------------|
| **Team Standards: Cohesion**                 | STYLE_GUIDE.md                                            |
| **Team Standards: Documentation**            | Below                                                     |
| **Team Standards: Version Control Workflow** | GIT_CONVENTION.md                                         |
| **Design & Structure**                       | DESIGN.md                                                 |
| **GUI: Clever and Interesting Design**       | screenshots/                                              |
| **Testing Documentation**                    | src/tests/TESTING.md                                      |
| **Functionality and Features**               | FEATURES.md                                               |

***
## Documentation
All of our code is inserted with meaningful comments which explain the purpose of specific functions or code
to help others better understand how it works. Every function and class has a document block explaining its purpose
along with inline comments explaining the variables and other code. API's that are used have a link to the
documentation so that they can be better explained to others. We have also provided below how to install our
project properly and how to run the application, either via running through the terminal or creating it as it
own executable.

API Documentation: 

Strava: https://developers.strava.com/docs/reference/

Resend:https://resend.com/docs/api-reference/

***
## Installation Tutorial

1. **Clone The Repository**: "https://github.com/newcastleuniversity-computing/CSC2033-Team-34-Project.git"
2. **Create and Activate the Virtual Enviorment**:
   ```bash
   .\venv\Scripts\activate     # Windows
   source venv/bin/activate    # macOS/Linux
   ```
3. **Download the Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

***
## How to Run Application
* To run within windows, run:
   ```bash
   flet run
   ```
* To create an executable:

| Target Platform | Requirements & Prerequisites | Build Command |
|:---|:---|:---|
| **Windows** | Enable **Developer Mode** in Settings. Install [Visual Studio](https://visualstudio.microsoft.com/downloads/) with "Desktop development with C++". | `flet build windows` |
| **Android** | Install [Android Studio](https://developer.android.com/studio). Ensure **Android SDK** and **Java (JDK)** are in your system path. | `flet build apk` |
| **iOS** | Requires **macOS** with [Xcode](https://developer.apple.com/xcode/) and **CocoaPods** installed. | `flet build ios` |
 
* To make sure that all requirements are installed with executables, make sure pyproject.toml is included,
as it uses it to install all dependencies in the apps.

<sub>* Some AI has been used in the development of this product *</sub>
