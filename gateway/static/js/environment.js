var rotate_item = nipplejs.create({
    zone: document.getElementById('static-rotate'),
    mode: 'static',
    lockX: true,
    position: 'absolute',
    color: 'red'
});
var forward_item = nipplejs.create({
    zone: document.getElementById('static-forward'),
    mode: 'static',
    lockY: true,
    position: 'absolute',
    color: 'blue'
});


// rotate_item.on('start', function (evt, nipple) {
//     nipple.on('move end dir plain', function (evt) {
//         console.log("ROTATE")
//         console.log("X POSITION:" + nipple.position.x + " Y POSITION:" + nipple.position.y)
//         console.log("FORCE:" + nipple.force + "    DISTANCE:" + nipple.distance + "    PRESSURE" + nipple.pressure)
//         // console.log("RADIAN:" + nipple.angle.degree)
//     });
// });

// forward_item.on('start', function (evt, nipple) {
//     nipple.on('move end dir plain', function (evt) {
//         console.log("FORWARD")
//         console.log("X POSITION:" + nipple.position.x + " Y POSITION:" + nipple.position.y)
//         console.log("FORCE:" + nipple.force + "    DISTANCE:" + nipple.distance + "    PRESSURE" + nipple.pressure)
//         // console.log("RADIAN:" + nipple.angle.degree)
//     });
// });


rotate_item.on('move', async function (evt, nipple) {
    console.log("Avvio rotazione!")
    let index = 0
    const response = await fetch("/rotate", { method: "GET" })
    // const data = {
    //     "distance": nipple.distance,
    //     "radian": nipple.angle.radian,
    //     "position": nipple.position,
    // }
    // try {
    //     const response = await fetch("/rotate", {
    //         method: "POST",
    //         data: JSON.parse(data)
    //     })
    // } catch (error) {
    //     console.log("Something went wrong")
    // }
});
