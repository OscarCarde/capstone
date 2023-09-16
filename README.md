**Distinctiveness and Complexity:**
  My Web application satisfies the distinctiveness requirements as it differs from any project done in this course. It is focused on file sharing and collaboration on music projects and has for features:
  - The sharing and serving of files 
  - A chat section for each music project
  - An audio waveform visualisation and player for audio files
  - A directory structure in each project that let's the user navigate through directories
  - a search feature to add collaborators
I believe it satisifies the complexity requirements by the range of features that it posseses
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
    
- [x] Create View: There should be a link on the dashboard to bring the user to a new repository form 
  - [x]  Users can create new music project repository, providing a title and description.

- [x] Comments:
  - [x] The chatbox appears next to the file structure in a repository
  - [x] Each chat is associated to a specific repository and is only accessed when on this repository's page
  - [x] Collaborators can comment in repositories
  - [x] Messages appear timestamped with the most recent at the bottom

- [x] File Storage:
    - [x] The file structure of repositories looks and feels like a standard hierarchical file structure.
    - [x] The files should be stored on the server in the path "user_id/repository/" and reflect the file structure of the repository.

- [x] Soundtrack
    - [x] When clicking on an audio file, the file should play 
    - [x] When playing, the file should be visualized as an audio waveform with a time banner

- [x] Profile: From their Dashboard, users should be able to update their profile's details
  - [x] The form should appear on the same page

- [x] Responsive: The website should display an interface appropriate the the device it is viewed on

- [x] Notifications: the Dashboard should display a notification on each repository with a new message or file uploaded

- [x] Project View:
  - [x] The owner and collaborating users can create directories,
  - [x] they can upload files in the desired location in their repository,
  - [x] delete files 
  - [x] delete folders with all their contents,
  - [x] When a user clicks on a file that isn't an audiofile, it should open in a new browser window

- [x] Settings: Each repository should have a link to a settings page for that repository accessible by all collaborators
  - [x] From the settings, A user should be able to rename the repository and change its description
  - [x] They should be able to delete the repository if they are the owner
  - [x] They should be able to leave the repository instead if they are collaborators
  - [x] The owner should be able to remove collaborators
  - [x] Any collaborator should be able to add other collaborators by finding them by username


**Files:**
**How to run the application:**