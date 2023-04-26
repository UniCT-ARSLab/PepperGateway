function savePoint() {
    const name = document.getElementById('point-name').value;

    fetch('/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: name
        })
    })
}
