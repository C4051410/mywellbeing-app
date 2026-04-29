# Git Conventions

***

**Branching Strategy**
We adopted as a team a GitHub Flow branching strategy, ensuring the main branch always remained in a stable condition.
We conducted all development within our own development branch in isolation from main to ensure the main branch never
resulted in errors or bugs. Developers should use rebase if their branch falls too much behind the main branch to ensure
the branch isn't outdated

**Branch Conventions**

"<category-reference-description>"


| Category | When Used                                              |
|----------|--------------------------------------------------------|
| feature  | used to implement new functionality                    |
| bugfix   | used to fix minor errors that occur during production  |
| hotfix   | used in emergency to fix errors that prevent production |
| testing  | used when creating tests                               |

***
**Git Commits**
"<category: description">

| Category | When Used                                        |
|-------|--------------------------------------------------|
| feature | when you implement a new functionality           |
| fix   | when repearing bugs                              |
| refactor | when changing the structure of the code          |
| chore | "housekeeping", used when nothing major is chanegd |

***
**Pull Requests**

Pull Requests occurs when a developer is ready to add their code into main, we have followed these rules to protect
ourselves against error being merged into main
* Should list the new features or changes made in bullet points.
* Any conflicts should be consulted by others first before removing code
* Users should wait until at least 2 other members approve of the pull request and reviewed the code.
* The request must meet with the CI/CD Github Action before merging to ensure the main functions of the project work

This workflow allows each developer to work on their own project without the worry that their code will stop working.
It is also useful in protecting the main project from being damaged by developers who rush unfinished/broken code back
into main, requiring many steps before entering the main.