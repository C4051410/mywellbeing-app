# CSC2033 Project Team 34

| **Criteria** | **Where to Find It (File Paths, Links, or Explanations)** |
|--------------|-----------------------------------------------------------|
| **Team Standards: Cohesion**                 | STYLE_GUIDE.md                                            |
| **Team Standards: Documentation**            | Below                                                     |
| **Team Standards: Version Control Workflow** | GIT_CONVENTION.md                                         |
| **Design & Structure**                       | DESIGN.md                                                 |
| **GUI: Clever and Interesting Design**       | screenshots/                                              |
| **Testing Documentation**                    | TESTING.md                                                |
| **Functionality and Features**               | FEATURES.md                                               |

***
**Installation Tutorial**

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
**How to Run Application**
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
    

<sub>* Some AI has been used in the development of this product *</sub>
