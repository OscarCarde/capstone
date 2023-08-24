document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.directories').forEach(directory => {
        console.log(directory.dataset.pk)
        directory.addEventListener('click', () => {
            loadDirectoryContents(directory.dataset.pk)
        });
    })
})

async function loadDirectoryContents(directory_pk) {
    document.querySelector("#contents").replaceChildren()
    //get the contents from the directory with primary key directory_pk
    //create a list of elements with the directory's contents
    await fetch(`/directory/${directory_pk}`)
    .then(response => response.json())
    .then(data => {
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
            let hiddenfileIcon = document.querySelector("#file-icon");
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