document.getElementById("upload-form").addEventListener("submit", function(event) {
    event.preventDefault();

    var fileInput = document.getElementById("file-input");
    var file = fileInput.files[0];

    var formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display the contents of the uploaded file
        var fileContents = document.getElementById("file-contents");
        fileContents.innerHTML = `<p>File name: ${data.filename}</p>`;

        // TODO: Add code to display the contents of the uploaded file
    });
});