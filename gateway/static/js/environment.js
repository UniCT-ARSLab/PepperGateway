var joysticks = {
    forward_joystick: {
        zone: document.getElementById('static-forward'),
        mode: 'static',
        position: 'absolute',
        lockY: true,
        color: 'blue'
    },
    rotate_joystick: {
        zone: document.getElementById('static-rotate'),
        mode: 'static',
        position: 'absolute',
        lockX: true,
        color: 'red'
    }
};
var joystick;

// Get debug elements and map them
var elDebug = document.getElementById('debug');
console.log(elDebug);
var elDump = elDebug.querySelector('.dump');
var els = {
  position: {
    x: elDebug.querySelector('.position .x .data'),
    y: elDebug.querySelector('.position .y .data')
  },
  force: elDebug.querySelector('.force .data'),
  pressure: elDebug.querySelector('.pressure .data'),
  distance: elDebug.querySelector('.distance .data')
};

createNipple('forward_joystick');
createNipple('rotate_joystick');

function bindNipple() {
    joystick.on('move', function(evt, data) {
        setTimeout(function() {
            debug(data);
        }, 2000);
    });

    // joystick.on('start end', function(evt, data) {
    //     // dump(evt.type);
    //     debug(data);
    // }).on('move', function(evt, data) {
    //     debug(data);
    // }).on('dir:up plain:up dir:left plain:left dir:down ' +
    //       'plain:down dir:right plain:right',
    //       function(evt, data) {
    //     // dump(evt.type);
    // }).on('pressure', function(evt, data) {
    //     debug({
    //         pressure: data
    //     });
    // });
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

// Print data into elements
function debug(obj) {
    function parseObj(sub, el) {
    	for (var i in sub) {
        	if (typeof sub[i] === 'object' && el) {
          		parseObj(sub[i], el[i]);
        	} else if (el && el[i]) {
        		el[i].innerHTML = scale(sub[i]);
                setTimeout(function() {
                    makeRequests(scale(sub["force"]));
                }, 2000);
        }
      }
    }
    setTimeout(function() {
      parseObj(obj, els);
    }, 2000);
  }
  
var nbEvents = 0;
  
  // Dump data
function dump(evt) {
    // setTimeout(function() {
    //     if (elDump.children.length > 4) {
    //         elDump.removeChild(elDump.firstChild);
    //     }
    // var newEvent = document.createElement('div');
    // newEvent.innerHTML = '<span class="data">' +
    //     evt + '</span>';
    //     elDump.appendChild(newEvent);
    //     nbEvents += 1;
    // }, 0);
}

function scale (number, inMin = 0, inMax = 10, outMin = 0, outMax = 3) {
	return (number - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
}

async function fetchWithTimeout(resource, options = {}) {
    const { timeout = 8000 } = options;
    
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    const response = await fetch(resource, {
      ...options,
      signal: controller.signal  
    });
    clearTimeout(id);
    return response;
}

// setInterval(
//     async function send(movement) {
//     try {
//         const response = await fetch("/move", {
//             method: "POST",
//             data: JSON.parse(movement)
//         })
//     } catch (error) {
//         console.log("Something went wrong")
//     }
// }, 5000);

// async function send(movement) {
//     // axios.post('/rotate', {
//     //     data: movement
//     // })
//     // .then(function (response) {
//     //     console.log(response);
//     // })
//     // .catch(function (error) {
//     //     console.log(error);
//     // });
//     console.log(movement);
// }

// async function sendData(movement) { 
//     return new Promise(async(resolve, reject) => {
//         console.log(movement);
//         return resolve();
//     })
// }
async function makeRequests (movement) {
    axios.post('/rotate', { data: movement }, { timeout: 2000 })
    .then(function (response) {
        console.log(response);
    })
    .catch(function (error) {
        console.log(error);
    });
}
