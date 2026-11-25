export async function startCamera(videoElement) {
    const constraints = {
        audio: false,
        video: {
            facingMode: { ideal: "environment" }
        },
    };

    const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
    videoElement.srcObject = mediaStream;
    try {
        await videoElement.play();
    } catch (err) {
        mediaStream.getTracks().forEach(track => track.stop());
        videoElement.srcObject = null;
        throw err;
    }
    return mediaStream;
}

export function stopCamera(mediaStream) {
    mediaStream?.getTracks().forEach(track => track.stop());
}

export function takeSnapshot(videoElement, maxSize = 800) {
    const scale = Math.min(1, maxSize/Math.max(videElement.videoWidth, videoElement.videoHeight))
    const canvas = document.createElement("canvas");
    canvas.width = Math.round(videoElement * scale);
    canvas.height = Math.round(videoElement.videoHeight * scale);
    canvas.getContext("2d").drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    return new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.85));
}