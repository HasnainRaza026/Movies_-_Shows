const socket = io(); // No namespace unless required

socket.on("connect", () => {
    console.log("WebSocket connected!");
});

document.getElementById("movieInput").addEventListener("input", function () {
    let query = this.value.trim();
    if (query.length > 0) {
        socket.emit("search_query", query);
        // console.log("Query sent to server:", query); // For Debug
    }
});

socket.on("search_results", function (data) {
    // console.log("Received data from server:", data); // For Debug
    let suggestions = document.getElementById("suggestions");
    suggestions.innerHTML = "";

    if (data.length > 0) {
        data.forEach(movie => {
            let item = document.createElement("li");
            item.classList.add("list-group-item", "d-flex", "align-items-center");

            let poster = document.createElement("img");
            poster.src = movie.poster || "https://via.placeholder.com/50";
            poster.alt = movie.title;
            poster.style.width = "50px";
            poster.style.height = "75px";
            poster.classList.add("me-3");

            let text = document.createElement("span");
            text.textContent = `${movie.title} (${movie.year})`;

            // Click event
            item.addEventListener("click", () => {
                document.getElementById("movieInput").value = `${movie.title} ${movie.movie_id}`;
                suggestions.style.display = "none";
            });            

            item.appendChild(poster);
            item.appendChild(text);
            suggestions.appendChild(item);
        });

        suggestions.style.display = "block";
        suggestions.style.maxHeight = "200px";
        suggestions.style.overflowY = "auto";
    } else {
        suggestions.style.display = "none";
    }
});
