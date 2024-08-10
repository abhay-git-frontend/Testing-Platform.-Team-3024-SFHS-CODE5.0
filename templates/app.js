const video = document.getElementById('video');
const canvas = document.getElementById('overlay');
const canvasContext = canvas.getContext('2d');

// Load face-api.js models
Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
    faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
    faceapi.nets.faceRecognitionNet.loadFromUri('/models')
]).then(() => {
    console.log("Models loaded successfully.");
    // Setup the video stream and start face detection
    startCamera();
});

function startCamera() {
    document.getElementById('details-section').classList.add('hidden');
    document.getElementById('camera-section').classList.remove('hidden');

    navigator.mediaDevices.getUserMedia({
        video: true
    }).then(stream => {
        video.srcObject = stream;
        video.play();
    }).catch(err => {
        console.error("Error accessing camera: ", err);
    });

    video.addEventListener('play', () => {
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(canvas, displaySize);

        let faceDetected = false;

        // Load the alert sound
        const alertSound = new Audio('/static/alert.mp3');  // Make sure to have an 'alert.mp3' file in the static directory

        setInterval(async () => {
            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptors();
            const resizedDetections = faceapi.resizeResults(detections, displaySize);

            canvasContext.clearRect(0, 0, canvas.width, canvas.height);
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

            if (resizedDetections.length > 0) {
                faceDetected = true;
            } else {
                if (faceDetected) {
                    alertSound.play();
                }
                faceDetected = false;
            }
        }, 100);
    });
}

function startCamera() {
    document.getElementById('details-section').classList.add('hidden');
    document.getElementById('camera-section').classList.remove('hidden');

    navigator.mediaDevices.getUserMedia({
        video: true
    }).then(stream => {
        video.srcObject = stream;
        video.play();
    }).catch(err => {
        console.error("Error accessing camera: ", err);
    });
}
