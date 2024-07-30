var recordButton, stopButton, recorder;

window.onload = () => {
  recordButton = document.getElementById('recordButton');
  stopButton = document.getElementById('stopButton');

  // get audio stream from user's mic
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(function (stream) {
    recordButton.disabled = false;
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    recorder = new MediaRecorder(stream, {mimeType: 'audio/webm'});

    // listen to dataavailable, which gets triggered whenever we have
    // an audio blob available
    recorder.addEventListener('dataavailable', onRecordingReady);
  });
};

const startRecording = () => {
  recordButton.disabled = true;
  stopButton.disabled = false;

  recorder.start();
}

const stopRecording = () => {
  recordButton.disabled = false;
  stopButton.disabled = true;

  // Stopping the recorder will eventually trigger the `dataavailable` event and we can complete the recording process
  recorder.stop();
}

const onRecordingReady = async (e) => {
  const audio = document.getElementById('audio');
  // e.data contains a blob representing the recording
  const audioBlob = e.data;
  const formData = new FormData();
  console.log(typeof audioBlob);
  formData.append('voiceMessage', audioBlob, 'voiceMessage.webm');

                await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
  audio.src = URL.createObjectURL(e.data);
}