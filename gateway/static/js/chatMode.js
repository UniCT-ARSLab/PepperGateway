async function setLiveListening(STATE) {
    fetch('/setLiveListening', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: STATE
        })
    })
}

function setLiveBtn() {
    const buttonColor = document.getElementById('stream-btn');
    const buttonMovement = document.getElementById('stream-span');
    let isOpen = buttonColor.classList.contains("bg-red-400")
    if (isOpen) { // Turn it off
        buttonColor.classList.remove("bg-red-400");
        buttonColor.classList.add("bg-gray-200");
        buttonMovement.classList.remove("translate-x-3.5");
        buttonMovement.classList.add("translate-x-0");
        console.log("Making a call to start audio stream")
        setLiveListening(true)
    } else { // Turn it on
        buttonColor.classList.toggle("bg-gray-200");
        buttonColor.classList.add("bg-red-400");
        buttonMovement.classList.toggle("translate-x-0");
        buttonMovement.classList.add("translate-x-3.5");
        console.log("Making a call to stop audio stream")
        setLiveListening(false)
    }
}

function createMessage(text, isUser = true) {
    let message = document.createElement('div');
    let div = document.createElement('div');
    let div2 = document.createElement('div');
    let div3 = document.createElement('div');
    let span = document.createElement('span');

    message.classList.add('chat-message');
    span.innerText = text;

    if (isUser) {
        div.classList.add('flex', 'items-end', 'justify-end');
        div2.classList.add('flex', 'flex-col', 'space-y-2', 'text-xs', 'max-w-xs', 'mx-2', 'order-1', 'items-end');
        span.classList.add('px-4', 'py-2', 'rounded-lg', 'inline-block', 'rounded-br-none', 'bg-red-400', 'text-white');
    } else {
        div.classList.add('flex', 'items-end');
        div2.classList.add('flex', 'flex-col', 'space-y-2', 'text-xs', 'max-w-xs', 'mx-2', 'order-2', 'items-start');
        span.classList.add('px-4', 'py-2', 'rounded-lg', 'inline-block', 'rounded-bl-none', 'bg-gray-300', 'text-gray-600');
    }

    div3.append(span);
    div2.append(div3);
    div.append(div2);
    message.append(div);

    return message;
}

function appendMessage(text, isUser = true) {
    // Append message to chat after create it by createMessage()
    console.log("[INFO] Append message: " + text);
    const messages = document.getElementById('messages');
    messages.append(createMessage(text, isUser));
    messages.scrollTop = messages.scrollHeight;
    document.getElementById('text').value = '';
    if (isUser) getAnswer(text);
}

function getAnswer(text) { // Send text to server
    console.log("[INFO] Call /getAnswer for text: " + text)
    fetch('/getAnswer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: text
        })
    })
    .then(response => response.json())
    .then(response => JSON.stringify(response["data"]))
    .then(response => appendMessage(response.replace(/"|'/g, ''), false))
}

function getMicrophone(startRecording = true) {
    if (startRecording) {
        console.log("[INFO] Call /startListening")
        fetch('/startListening')
            .then(data => console.log(data.text()))
    } else {
        console.log("[INFO] Call /stopListening")
        fetch('/stopListening')
            .then(data => data.text())
            .then(data => appendMessage(data))
    }
}

function recordVoice() {
    const isRecording = document.getElementById('ping');
    if (!isRecording) {
        console.log("Inizio a registrare...")
        const div = document.getElementById('input-btn');
        const span = document.createElement('span');
        span.setAttribute("id", "ping")
        span.classList.add('animate-ping', 'outline', 'outline-offset-2', 
            'outline-red-500', 'rounded-full', 'absolute', 'inset-y-0', 
            'bg-red-400', 'ring-opacity-5', 'flex', 'items-center', 'h-12', 'w-12');
        div.prepend(span);
        getMicrophone();
    } else {
        console.log("Smetto di registrare...")
        isRecording.remove();
        getMicrophone(false);
    }
}