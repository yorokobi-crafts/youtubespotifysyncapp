

//Reads a stored cookie by its name.
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//Gets the csrf token within the browser
var csrftoken = getCookie('csrftoken');

//Let the user log in
function signInCallback(authResult) {
    if (authResult['code']) {

        $.ajax({
            type: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader('X-CSRFToken', csrftoken);
            },
            url: 'https://yssync.herokuapp.com/login/',
            //url: 'http://localhost:8000/login/',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function (result) {
                location.reload(true);
            },
            data: { auth_code: authResult['code'] }
        });
    } else {
        alert('error');
    }
}