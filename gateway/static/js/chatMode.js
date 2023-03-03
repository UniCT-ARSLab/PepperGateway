function toServer(text) {
    var data = new FormData();
    data.append("json", JSON.stringify(text));
    fetch("http://0.0.0.0:5000/getAnswer",
    {
        method: "POST",
        body: data
    })
    .then(data => data.text())
    .then((res) => { console.log(res) })
}

function createMessage(text) {
    const message = document.createElement('div');
    message.classList.add('chat-message');
    const div = document.createElement('div');
    div.classList.add('flex', 'items-end', 'justify-end');
    const div2 = document.createElement('div');
    div2.classList.add('flex', 'flex-col', 'space-y-2', 'text-xs', 'max-w-xs', 'mx-2', 'order-1', 'items-end');
    const div3 = document.createElement('div');
    const span = document.createElement('span');
    span.classList.add('px-4', 'py-2', 'rounded-lg', 'inline-block', 'rounded-br-none', 'bg-red-400', 'text-white');
    span.innerText = text;
    div3.append(span);
    div2.append(div3);
    div.append(div2);
    message.append(div);
    return message;
}
function sendMessage() {
    const text = document.getElementById('text').value;
    const messages = document.getElementById('messages'); // Messages Area
    messages.append(createMessage(text));
    messages.scrollTop = messages.scrollHeight;
    document.getElementById('text').value = '';
    toServer(text); // Send message to server
}