import { searchUsers, removeCollaborator, deleteDirectory, hello } from "./helpers.js";

document.addEventListener('DOMContentLoaded', () => {
    
    hello();

    const detailsForm = document.querySelector("#details-form");
    const repositoryName = detailsForm.dataset.name;
    const repositoryDescription = detailsForm.dataset.description;
    const repositorypk = detailsForm.dataset.pk;
    detailsForm.querySelector("#id_name").value = repositoryName;
    detailsForm.querySelector("#id_description").value = repositoryDescription;

    //DELETE REPOSITORY
    var deleteBtn = document.querySelector("#delete-repository");
    deleteBtn.onclick = () => {
        deleteDirectory(repositorypk);
        window.location.href = "/dashboard";
    }

    //REMOVE COLLABORATORS
    document.querySelectorAll(".remove-collaborator").forEach(btn => {
        btn.onclick = () => {
            btn.parentElement.style.display = 'none';
            removeCollaborator(btn.dataset.collaborator, repositorypk);
        }
    })

    //ADD COLLABORATORS
    var addCollaboratorBtn = document.querySelector("#add-collaborator-btn");
    addCollaboratorBtn.onclick = () => {
        let modal = document.querySelector("#search-form-modal");
        modal.style.display = "grid";

        window.onclick = function(event) {
            if (event.target == modal) {
              modal.style.display = "none";
            }
        }
    }

    var addCollaboratorInput = document.querySelector("#input-search");
    addCollaboratorInput.addEventListener("input", () => {
        let text = addCollaboratorInput.value;
        let users = searchUsers(text);
        let usersListContainer = document.querySelector("#user-search-results-container");
        if(users != null) {
            users.forEach(user => {
                let userContainer = document.querySelector("#user-container-template").cloneNode(true);
                //set user's profile picture
                userContainer.querySelector(".avatar-sm").setAttribute("src", user.avatar);
                //set user's name
                userContainer.querySelector("p").innerHTML = user.username;
                userContainer.querySelector("button").setAttribute("data-collaborator", user.pk);
            })
            
        }
        

    });

})