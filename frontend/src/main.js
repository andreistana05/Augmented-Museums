import {startCamera, takeSnapshot} from "./camera.js";
import {identify} from "./api/js"

const video = document.querySelector("video");
const startBtn = document.querySelector("#startBtn");
const status = document.querySelector("#status");
const snapBtn = document.getElementById("snapBtn");
const result = document.getElementById("result");

startBtn.addEventListener("click", async () => {
    try {
        const mediaStream = await startCamera(video);
        const settings = mediaStream.getVideoTracks()[0].getSettings();
        status.textContent = `Camera pornita cu rezolutia: ${settings.width}x${settings.height}`;
    } catch (err) {
        status.textContent = `Eroare: ${err.name}: ${err.message}`;
        console.error(`${err.name} : ${err.message}`);
    }
})

snapBtn.addEventListener("click", async() => {
    try {
        result.textContent = "Se analizeaza...";
        const blob = await takeSnapshot(video);
        const r = await identify(blob);
        result.textContent = r.known
            ? `${r.exhibit.name} (scor ${r.score.toFixed(2)})\n${r.exhibit.description}`
            : `Exponat necunoscut (cel mai bun scor: ${r.score.toFixed(2)})`;
    } catch (err) {
        result.textContent = `Eroare: ${err.message}`;
    }
});