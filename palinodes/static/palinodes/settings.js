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
    var addCollaboratorInput = document.querySelector("#input-search");
    addCollaboratorInput.addEventListener("input", () => {
        let text = addCollaboratorInput.value;
        searchUsers(text);
    });

})