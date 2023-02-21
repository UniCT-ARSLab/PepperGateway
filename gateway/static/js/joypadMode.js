var ws = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port + "/ws");

ws.onopen = function () { console.log('WS Connected'); }
ws.onclose = function () { console.log('WS Disconnected'); }
ws.onmessage = function (event) { console.log("Received data"); }

function doSend(message, msg_type) {

    ws.send(JSON.stringify({
        msg_type: msg_type,
        data: message
    }))
    // setInterval(function() {
    //     ws.send(JSON.stringify({
    //         msg_type: msg_type,
    //         data: message
    //     }));
    // }, 2000);
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
            const normalised = scale(value, -50, 50, -1, 1);
            const msg_type = direction["y"] === undefined ? "rotate" : "move_forward";
            // console.log(msg_type + " : " + normalised);
            // console.log("Message Type: " + msg_type)

            doSend(normalised, msg_type);
        }
    });

    joystick.on('end', function(evt, data) {
        //debug(data);

            if(data.el.id=="nipple_0_0"){
                doSend(0, "move_forward");
            } else{
                doSend(0, "rotate");
            }
        });


}

function createNipple(evt) {
    var type = typeof evt === 'string' ?
        evt : evt.target.getAttribute('data-type');
    // if (joystick) {
    //   joystick.destroy();
    // }
    joystick = nipplejs.create(joysticks[type]);
    bindNipple();
}

function scale (number, inMin, inMax, outMin, outMax) {
	return (number - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
}



