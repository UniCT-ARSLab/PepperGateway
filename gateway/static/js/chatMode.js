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

function appendMessage(text = NaN, isUser = true) {
    // Append message to chat after create it by createMessage()
    if (text == NaN) text = document.getElementById('text').value;
    console.log("appendMessage received: " + text);
    const messages = document.getElementById('messages');
    messages.append(createMessage(text, isUser));
    messages.scrollTop = messages.scrollHeight;
    document.getElementById('text').value = '';
    if (isUser) getAnswer(text);
}

function getAnswer(text) { // Send text to server
    fetch('/getAnswer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: text
        })
    })
    .then(data => data.text())
    .then(res => { appendMessage(res, false) })
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
    const ping = document.getElementById('ping');
    if (!ping) {
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
        ping.remove();
        getMicrophone(false);
    }
}