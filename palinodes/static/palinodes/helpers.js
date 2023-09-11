const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

export async function searchUsers(value) {
    //retreive first 10 users that have the substring value
    const response = await fetch(`search-collaborators/${value}`);
    const data = await response.json();
    return data.users;
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