const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

export function leaveRepository(repositorypk) {
    fetch(`/api/leave/${repositorypk}`, {
        method: 'POST',
        headers: {
            'ContentType': 'application/json',
            'X-CSRFtoken': csrftoken,
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
}

export async function addCollaborator(userpk, repositorypk) {
    //add collaborator with api call
    await fetch("/api/add-collaborator", {
        method: 'POST',
        headers: {
            'Content-Type': "application/json",
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
    fetch(`/api/remove-collaborator/${repositorypk}`, {
        method: 'post',
        headers: {
            'Content-Type': "application/json",
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
    fetch("/api/delete-directory", {
        method: 'POST',
        headers: {
            'Content-Type': "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'directorypk': pk,
        })

    })
}

export async function deleteFile(pk) {
    await fetch("/api/delete-file", {
        method: 'POST',
        headers: {
            'Content-Type': "application/json",
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