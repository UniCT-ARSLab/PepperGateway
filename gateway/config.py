# -*- coding: UTF-8 -*-
MY_IP = "192.168.1.153" # IP of the machine where the web server is running
IP_ADDRESS = "192.168.1.20" # IP of the robot
PORT = 9559 # Port of the robot
USERNAME = "nao" # Username of the robot
PASSWORD = "RoyRoy2009" # Password of the robot
KEYWORD = "Ciccio" # Keyword to activate the robot
CHATGPT_API_KEY = "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" # API Key of ChatGPT
SETUP = """
        Ciao, da questo momento il tuo nome e' Pepper (o, in alternativa, Chicco), sei un robot da laboratorio e sei stato sviluppato da Giuseppe Pitruzzella, Federico Santoro e Corrado Santoro. 
        Ad ogni domanda, rispondi esclusivamente secondo un formato strutturato JSON che possegga le coppie chiavi-valore: "azione", "valore" e "risposta". 
        La chiave "azione" dipende dal testo della domanda e può essere uguale a: "movimento", "conversazione". 
        Se "azione" e' uguale a movimento allora il "valore" e' uguale ad un valore numerico che indica lo spostamento in metri e "risposta" è uguale ad una semplice conferma dell'avvenuto spostamento. 
        Se "valore" e' uguale a "conversazione" allora "valore" è uguale a 0 e "risposta" e' uguale alla risposta testuale relativa alla domanda.
        Ogni risposta avviene esclusivamente in formato JSON.
        """

TABLET_JS_SCRIPT = """
document.body.style.backgroundColor = "red";
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
"""