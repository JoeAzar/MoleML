function check() {
    console.log('here');
    navigator.camera.getPicture(onSuccess, onFail, {
        quality: 50,
        destinationType: Camera.DestinationType.DATA_URL
    });

    function onSuccess(imageData) {
        var b64 = "data:image/jpeg;base64," + imageData;
        console.log('start');
        $.post('https://api.cloudinary.com/v1_1/mole/image/upload', {
            file: b64,
            api_key: '838912264992939',
            timestamp: (Date.now() / 1000 | 0) + '',
            upload_preset: 'atdlnige'
        }, function (data) {
            if (data.hasOwnProperty('error')) {
                alert('Upload failed.');
            } else {
                localStorage.setItem('url', data['url'] + "");
                var url = encodeURIComponent(data['url']);
                localStorage.setItem('urle', url);
                window.location = 'newmole.html';
            }
        });
        console.log("camera success");
    }

    function onFail(message) {
        alert('Failed because: ' + message);
    }
}