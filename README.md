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

- [ ] Project View:
  - [x] The owner and collaborating users can create directories,
  - [x] they can upload files in the desired location in their repository,
  - [x] delete files 
  - [x] delete folders with all their contents,
  - [x] and add multiple collaborators (musicians) (((who can be invited via email))).
  - [ ] Only the owner can remove collaborators
  - [x] The Owner can delete the project and is redirected to his dashboard when doing so
  - [ ] Collaborating users should be able to leave a repository

- [ ] Invite: Users should be able to add collaborators to a repository
  - [ ] Only non collaborating users should be invitable
  - [ ] 
  


- [ ] **Additional Features:**
  - [ ] Search and Discovery:
    - [ ] Search functionality to find public projects based on keywords or tags.
    - [ ] Trending and popular projects based on user interactions.

  - [ ] Analytics and Insights:
    - [ ] Basic analytics for projects, such as track play counts and collaborator contributions.

  - [ ] Security and Privacy:
    - [ ] Proper authentication and authorization mechanisms to ensure data privacy and security.
    - [ ] Secure storage and handling of music files and user data.

  - [ ] Deployment and Hosting:
    - [ ] Deploy the web app on a cloud hosting platform like Heroku or DigitalOcean.



**Distinctiveness and Complexity:**
**Files:**
**How to run the application:**