//import WaveSurfer from '/static/palinodes/node_modules/wavesurfer.js/dist/wavesurfer.js';
import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'
import { deleteDirectory, deleteFile } from './helpers.js';

const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
const user = document.querySelector("#loggedin-user").dataset.username;

document.addEventListener('DOMContentLoaded', function() {
    //NEW DIRECTORY FORM
    let newDirectory = document.querySelector("#new-directory");
    newDirectory.addEventListener('click', () => {
        //display new directory form as modal
        var modal = document.querySelector("#new-directory-modal");
        newDirectory.style.display = "none";
        modal.style.display = "block";
        
        window.onclick = function(event) {
            if (event.target == modal) {
              modal.style.display = "none";
              newDirectory.style.display = "block";
            }
        }
        //add event listener to form for saving new directory
        var submit = document.querySelector("#new-directory-form");
        submit.addEventListener('submit', () => {
            //call function to create new directory
            var newDirectoryName = document.querySelector("#new-directory-name").value;
            if(newDirectoryName != null) {
                createNewDirectory(newDirectoryName);
            }
        });
    });

    const repositorypk = document.querySelector("#contents").dataset.pk;
    //LOAD CONTENTS
    loadDirectoryContents(repositorypk);

    //LOAD CHAT
    loadChat(repositorypk);

    //NEW COMMENT
    //TODO: Display new comment without fetch call to keep audio track loaded
    document.querySelector("#new-comment").onsubmit = async () => {
        var comment = document.querySelector("#comment-input").value;
        console.log(comment);
        await fetch("/new-comment", {
            method: 'POST', 
            headers: {
                'ContentType':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                "comment": comment,
                "repositorypk": repositorypk,
            })
        })
    }
    
});





async function loadChat(repositorypk) {
    console.log(user);
    fetch(`/repository/${repositorypk}/comments`)
    .then(response => response.json())
    .then(data => {
        var container = document.querySelector("#chat");
        var commentTemplate = document.querySelector("#comment-template");
        var commentTemplateSelf = document.querySelector("#comment-template-self");

        data.comments.forEach(comment => {
            console.log(comment.username);
            if(comment.username != user) {
                var commentContainer = commentTemplate.cloneNode(true);
                commentContainer.querySelector(".commenter").innerHTML = comment.username;
            }
            else {
                var commentContainer = commentTemplateSelf.cloneNode(true);
            }
            commentContainer.id = "";
            commentContainer.style.display = "flex";
            commentContainer.querySelector(".comment").innerHTML = comment.comment;
            commentContainer.querySelector(".timestamp").innerHTML = comment.when;
            
            container.prepend(commentContainer);
            container.scrollTop = container.scrollHeight;
        }) 
    })
}

async function createNewDirectory(newDirectoryName) {
    //post to api to create new directory from formData
    //with the current directory as parent
    var parent_pk = document.querySelector("#parent").dataset.pk;

    await fetch("/new-directory", {
        method: 'POST',
        headers: {
            'ContentType':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            "name": newDirectoryName,
            'parent_pk': parent_pk,
        }),
    })
    .then(response => response.json())
    .then(data => {
        loadDirectoryContents(data.directory_pk);
    })
    
}

async function loadDirectoryContents(directory_pk) {
    document.querySelector("#contents").replaceChildren();
    var deleteBtnTemplate = document.querySelector("#delete-btn-template");

    //FILE UPLOAD FORM HANDLING
    let form = document.querySelector("#file-form");
    form.onsubmit = async event => {
        event.preventDefault();
        var file = document.querySelector("#file-input");
        var data = new FormData();

        data.append('file', file.files[0]);
        console.log(file.files[0]);
        data.append('parentpk', directory_pk);
        console.log(directory_pk);
        console.log(data);

        await fetch("/new-file", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: data,
        })
        .then(response => response.json())
        .then(message => {
            console.log(message.message);
            file.value = null;
            loadDirectoryContents(directory_pk);
        })
        
    };

    //get the contents from the directory with primary key directory_pk
    //create a list of elements with the directory's contents
    await fetch(`/directory/${directory_pk}`)
    .then(response => response.json())
    .then(data => {

        //hidden current directory data
        var currentDirectory = document.createElement("div");
        currentDirectory.style.display = "none";
        currentDirectory.setAttribute("id", "parent");
        currentDirectory.setAttribute("data-name", data.current.name);
        currentDirectory.setAttribute("data-pk", data.current.pk);
        document.getElementById("contents").append(currentDirectory);


        // folder link to return to parent directory
        if(data.parent != null) {
            let parent = document.createElement("div");
            let hiddenfolderIcon = document.querySelector("#folder-icon");
            let folderIcon = hiddenfolderIcon.cloneNode(true);
            folderIcon.style.display = "block";
            let directory = document.createElement('p');
            directory.innerHTML = ". .";
            parent.append(folderIcon, directory);
            parent.setAttribute("data-pk", data.parent.pk);
            parent.className = "directories file-entries clickable";
            parent.addEventListener('click', () => {
                loadDirectoryContents(parent.dataset.pk)
            });
            document.getElementById("contents").append(parent);
        }


        
        data.subdirectories.forEach(subdirectory => {
            //add the link to the parent directory
            //add each subdirectory in the current directory to the file structure in the DOM
            let container = document.createElement('div');

            //FOLDER ICON
            let hiddenfolderIcon = document.querySelector("#folder-icon");
            let folderIcon = hiddenfolderIcon.cloneNode(true);
            folderIcon.style.display = "block";

            //DELETE FOLDER BUTTON
            let deleteBtn = deleteBtnTemplate.cloneNode(true);
            deleteBtn.id = "";
            deleteBtn.style.display = "block";
            deleteBtn.onclick = () => {
                container.remove();
                deleteDirectory(subdirectory.pk);
            }


            let directory = document.createElement('p');
            directory.innerHTML = subdirectory.name;
            directory.className = "clickable";
            container.append(folderIcon, directory, deleteBtn);
            container.setAttribute("data-pk", subdirectory.pk);
            container.className = "directories file-entries";
            directory.addEventListener('click', () => {
                loadDirectoryContents(container.dataset.pk)
            });

            document.getElementById("contents").append(container);
            
            

        })
        data.files.forEach(file => {
            let container = document.createElement('div');
            var wavesurfer;

            //DELETE FOLDER BUTTON
            let deleteBtn = deleteBtnTemplate.cloneNode(true);
            deleteBtn.id = "";
            deleteBtn.style.display = "block";
            deleteBtn.onclick = () => {
                container.remove();
                deleteFile(file.pk);
            }

            var filename = document.createElement('p');
            filename.className = "clickable";
            filename.style.display = "block";
            filename.innerHTML = file.filename;

            if(file.is_audiofile){
                var soundwave = document.querySelector("#soundwave")
                var hiddenfileIcon = document.querySelector("#audiofile-icon");
                filename.addEventListener('click', () => {
                    soundwave.replaceChildren();
                    wavesurfer = WaveSurfer.create({
                        container: '#soundwave',
                        waveColor: '#ffffff',
                        progressColor: '#999999',
                        autoplay: true,
                        url: file.fileurl,
                        mediaControls: true,
                    });

                    wavesurfer.on('interaction', () => {
                        wavesurfer.play();
                    });

                    wavesurfer.play();
                });
            }
            else {
                var hiddenfileIcon = document.querySelector("#file-icon");
                filename.addEventListener( "click", () => {
                    const newWindow = window.open(file.fileurl, file.filename, `width=600, height=600`);

                    // Make sure the new window was successfully opened
                    if (newWindow) {
                        newWindow.focus();
                    } else {
                        alert('Popup blocked! Please allow popups for this site.');
                    }
                })
                
            }

            let fileIcon = hiddenfileIcon.cloneNode(true);
            fileIcon.style.display = "block";

            container.append(fileIcon, filename, deleteBtn);
            container.className = "audiofile file-entries";
            document.getElementById("contents").append(container);
        })
        //LOAD FIRST AUDIO FILE IF PRESENT
        let audiofile = document.querySelector(".audiofile");
        if(audiofile != null) {
            audiofile.click();
        }
    })
}