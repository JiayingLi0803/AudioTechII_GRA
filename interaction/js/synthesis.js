window.addEventListener('load', function () {
  var context = new (window.AudioContext || window.webkitAudioContext)();
  var oscillatorNodes = [];
  var canvas = document.getElementById('waveformCanvas');
  var ctx = canvas.getContext('2d');
  var signalTypeSelect = document.getElementById('signalType');
  var frequencySliders = [
    document.getElementById('frequency1'),
    document.getElementById('frequency2'),
    document.getElementById('frequency3'),
    document.getElementById('frequency4'),
    document.getElementById('frequency5')
  ];
  var amplitudeSliders = [
    document.getElementById('amplitude1'),
    document.getElementById('amplitude2'),
    document.getElementById('amplitude3'),
    document.getElementById('amplitude4'),
    document.getElementById('amplitude5')
  ];
  var playBtn = document.getElementById('playBtn');
  var stopBtn = document.getElementById('stopBtn');

  const freqtext1 = document.getElementById("freqShow1");
  const freqtext2 = document.getElementById("freqShow2");
  const freqtext3 = document.getElementById("freqShow3");
  const freqtext4 = document.getElementById("freqShow4");
  const freqtext5 = document.getElementById("freqShow5");
  const amptext1 = document.getElementById("ampShow1");
  const amptext2 = document.getElementById("ampShow2");
  const amptext3 = document.getElementById("ampShow3");
  const amptext4 = document.getElementById("ampShow4");
  const amptext5 = document.getElementById("ampShow5");

  // check waveform
  function drawWaveform(data, color) {
    var step = canvas.width / data.length;
    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);
    for (var i = 0; i < data.length; i++) {
      ctx.lineTo(i * step, canvas.height / 2 - (data[i] * (canvas.height / 2)));
    }
    ctx.strokeStyle = color;
    ctx.stroke();
  }

  // create oscillator
  function createOscillator(signalType, frequency, amplitude) {
    var oscillator = context.createOscillator();
    oscillator.type = signalType;
    oscillator.frequency.value = frequency;

    var gainNode = context.createGain();
    gainNode.gain.value = amplitude;

    oscillator.connect(gainNode);
    gainNode.connect(context.destination);

    return oscillator;
  }

  // stop all oscillators
  function stopAllOscillators() {
    for (var i = 0; i < oscillatorNodes.length; i++) {
      oscillatorNodes[i].stop();
    }
    oscillatorNodes = [];
  }

  // play button function
  playBtn.addEventListener('click', function () {
    stopAllOscillators();
    var signalType = signalTypeSelect.value;
    var frequencies = frequencySliders.map(function (slider) {
      return parseFloat(slider.value);
    });
    var amplitudes = amplitudeSliders.map(function (slider) {
      return parseFloat(slider.value);
    });

    for (var i = 0; i < 5; i++) {
      var frequency = frequencies[i];
      var amplitude = amplitudes[i];
      var oscillator = createOscillator(signalType, frequency, amplitude);
      oscillator.start();
      oscillatorNodes.push(oscillator);
    }
  });

  // stop button
  stopBtn.addEventListener('click', function () {
    stopAllOscillators();
  });

  // draw xticks and yticks
  function drawGraphBox() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'black';

    ctx.beginPath();
    ctx.moveTo(40, canvas.height - 20);
    ctx.lineTo(canvas.width - 10, canvas.height - 20);
    ctx.stroke();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    ctx.fillText('0', 40, canvas.height - 15);
    ctx.fillText('1', canvas.width / 4, canvas.height - 15);
    ctx.fillText('2', canvas.width / 2, canvas.height - 15);
    ctx.fillText('3', canvas.width * 3 / 4, canvas.height - 15);

    var amplitudeStep = (canvas.height - 10) / 4;
    ctx.beginPath();
    ctx.moveTo(40, 10);
    ctx.lineTo(40, canvas.height - 20);
    ctx.stroke();
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    // for (var j = 0; j < 5; j++) {
    //   var y = canvas.height - 10 - amplitudeStep * j;
    //   var amplitude = amplitudeSliders[j].value;
    //   ctx.fillText(amplitude, 35, y);
    // }
    ctx.fillText('1', 25, 20);
    ctx.fillText('0', 25, canvas.height /2 - 10);
    ctx.fillText('-1', 25, canvas.height - 20);


    ctx.textAlign = 'center';
    ctx.fillText('time (ms)', canvas.width - 30, canvas.height - 10);
    ctx.fillText('Ampitude', 25, 5);
  }

  // initialize graphbox
  drawGraphBox();

  // for each frequency slider change, update waveform
  frequencySliders.forEach(function (slider) {
    slider.addEventListener('input', updateWaveform);
  });

  // for each amplitude slider change, update waveform
  amplitudeSliders.forEach(function (slider) {
    slider.addEventListener('input', updateWaveform);
  });

  // for each type of signal, update waveform
  signalTypeSelect.addEventListener('change', updateWaveform);

  // update display text
  function updateText() {
    var frequencies = frequencySliders.map(function (slider) {
      return parseFloat(slider.value);
    });
    var amplitudes = amplitudeSliders.map(function (slider) {
      return parseFloat(slider.value);
    });

    freqShow1.innerText = frequencies[0];
    freqShow2.innerText = frequencies[1];
    freqShow3.innerText = frequencies[2];
    freqShow4.innerText = frequencies[3];
    freqShow5.innerText = frequencies[4];

    ampShow1.innerText = amplitudes[0];
    ampShow2.innerText = amplitudes[1];
    ampShow3.innerText = amplitudes[2];
    ampShow4.innerText = amplitudes[3];
    ampShow5.innerText = amplitudes[4];
  }

  // update waveform
  function updateWaveform() {
    updateText();

    var signalType = signalTypeSelect.value;
    var frequencies = frequencySliders.map(function (slider) {
      return parseFloat(slider.value);
    });
    var amplitudes = amplitudeSliders.map(function (slider) {
      return parseFloat(slider.value);
    });

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawGraphBox();

    var data = new Float32Array(context.sampleRate * 0.003);
    var t = 0;

    for (var i = 0; i < data.length; i++) {
      var sample = 0;
      for (var k = 0; k < 5; k++) {
        var frequency = frequencies[k];
        var amplitude = amplitudes[k];
        switch (signalType) {
          case 'sine':
            sample += Math.sin(2 * Math.PI * frequency * t) * amplitude;
            break;
          case 'square':
            sample += (Math.sin(2 * Math.PI * frequency * t) > 0) ? amplitude : -amplitude;
            break;
          case 'sawtooth':
            sample += (2 * (t * frequency - Math.floor(t * frequency + 0.5))) * amplitude;
            break;
          case 'triangle':
            sample += (2 * Math.abs(2 * (t * frequency - Math.floor(t * frequency + 0.5))) - 1) * amplitude;
            break;
        }
      }
      data[i] = sample / 5;
      t += 1 / context.sampleRate;
    }

    drawWaveform(data, '#0022ff');
  }

  // initialize waveform
  updateWaveform();
});