const audioContext = new (window.AudioContext || window.webkitAudioContext)();

const waveType = document.getElementById("waveType");
const frequencySlider = document.getElementById("frequency");
const frequencyValue = document.getElementById("frequencyValue");
const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const canvas = document.getElementById("waveformCanvas");
const canvasCtx = canvas.getContext("2d");

let oscillator;

function createOscillator() {
    oscillator = audioContext.createOscillator();
    oscillator.type = waveType.value;
    oscillator.frequency.value = frequencySlider.value;
    oscillator.connect(audioContext.destination);
}

function updateFrequency() {
    if (oscillator) {
        oscillator.frequency.value = frequencySlider.value;
    }
    frequencyValue.innerText = frequencySlider.value;
    drawWaveform();
}

function drawWaveform() {
    const width = canvas.width;
    const height = canvas.height;
    const centerY = height / 2;

    canvasCtx.clearRect(0, 0, width, height);
    canvasCtx.beginPath();
    canvasCtx.moveTo(0, centerY);

    const wave = waveType.value;
    const frequency = parseFloat(frequencySlider.value);
    const numPeriods = 3;
    const numPoints = width;
    const angularFrequency = 2 * Math.PI * frequency;

    for (let x = 0; x <= numPoints; x++) {
        const t = x / width * numPeriods * (1 / frequency);
        let y;

        switch (wave) {
            case 'sine':
                y = centerY - Math.sin(angularFrequency * t) * centerY;
                break;
            case 'square':
                y = centerY - (Math.sign(Math.sin(angularFrequency * t)) * centerY);
                break;
            case 'sawtooth':
                y = centerY - ((2 * (t * frequency - Math.floor(0.5 + t * frequency))) * centerY);
                break;
        }

        canvasCtx.lineTo(x, y);
    }

    canvasCtx.stroke();
}

waveType.addEventListener("change", () => {
    if (oscillator) {
        oscillator.stop();
        createOscillator();
        oscillator.start();
    }
    drawWaveform();
});

frequencySlider.addEventListener("input", updateFrequency);

startButton.addEventListener("click", () => {
    createOscillator();
    oscillator.start();
});

stopButton.addEventListener("click", () => {
    if (oscillator) {
        oscillator.stop();
        oscillator = null;
    }
});

updateFrequency();
