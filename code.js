function stopAttack() {

    fetch('/stop', { method: 'POST' })
        .then(response => response.text())
        .then(data => {
            document.getElementById('output').innerHTML += '<br>' + data;
        });
    
    document.getElementById('stop-button').style.cursor = 'not-allowed';
    document.getElementById('stop-button').style.opacity = '0.5';
    document.getElementById('stop-button').disabled = true;
    }

function returnAndStop() {
    stopAttack();
    window.location.href = '/';
}

function hidden_item(bool) {
    if (bool == true)
    document.getElementById("hide-item").style.display = 'none';
    else
    document.getElementById("hide-item").style.display = 'block';
    return;
}