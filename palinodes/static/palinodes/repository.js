//import WaveSurfer from '/static/palinodes/node_modules/wavesurfer.js/dist/wavesurfer.js';
import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'
import TimelinePlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/timeline.esm.js'

const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

document.addEventListener('DOMContentLoaded', function() {
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

    document.querySelectorAll('.directories').forEach(directory => {
        console.log(directory.dataset.pk)
        directory.addEventListener('click', () => {
            loadDirectoryContents(directory.dataset.pk)
        });
    })

    document.querySelectorAll('.audiofile').forEach(audiofile => {
        audiofile.addEventListener('click', () => {
            document.querySelector("#soundwave").replaceChildren();
            const wavesurfer = WaveSurfer.create({
                container: '#soundwave',
                waveColor: '#ff000099',
                progressColor: '#660000',
                autoplay: true,
                hideScrollbar: false,
                url: audiofile.dataset.fileurl,
                mediaControls: true,
              });

              wavesurfer.on('interaction', () => {
                wavesurfer.play();
              });

              /*wavesurfer.on('finish', () => {
                pause.style.display = 'none';
                play.style.display = 'block';
                wavesurfer.setTime(0);
              })*/
              
        });
    });
    
});


async function createNewDirectory(newDirectoryName) {
    //post to api to create new directory from formData
    //with the current directory as parent
    parent_pk = document.querySelector("#parent").dataset.pk;
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
    document.querySelector("#contents").replaceChildren()
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
            let hiddenfolderIcon = document.querySelector("#folder-icon");
            let folderIcon = hiddenfolderIcon.cloneNode(true);
            folderIcon.style.display = "block";
            let directory = document.createElement('p');
            directory.innerHTML = subdirectory.name;
            container.append(folderIcon, directory);
            container.setAttribute("data-pk", subdirectory.pk);
            container.className = "directories file-entries clickable";
            container.addEventListener('click', () => {
                loadDirectoryContents(container.dataset.pk)
            });
            document.getElementById("contents").append(container);
        })
        data.files.forEach(file => {
            let container = document.createElement('div');
            if(file.is_audiofile){
                var hiddenfileIcon = document.querySelector("#audiofile-icon");
                container.addEventListener('click', () => {
                    let audio = document.querySelector('audio');
                    audio.setAttribute("src", file.fileurl);
                    audio.setAttribute("controls", "");
                });
            }
            else {
                var hiddenfileIcon = document.querySelector("#file-icon");
            }
            let fileIcon = hiddenfileIcon.cloneNode(true);
            fileIcon.style.display = "block";
            let filename = document.createElement('p');
            filename.innerHTML = file.filename;
            container.append(fileIcon, filename);
            container.className = "file-entries clickable";
            document.getElementById("contents").append(container);
        })
    })
}