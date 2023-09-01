document.addEventListener('DOMContentLoaded', () => {
    //load dashboard
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
})
