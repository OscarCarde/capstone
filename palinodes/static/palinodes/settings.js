import { addCollaborator, removeCollaborator, deleteDirectory, hello } from "./helpers.js";
var repositorypk;

document.addEventListener('DOMContentLoaded', () => {
    
    hello();

    const detailsForm = document.querySelector("#details-form");
    const repositoryName = detailsForm.dataset.name;
    const repositoryDescription = detailsForm.dataset.description;
    repositorypk = detailsForm.dataset.pk;
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

    var inputSearch = document.querySelector("#input-search");
    inputSearch.addEventListener("input", () => {
        let text = inputSearch.value;
        searchUsers(text);
    })
})

async function searchUsers(value) {
    var usersListContainer = document.querySelector("#user-search-results-container");
    usersListContainer.replaceChildren();
    if(value != "") {
        //retreive first 10 users that have the substring value
        await fetch(`/search-collaborators/${value}`)
        .then(response => response.json())
        .then(data => {
            data.users.forEach(user => {
                let userContainer = document.querySelector("#user-container-template").cloneNode(true);
                //set user's profile picture
                if(user.avatar != null) {
                    userContainer.querySelector(".avatar-sm").setAttribute("src", user.avatar);
                }
                //set user's name
                userContainer.querySelector(".collaborator-username").innerHTML = user.username;

                userContainer.style.display = "flex";
                userContainer.id = "";
                usersListContainer.append(userContainer);

                userContainer.addEventListener("click", () => {
                    addCollaborator(user.pk, repositorypk);
                })
            })
        });
    }
}