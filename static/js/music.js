var pressPlay = false

function musicEndedEvent(music, musicId, musicOrder) {
    // Impede que o usuário avance diretamente para o final da música, ativando 
    // o listener de musica finalizada
    if (Math.round(music.played.end(0)) != Math.round(music.duration)) {
        console.log("Coé irmão, não pode avançar a música não kkk.")
        return
    }

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
                    pressPlay = false
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

// Quando o usuario aperta o botão play, setamos pressPlay para true
const setPlay = () => {
    pressPlay = true
}

const setLastTime = (music) => {
    // Impede que o usuario avance a música antes de ter apertado play 
    if (!pressPlay)
        music.currentTime = 0

    const currentTime = music.currentTime
    const playedTime = music.played.end(0)

    // Impede que o usuario avance a musica
    if (currentTime != playedTime) {
        console.log("Coé irmão, não pode avançar a música não kkk.")
        music.currentTime = playedTime
    }

}