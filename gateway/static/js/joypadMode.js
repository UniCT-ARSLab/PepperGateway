var ws = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port + "/ws");

ws.onopen = function () { console.log('WS Connected'); }
ws.onclose = function () { console.log('WS Disconnected'); }
ws.onmessage = function () { console.log("Received data"); }
ws.onmessage = function (frame) { 
    var img = document.createElement("img");
    img.src = frame;
    img.classList.add("h-48 w-48");
    document.querySelector("#frame").appendChild(frame); 
}

function doSend(message, msg_type) {
    ws.send(JSON.stringify({
        msg_type: msg_type,
        data: message
    }))
};

// Ricorda di inizializzare metodi per l'errore e chiusura WebSocket
var joysticks = {
    forward_joystick: {
        zone: document.getElementById('static-forward'),
        lockY: true,
        color: 'blue'
    },
    rotate_joystick: {
        zone: document.getElementById('static-rotate'),
        lockX: true,
        color: 'red'
    }
};
var joystick;

createNipple('forward_joystick');
createNipple('rotate_joystick');

function bindNipple() {
    joystick.on('move', function(evt, data) {
        if (data["direction"]) {
            const direction = data["direction"];
            const value = (direction["y"] == "down" || direction["x"] == "right") ? -data["distance"] : data["distance"];
            const normalised = scale(value, -50, 50, -0.5, 0.5);
            const msg_type = direction["y"] === undefined ? "rotate" : "move_forward";

            doSend(normalised, msg_type);
        }
    });
    joystick.on('end', function(evt, data) { // Refactor this!!!
        if (data.el.id=="nipple_0_0"){
            doSend(0, "move_forward");
        } else {
            doSend(0, "rotate");
        }
    });
}

function createNipple(evt) {
    var type = typeof evt === 'string' ?
        evt : evt.target.getAttribute('data-type');
    joystick = nipplejs.create(joysticks[type]);
    bindNipple();
}

function scale (number, inMin, inMax, outMin, outMax) {
	return (number - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
}

