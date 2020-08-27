function musicEndedEvent(musicId) {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("X-CSRFToken", csrf)
    fetch(musicUpdateUrl,
    {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            music: musicId
        })
    })
    .then(function(res) { 
        console.log(res) 
    })
    .catch(function(res){ console.log(res) })
}