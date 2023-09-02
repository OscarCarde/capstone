document.addEventListener('DOMContentLoaded', () => {
    //Event listeners to toggle between recent/owned/collaborating repositories
        //recent
    document.querySelector("#recent-btn").onclick = () => {
        document.querySelectorAll(".owned-repositories").forEach(repository => {
            repository.style.display = "none";
        })
        document.querySelectorAll(".collaborating-repositories").forEach(repository => {
            repository.style.display = "none";
        })
        document.querySelectorAll(".all-repositories").forEach(repository => {
            repository.style.display = "block";
        })
    }
        //owned
    document.querySelector("#my-repositories-btn").onclick = () => {
        document.querySelectorAll(".owned-repositories").forEach(repository => {
            repository.style.display = "block";
        })
        document.querySelectorAll(".collaborating-repositories").forEach(repository => {
            repository.style.display = "none";
        })
        document.querySelectorAll(".all-repositories").forEach(repository => {
            repository.style.display = "none";
        })
    }
        //collab
    document.querySelector("#collaborating-btn").onclick = () => {
        document.querySelectorAll(".owned-repositories").forEach(repository => {
            repository.style.display = "none";
        })
        document.querySelectorAll(".collaborating-repositories").forEach(repository => {
            repository.style.display = "block";
        })
        document.querySelectorAll(".all-repositories").forEach(repository => {
            repository.style.display = "none";
        })
    }

    //Event listeners to toggle between Profile view and edit profile form

    const profileBanner = document.querySelector("#profile-banner");
    profileBanner.querySelector("button").onclick = () => {
        //hide all children of the profile banner
        profileBanner.querySelectorAll(".profile").forEach(node => {
            node.style.display = 'none';
        })
        //display the edit profile form
        let form = profileBanner.querySelector("form");
        form.style.display = 'flex';
        //set initial description value to current description for form
        let currentDescription = document.querySelector("#profile-description").dataset.description;
        document.querySelector("#id_description").value = currentDescription;

        //handle edit cancellation and toggle back to profile view
        form.querySelector("button").onclick = () => {
            profileBanner.querySelectorAll(".profile").forEach(node => {
                node.style.display = 'none';
            })
            profileBanner.querySelector("#profile-details").style.display = "flex";
        }
        
    }
    
})
