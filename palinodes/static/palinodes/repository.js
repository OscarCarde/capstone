document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.directories').forEach(directory => {
        directory.addEventListener('click', () => {
            loadDirectoryContents(this.dataset.pk)
        });
    })
})

function loadDirectoryContents(directory_pk) {
    document.querySelector("#contents").replaceChildren()
    //get the contents from the directory with primary key directory_pk
    //create a list of elements with the directory's contents
    fetch(`/directory/${directory_pk}`)
    .then(response => response.json)
    .then(data => {
        data.subdirectories.forEach(subdirectory => {
            let container = document.createElement('div');
            //TODO: find out how to add the folder icon 
            let folderIcon = document.getElementById("folder-icon").cloneNode(true);
            folderIcon.style.display = "block";
            let directory = document.createElement('p');
            directory.innerHTML = subdirectory.name;
            container.append(folderIcon, directory);
            container.setAttribute("data-pk", subdirectory.pk);
            container.className = "directories file-entries";
            document.getElementById("contents").append(container);
        })
        data.files.forEach(file => {
            let container = document.createElement('div');
            let fileIcon = document.getElementById("file-icon").cloneNode(true);
            fileIcon.style.display = "block";
            let filename = document.createElement('p');
            filename.innerHTML = file.filename;
            container.append(fileIcon, filename);
            container.className = "file-entries";
            document.getElementById("contents").append(container);
        })
    })
}