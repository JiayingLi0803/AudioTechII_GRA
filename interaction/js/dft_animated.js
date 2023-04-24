// Create an AudioContext
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

// Define the number of sinusoids to generate
const numSinusoids = 5;

// Create an array of OscillatorNodes for each sinusoid
const oscillators = new Array(numSinusoids);
for (let i = 0; i < numSinusoids; i++) {
  oscillators[i] = audioCtx.createOscillator();
}

// Connect the oscillators to the AudioContext
for (let i = 0; i < numSinusoids; i++) {
  oscillators[i].connect(audioCtx.destination);
}

// Function to generate a sinusoid with a specified frequency and amplitude
function generateSinusoid(frequency, amplitude) {
  // Set the frequency and type of waveform (sine) for the oscillator
  const oscillator = audioCtx.createOscillator();
  oscillator.type = 'sine';
  oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);

  // Set the amplitude (volume) of the oscillator using a GainNode
  const gainNode = audioCtx.createGain();
  gainNode.gain.setValueAtTime(amplitude, audioCtx.currentTime);

  // Connect the oscillator to the GainNode and the GainNode to the AudioContext
  oscillator.connect(gainNode);
  gainNode.connect(audioCtx.destination);

  // Start the oscillator and return it
  oscillator.start();
  return oscillator;
}

// Function to stop all oscillators
function stopAllOscillators() {
  for (let i = 0; i < numSinusoids; i++) {
    oscillators[i].stop();
  }
}

// Add event listeners to the buttons to generate and play the sinusoids
for (let i = 0; i < numSinusoids; i++) {
  const button = document.getElementById(`button-${i}`);
  button.addEventListener('click', () => {
    const frequency = Number(document.getElementById(`frequency-${i}`).value);
    const amplitude = Number(document.getElementById(`amplitude-${i}`).value);
    const oscillator = generateSinusoid(frequency, amplitude);
    oscillators[i] = oscillator;
  });
  button.addEventListener('mouseup', stopAllOscillators);
}
