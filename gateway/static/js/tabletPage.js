function getMicrophone(startRecording = true) {
    if (startRecording) {
        console.log("Inizio ad ascoltare...")
        fetch('/startListening')
            .then(data => console.log(data.text()))
    } else {
        console.log("Smetto di ascoltare...")
        fetch('/stopListening')
            .then(data => console.log(data.text()))
            .then(data => appendMessage(data))
            .then(() => recordVoice());
    }
}

const mic = document.getElementById('mic');
let isRecording = false;
mic.addEventListener('click', () => {
    if (!isRecording) {
        mic.src = '/static/img/recordingMic.png';
        getMicrophone();
        isRecording = true;
    } else {
        mic.src = '/static/img/Mic.png';
        getMicrophone(false);
        isRecording = false;
    }
});