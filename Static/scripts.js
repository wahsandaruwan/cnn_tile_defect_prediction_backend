// -----Variabels-----
let video = document.querySelector("#video");
let canvas = document.querySelector("#canvas");
let result = document.querySelector("#result");

// Hide canvas
canvas.style.display = "none";

// -----Start video-----
navigator.mediaDevices
  .getUserMedia({
    video: true,
    audio: false,
  })
  .then((stream) => {
    video.srcObject = stream;
  });

// Capture image every 5 seconds
setInterval(function () {
  // Show canvas
  canvas.style.display = "";

  // Get canvas context
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);

  // Save to a file
  canvas.toBlob(function (blob) {
    // Generate a file
    let file = new File([blob], "shot.jpg", { type: "image/jpeg" });

    // Create form data object
    let data = new FormData();

    // Append the file
    data.append("file", file);

    // Create request object
    let request = new XMLHttpRequest();
    request.open("POST", "http://127.0.0.1:5000/predict");

    // Upload progress event
    request.upload.addEventListener("progress", function (e) {
      let percent_complete = (e.loaded / e.total) * 100;

      // Percentage of upload completed
      console.log(percent_complete);
    });

    // AJAX request finished event
    request.addEventListener("load", function (e) {
      // HTTP status message
      console.log(request.status);

      // Response
      let final = JSON.parse(request.response).result;

      // Update html
      result.textContent = final;
    });

    // Send POST request
    request.send(data);
  }, "image/jpeg");
}, 10000);
