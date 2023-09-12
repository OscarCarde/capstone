const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;


export async function addCollaborator(userpk, repositorypk) {
    //add collaborator with api call
    await fetch("/add-collaborator", {
        method: 'POST',
        headers: {
            'ContentType': "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'newCollaboratorpk': userpk,
            'repositorypk': repositorypk
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        
    })
}
export function removeCollaborator(collaboratorpk, repositorypk) {
    //remove collaborator with api call
    fetch(`/remove-collaborator/${repositorypk}`, {
        method: 'post',
        headers: {
            'ContentType': "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'pk': collaboratorpk,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
}

export async function deleteDirectory(pk) {
    fetch("/delete-directory", {
        method: 'POST',
        headers: {
            'ContentType': "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'directorypk': pk,
        })

    })
}

export async function deleteFile(pk) {
    await fetch("/delete-file", {
        method: 'POST',
        headers: {
            'ContentType': "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'filepk': pk,
        })
        
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);  
    })
    
}

export function hello() {
    console.log("Hello, from helpers.js");
}