[![Watch the video](https://img.youtube.com/vi/ASuaOeJHPxo/hqdefault.jpg)](https://www.youtube.com/embed/ASuaOeJHPxo)


**Distinctiveness and Complexity:**
  My Web application satisfies the distinctiveness requirements as it differs from any project done in this course. It is focused on file sharing and collaboration on music projects and has for features:
  - Dashboard:
      Here, users are greeted with an intuitive interface that displays repositories they own and collaborate on, sorted by order of the last modified. They are able to toggle between repositories that they own, collaborate on or both. Crafting this dashboard involved intricate database queries and dynamic template rendering to provide a seamless experience.

  - File Storage and Structure:
      One of the most distinctive features of my project is the hierarchical file structure that mimics a standard file system. Behind the scenes, each directory and file's path is recursively computed to be stored in the server identically to how it is stored for the user. Additionaly, files and directories that are in subdirectories recursively go through their parent directories to determine which repository they belong to. Repositories are themselves Directory instances. This file management system was a complex endeavor, merging the virtual and physical worlds seamlessly.

  - Comments:
      The chatbox feature in Palinodes provides a space for comments, directly associated with specific repositories. They are presented as a chat to encourage collaboration

  - Audio Playback and Visualization:
      To enhance the user experience, I integrated the WaveSurfer libary for audio playback and waveform visualization. Users can click on audio files, which play dynamically and provide a visual representation of the audio's waveform, a feature that sets Palinodes apart from standard file-sharing platforms.

  - Settings Management:
      Each repository has a settings page that allows users to rename, describe, delete, and manage collaborators. These features are accessible to all collaborators, and owners hold the power to add or remove collaborators. Implementing a search feature for collaborators using asynchronous fetch calls to update the search results on user input was a complex task

  - Notifications:
      The dashboard is equipped with a notification system that appears on each repository every time a file, folder or comment was created or deleted. This feature enables users to keep track of changes to a repository and is unique to Palinodes.

  - Project View:
      Users can create directories, upload files, manage content and chat within repositories, all while enjoying a familiar file system interface. This feature mirrors the complexity of managing physical files while providing a digital workspace.

**Files:**
  - Static files:
    - the following javascript files contain the dynamic behaviour for their respective templates:
      - dashboard.js: dynamic behaviour of the dashboard template, including profile editing and toggling between owned/collaborating/recent repositories
      - repository.js: for the repository template, implements the chat/file structure/ waveform visualisation for the corresponding repository in the template context
      - settings.js: for both the settings template and the new directory form template. it implements repository deletion or leave if a collaborator, as well as the search feature to dynamically find collaborators on input and the removal of existing collaborators.
      - helpers.js: implements helper functions that are occasionaly reused in other js files

    - the following stylesheets separated for responsiveness
      - common.css: stylesheet for the whole website that implements styles common to all device sizes
      - smallscreen.css: implements styles for small screens only
      - widescreen.css: implements styles for widescreens only
  
  - Templates:
    - layout.html: provides html headers, scripts and stylesheets common to all templates as well as the top navbar.
    - dashboard.html: renders dashboard template using context passed from the corresponding view.
    - repository.html: renders repository corresponding to the url /repository/repository_id
    - directory_form.html: renders a form to create a new repository from a corresponding class based form view
    - settings.html: renders the forms to edit the current repository using a combination of template context form and forms handled by javascript with api calls
    - login.html/register.html: provides forms to handle user login and registration using django built-in authentication capabilities.

  - Python files:
    - apis.py: implements the Django Rest apis endpoints to create/edit and delete files/directories/repositories/comments
    - forms.py: implements the RepositoryForm and ProfileForm forms passed to the template contexts
    - helpers.py: implements helper methods
    - models.py: implements the models User/Profile/Directory/FileModel/Notification/Comment with their custom properties
    - serializers.py: implements serializers to convert data from models to data structures that can be easily read and converted to json for the apis
    - tests.py: implements tests for models, views and apis
    - urls.py: defines urls and maps them to views and apis
    - views.py: implements the login/logout/register views as well as the dashboard/repository/settings views and the CreateRepository generic form view.
    - settings.py: sets up the project and defines the paths to upload and access media files

  
  - Other Files:
    - .gitignore: excludes files from version control
    - db.sqlite3: database
    - requirements.txt: the set of requirements to install to be able to run the project
    - testFiles: files used for unit testing

**How to run**:
I recommend using a virtual environment like venv.
You need to be connected to the internet for the cdn libraries.

- clone the repository
- install requirements in requirements.txt with pip `pip install requirements.txt`
- run the application with `python3 manage.py runserver`
- login as superuser with username _admin_ and password _1234_

**Specification:**

- [x] User Authentication and Registration:
  - [x] User registration and login using Django's built-in authentication system.
  - [x] When a user registers, a profile should automatically be created
  
- [x] Dashboard:
  - [x] When Logged-in, a user should be brought to their dashboard
  - [x] The Dashboard should display all the repositories that the user owns or is a collaborator on 
  - [x] The user should be able to view its most recent repositories, owned and collaborated on separately on the same page
  - [x] Each repository should display it's title, description, owner and number of collaborators
  - [x] When clicking on a repository, the user should be directed to the page for that repository
    
- [x] Profile: From their Dashboard, users should be able to update their profile's details
  - [x] The form should appear on the same page

- [x] Create View: There should be a link on the dashboard to bring the user to a new repository form 
  - [x]  Users can create new music project repository, providing a title and description.

- [x] Project View:
  - [x] The owner and collaborating users can create directories,
  - [x] they can upload files in the desired location in their repository,
  - [x] delete files 
  - [x] delete folders with all their contents,
  - [x] When a user clicks on a file that isn't an audiofile, it should open in a new browser window or download

- [x] File Storage:
    - [x] The file structure of repositories looks and feels like a standard hierarchical file structure.
    - [x] The files should be stored on the server in the path "user_id/repository/" and reflect the file structure of the repository.

- [x] Soundtrack
    - [x] When clicking on an audio file, the file should play 
    - [x] When playing, the file should be visualized as an audio waveform with a time banner

- [x] Comments:
  - [x] The chatbox appears next to the file structure in a repository
  - [x] Each chat is associated to a specific repository and is only accessed when on this repository's page
  - [x] Collaborators can comment in repositories
  - [x] Messages appear timestamped with the most recent at the bottom

- [x] Notifications: the Dashboard should display a notification on each repository with a new message or file uploaded

- [x] Settings: Each repository should have a link to a settings page for that repository accessible by all collaborators
  - [x] From the settings, A user should be able to rename the repository and change its description
  - [x] They should be able to leave the repository instead if they are collaborators
  - [x] They should be able to delete the repository if they are the owner
  - [x] The owner should be able to remove collaborators
  - [x] Any collaborator should be able to add other collaborators by finding them by username

- [x] Responsive: The website should display an interface appropriate to the device it is viewed on