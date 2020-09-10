function musicEndedEvent(musicId, musicOrder) {
    const headers = {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf
    }

    fetch(musicUpdateUrl,
        {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                music: musicId
            })
        })
        .then(async res => {
            const { playlistCompleted } = await res.json()

            if (res.status == 200) {
                blockMusic(musicOrder)
                if (playlistCompleted) {
                    const divComplete = document.querySelector('.div-complete-playlist')
                    const header = document.querySelector('.header')
                    header.classList.add('d-none')
                    divComplete.classList.remove('d-none')
                } else {
                    allowMusic(musicOrder)
                }
            }
        })
        .catch(function (res) { console.log(res) })
}

const blockMusic = (musicOrder) => {
    const cardMusic = document.querySelector(`#card-music-${musicOrder}`)
    cardMusic.classList.add('card-music-block')
}

const allowMusic = (musicOrder) => {
    const cardMusic = document.querySelector(`#card-music-${musicOrder + 1}`)
    cardMusic.classList.remove('card-music-block')
}

/*function setLastTime() {
    var currentTime = Math.round(m1.currentTime)
    if (currentTime == Math.round(lastTime) || currentTime == (Math.round(lastTime) + 1)) {
        lastTime = m1.currentTime
    } else
        m1.currentTime = lastTime
}

m1.ontimeupdate = function () { setLastTime() }*/