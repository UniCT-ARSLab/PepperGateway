console.log(document.getElementById('autonomous-btn').classList.contains("bg-red-400"))

function turnOn(btnColor, btnMovement) {
    console.log("[INFO] Turning On...")
    btnColor.classList.toggle("bg-gray-200");
    btnColor.classList.add("bg-red-400");
    btnMovement.classList.toggle("translate-x-0");
    btnMovement.classList.add("translate-x-3.5");
}

function turnOff(btnColor, btnMovement) {
    console.log("[INFO] Turning Off...")
    btnColor.classList.remove("bg-red-400");
    btnColor.classList.add("bg-gray-200");
    btnMovement.classList.remove("translate-x-3.5");
    btnMovement.classList.add("translate-x-0");
}

async function setAutonomousState(state) {
    fetch('/setAutonomous', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: state
        })
    })
    .then(data => data.text())
    .then(data => console.log(data));
}

function autonomousBtn() {
    const btnColor = document.getElementById('autonomous-btn');
    const btnMovement = document.getElementById('autonomous-span');
    const isActive = btnColor.classList.contains("bg-red-400")
    if (isActive) {
        turnOff(btnColor, btnMovement)
        console.log("Autonomous is now off, make a call to the server to turn off")
        setAutonomousState(false);
    } else {
        turnOn(btnColor, btnMovement)
        console.log("Autonomous is now on, make a call to the server to turn on")
        setAutonomousState(true);
    }
}

fetch('/getBattery')
    .then(data => data.text())
    .then(data => document.getElementById('battery').innerHTML = data);
const item = document.getElementById('battery');
if (item >= '60') {
    item.classList.add('bg-green-100');
} else if (item.innerHTML < 60 && item.innerHTML > 30) {
    item.classList.add('bg-yellow-100');
} else {
    item.classList.add('bg-red-100');
}

fetch('/getAutonomous')
    .then(data => data.text())
    .then(data => {
        console.log(data);
        if (data == "True") {
            console.log("[AUTONOMOUS] ON")
            turnOn(document.getElementById('autonomous-btn'), document.getElementById('autonomous-span'));
        } else {
            console.log("[AUTONOMOUS] OFF")
            turnOff(document.getElementById('autonomous-btn'), document.getElementById('autonomous-span'));
        }
    });

// fetch('/getCamera')
//     .then(data => data.text())
//     .then(data => {
//         if (data == 'true') {
//             turnOn(document.getElementById('autonomous-btn'), document.getElementById('autonomous-span'));
//         } else {
//             turnOff(document.getElementById('autonomous-btn'), document.getElementById('autonomous-span'));
//         }
//     })
