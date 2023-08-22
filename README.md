**Specification:**

- [x] User Authentication and Registration:
  - [x] User registration and login using Django's built-in authentication system.
  - [x] When a user registers, a profile should automatically be created
  
  
- [ ] Profile: From their Dashboard, users should be able to update their profile's details
  - [ ] The form should appear on the same page
  - [ ] The page shouldn't reload on validation

- [ ] Dashboard:
  - [x] When Logged-in, a user should be brought to their dashboard
  - [x] The Dashboard should display all the repositories that the user owns or is a collaborator on 
  - [x] Each repository should display it's title, description, owner and number of collaborators
  - [x] When clicking on a repository, the user should be directed to the page for that repository
  
- [ ] Notifications: the Dashboard should display a notification on each repository with a new message or file uploaded

- [x] Create View: There should be a link on the dashboard to bring the user to a new repository form 
  - [x]  Users can create new music project repository, providing a title and description.

- [ ] Project View:
  - [ ] The owner and collaborating users can create directories,
  - [ ] they can upload files in the desired location in their repository
  - [ ] and add multiple collaborators (musicians) (((who can be invited via email))).
  - [ ] Only the owner can remove collaborators
  - [ ] The owner can transfer ownership to another user

- [ ] File Storage:
    - [ ] The file structure of repositories looks and feels like a standard hierarchical file structure.
    - [x] The files should be stored on the server in the path "user_id/repository/" and reflect the file structure of the repository.

- [ ] Version Control:
  - [ ] Implementation of version control for music files (tracks, samples, etc.).
  - [ ] Users can upload new versions of tracks, and previous versions are saved and accessible.

- [ ] Chat:
  - [ ] The chatbox appears next to the file structure in a repository
  - [ ] Each chat is associated to a specific repository and is only accessed when on this repository's page
  - [ ] Collaborators can chat in repositories
  - [ ] Messages appear timestamped with the most recent at the bottom
  - [ ] The older messages fade out at the top of the chatbox
  - [ ] Each collaborator of the repository should get notified when a message has been sent by another user


  (((- [ ] Collaboration Features:
    - [ ] Real-time collaboration on tracks using WebSocket communication.

  - [ ] User Permissions and Access Control:
    - [ ] Different levels of access for collaborators (e.g., read-only, read-write).
    - [ ] Project owners can manage collaborators and their permissions.
  )))

- [ ] Soundtrack
    - [ ] When clicking on an audio file, the file should play 
    - [ ] When playing, the file should be visualized as an audio waveform with a time banner

- [ ] User Profile:
  - [ ] Display user information, profile picture, and list of owned and collaborated-on projects.

- [ ] Notifications and Alerts:
  - [ ] Notify users about collaboration invitations, comments, and changes to projects.

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