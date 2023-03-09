function mapSection(_) {
    if (_) {
        showItem('mapSection');
        showItem('grayBackground');
    } else {
        hideItem('mapSection');
        hideItem('grayBackground');
    }
}

function explorationMode() {
    const radius = document.getElementById('radius').value;
    const loader = document.getElementById('loaderItem');
    showItem('grayBackground');
    showItem('loaderItem');
    fetch('/exploreEnv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: radius
        })
    })
    .then(response => {
        hideItem('loaderItem');
        if (response.ok) {
            showItem('mapSection');
        } else throw new Error('Errore nella chiamata al server');
    })
}

async function getMaps() {
    const response = await fetch('/getMaps');
    const maps = await response.json();
    
    console.log(maps);
    addMaps(maps);
}

async function loadMap(item) {
    mapName = item.parentElement.parentElement.children[0].innerText;
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            // 'Content-Type': 'application/json',
        },
        body: JSON.stringify(mapName)
    };
    try {
        const fetchResponse = await fetch('/loadMap', settings);
        // const data = await fetchResponse.json();
        // console.log(data);
        // return data;
    } catch (e) {
        return e;
    }
}

async function deleteMap(item) {
    mapName = item.parentElement.parentElement.children[0].innerText;
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(mapName)
    };
    try {
        const fetchResponse = await fetch('/deleteMap', settings);
        location.reload(true);
    } catch (e) {
        return e;
    }
}

const addMaps = (maps) => {
    maps.forEach(e => {
        const tbody = document.querySelector('#maps_table tbody')
        const tr = document.createElement('tr')
        const td_text = document.createElement('td')
        const td_load_button = document.createElement('td')
        const td_delete_button = document.createElement('td')

        tr.classList.add('bg-white', 'border-b', 'dark:bg-gray-800', 'dark:border-gray-700');
        td_text.classList.add('px-6', 'py-4', 'font-medium', 'text-gray-900', 'whitespace-nowrap', 'dark:text-white');
        td_load_button.classList.add('px-6', 'py-4', 'text-right');
        td_delete_button.classList.add('px-6', 'py-4', 'text-right');
        
        td_text.innerText = e;
        td_load_button.innerHTML += '<span class="font-medium text-blue-600 hover:cursor-pointer" onclick="loadMap(this)">Carica</a>';
        td_delete_button.innerHTML += '<span class="font-medium text-blue-600 hover:cursor-pointer" onclick="deleteMap(this)">Elimina</a>';

        tr.appendChild(td_text);
        tr.appendChild(td_load_button);
        tr.appendChild(td_delete_button);

        tbody.appendChild(tr)
    })
}

getMaps();