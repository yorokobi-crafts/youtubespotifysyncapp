//Set your client_id and scope to let the user login
function start() {
    gapi.load('auth2', function () {
        auth2 = gapi.auth2.init({
            client_id: '125100192294-a23qgdu7mv0volo8fsb1j8tj113jp9i0.apps.googleusercontent.com',
            scope: 'https://www.googleapis.com/auth/youtube.readonly'
        });
    });
}