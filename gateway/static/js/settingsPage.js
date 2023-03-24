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
    const buttonColor = document.getElementById('autonomous-btn');
    const buttonMovement = document.getElementById('autonomous-span');
    if (buttonColor.classList.contains("bg-red-400")) { // Button is on
        buttonColor.classList.remove("bg-red-400");
        buttonColor.classList.add("bg-gray-200");
        buttonMovement.classList.remove("translate-x-3.5");
        buttonMovement.classList.add("translate-x-0");
        console.log("Autonomous is now off, make a call to the server to turn off")
        setAutonomousState(false);
        
    } else { // Button is off
        buttonColor.classList.toggle("bg-gray-200");
        buttonColor.classList.add("bg-red-400");
        buttonMovement.classList.toggle("translate-x-0");
        buttonMovement.classList.add("translate-x-3.5");
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