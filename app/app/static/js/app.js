function imgMod(){

    let redness = document.getElementById('redness').value
    let greenness = document.getElementById('greenness').value
    let blueness = document.getElementById('blueness').value
    let brightness = document.getElementById('brightness').value
    let saturation = document.getElementById('saturation').value
    let blur_sharp = document.getElementById('blur_sharp').value
    let rotation = document.getElementById('rotation').value

    let userImgSrc = document.getElementById('user_img').src
    // get rid of the 'data:image/jpeg;base64 bit: 
    let userImgBase64 = userImgSrc.substring(23)
    let clientInfo = {
        img: userImgBase64,
        redness: redness,
        blueness: blueness,
        greenness: greenness,
        brightness: brightness,
        saturation: saturation,
        blur_sharp: blur_sharp,
        rotation: rotation
    }

    fetch(`${window.origin}/upload-image`,{
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(clientInfo),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
    .then(function(response){
        response.json().then(function(data){
            document.getElementById('mod_img').src = `data:image/jpeg;base64,${data}`
        })
    })
}
