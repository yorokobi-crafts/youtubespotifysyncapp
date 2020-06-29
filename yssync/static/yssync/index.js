/////////////////////////////
//  DECLARATIONS
/////////////////////////////
//#region
var xhr;
const openModalButtons = document.querySelectorAll('[data-modal-target]');
const openOptionButtons = document.querySelectorAll('[data-option-target]');
const closeModalButtons = document.querySelectorAll('[data-close-button]');
const allModal = document.querySelectorAll('.user-option-menu');
const overlay = document.getElementById('dark-screen-id');
const loadingItem = document.getElementById('loading-item-id')
const modalResult = document.querySelector(".modal-result");
const allQuestions = document.querySelectorAll('.question');
const allActiveQuestions = document.querySelectorAll('li');
const allActiveAnswers = document.querySelectorAll('.answer');
const leftButton = document.querySelector('button.left');
const rigthButton = document.querySelector('button.right');
var currentInstruction = document.querySelector('.instruction.active');
var currentImage = document.querySelector('.tutorial-image.active');
var allTranslateText = document.querySelectorAll('[data-translate-text]');
const translateItem = document.querySelectorAll('[data-translation]');
const loadingIcon = document.querySelector('.loading-videos-icon');
const htmlItem = document.documentElement;
const allFlags = document.querySelectorAll('.language');
const changeUserButton = document.querySelector('#change-user');
const logOutButton = document.querySelector('#log-out');
const buttonSync = document.querySelector('.button-sync');
const burgerIcon = document.querySelector('.burger-menu');
const menuList = document.querySelector('.menu-list');
const shirnkMenuList = document.querySelector('.menu-list-shrink');
const darkModeItem = document.querySelector('.dark-mode-item');
const menuOptions = document.querySelectorAll('.item-hover');
var playlistInputs = document.querySelectorAll('.youtube-list-item');
const arrows = document.querySelectorAll(".arrow");
const urlSearchButton = document.querySelector('.url-append-button');
const urlInfo = document.querySelector("#searchInput");
const selectAllCheckboxArray = document.querySelectorAll('.playlist-checkbox-input');
//#endregion


/////////////////////////////
//  APPEND URL VIDEOS
/////////////////////////////
//#region


//Sends an ajax post requesting the playlist provided in the url info input.
//Appends the new playlist in the url-playlist list
//Adds the selectPlaylistItems listener to the playlist again.
function sendUrlInfo(urlName) {

    $.ajax({
        url: "https://yssync.herokuapp.com/yssync/ajax_url/",
        //url: "http://localhost:8000/yssync/ajax_url/",
        type: 'post',
        beforeSend: function (request) {
            request.setRequestHeader('X-CSRFToken', csrftoken);
        },
        data: { playListURL: urlName },
        success: function (data) {

            if (data == "NULL") {
                alert("Enlace no válido")
            }
            else {
                var json_data = JSON.parse(data);

                $("#url-append-list").append(
                    '<li class="youtube-list-item-element">' +
                    '<div class="youtube-list-item" id="' + json_data["id"] + '">' +

                    '<img class="youtube-list-picture youtube-playlist-itemlist" src="' + json_data["thumbnail"] + '" />' +

                    '<div class="youtube-playlist-itemlist">' +
                    '<ul>' +
                    '<li>' +
                    '<div> <a target="_blank" href="https://www.youtube.com/watch?v=' + json_data["id"] + '" > ' + json_data["title"] + ' </a> </div>' +
                    '</li>' +
                    '<li>' +
                    '<div> ' + json_data["counter"] + ' <span>Videos </span></div>' +
                    '</li>' +
                    '</ul>' +
                    '</div>' +

                    '<div class="checkbox-listitem">' +
                    '<input class="youtube-playlist-itemlist playlist-checkbox url-item-checkbox" type="checkbox" checked id="' + json_data["title"] + '" name="' + json_data["title"] + '" value="' + json_data["id"] + '">' +
                    '<label for="' + json_data["title"] + '"></label>' +
                    '</div>' +

                    '</div>' +
                    '</li>'
                );

                playlistInputs = document.querySelectorAll('.youtube-list-item');
                playlistInputs.forEach(div => {
                    div.addEventListener('click', function () { SelectPlaylistItems(this.id) })
                });
            }
        },
        error: function (data) {

        }
    });
}

//Gets the content of the url info input wihtin the app, and extracts the id of the playlist url provided. 
//Verifies if the provided playlist is already in the app
//If the url is new, proceeds to ask to the playlist to retrieve the content.
function verifyPlaylist() {
    var urlName = urlInfo.value.split("=").pop();
    var elementExists = document.getElementById(urlName);

    if (elementExists) {
        alert("Playlist already added");
    }
    else {
        sendUrlInfo(urlName);
    }
}

//Listens for the url search button to be clicked, triggers the veryfyPlaylist function when clicked.
urlSearchButton.addEventListener('click', function () { verifyPlaylist() });

//#endregion


/////////////////////////////
//  FEED VIDEOS
/////////////////////////////
//#region

//Asks for a playlist id and the desired page to go.
//Clears the preious videos from the videos section
//unsets the navigation arrows
//Displays the loaging icon
//Sends an ajax post asking for the desired videos
//Once the answer is recieved, verifies if there are next or previous pages, and then sets the correct visuals.
//Appends the new videos to the video section.
//Gets the new ignore-buttons and translates them into the current language
function ajaxSender(playlist_id, goTo) {

    var ul = document.getElementById("youtube-video-list-id");
    while (ul.firstChild) ul.removeChild(ul.firstChild);

    document.getElementById("prev-page").classList.remove("active-arrow");
    document.getElementById("next-page").classList.remove("active-arrow");

    loadingIcon.classList.add('active');

    $.ajax({
        url: "https://yssync.herokuapp.com/yssync/ajax_videos/",
        //url: "http://localhost:8000/yssync/ajax_videos/",
        type: 'post',
        beforeSend: function (request) {
            request.setRequestHeader('X-CSRFToken', csrftoken);
        },
        data: { playListId: playlist_id, goto_page: goTo },
        success: function (data) {

            var ul = document.getElementById("youtube-video-list-id");
            while (ul.firstChild) ul.removeChild(ul.firstChild);

            loadingIcon.classList.remove('active');

            if (data == "NULL") {
                alert("Enlace no válido")
            }
            else {
                var json_data = JSON.parse(data);

                if (json_data["prev_page"] != "NULL") {
                    var prevPageItem = document.getElementById("prev-page");
                    prevPageItem.classList.add("active-arrow");
                    prevPageItem.setAttribute("data-page", json_data["prev_page"]);
                }

                if (json_data["next_page"] != "NULL") {
                    var nextPageItem = document.getElementById("next-page");
                    nextPageItem.classList.add("active-arrow");
                    nextPageItem.setAttribute("data-page", json_data["next_page"]);
                }

                for (i = 0; i < json_data["videos"].length; i++) {

                    var ignoredElement = document.querySelector('[data-ignored-video-id="' + json_data["videos"][i][0] + '"]');
                    if (ignoredElement == null) {
                        $("#youtube-video-list-id").append(
                            '<li>' +
                            '<div class="youtube-video-item youtube-item" data-video-image-url="' + json_data["videos"][i][2] + '" data-video-title="' + json_data["videos"][i][1] + '" id="' + json_data["videos"][i][0] + '">' +
                            '<img class="youtube-video-picture youtube-video-itemlist"' +
                            'src="' + json_data["videos"][i][2] + '" />' +

                            '<div class="youtube-video-itemlist">' +
                            '<ul>' +
                            '<li>' +
                            '<div class="itemlist-title" > <a target="_blank" href="https://www.youtube.com/watch?v=' + json_data["videos"][i][0] + '"> ' + json_data["videos"][i][1] + ' </a> </div>' +
                            '</li>' +
                            '</ul>' +
                            '</div>' +
                            '<div class="checkbox-listitem">' +
                            ' <button data-video-id="' + json_data["videos"][i][0] + '" class="ignore-button-item"type="button" data-translate-text data-translate-button>IGNORE</button> ' +
                            '</div>' +
                            '</div>' +

                            '</li>'
                        );
                    }
                    else {
                        $("#youtube-video-list-id").append(
                            '<li>' +
                            '<div class="youtube-video-item youtube-item video-ignored" data-video-image-url="' + json_data["videos"][i][2] + '" data-video-title="' + json_data["videos"][i][1] + '" id="' + json_data["videos"][i][0] + '">' +
                            '<img class="youtube-video-picture youtube-video-itemlist"' +
                            'src="' + json_data["videos"][i][2] + '" />' +

                            '<div class="youtube-video-itemlist">' +
                            '<ul>' +
                            '<li>' +
                            '<div class="itemlist-title" > <a target="_blank" href="https://www.youtube.com/watch?v=' + json_data["videos"][i][0] + '"> ' + json_data["videos"][i][1] + ' </a> </div>' +
                            '</li>' +
                            '</ul>' +
                            '</div>' +
                            '<div class="checkbox-listitem">' +
                            ' <button data-video-id="' + json_data["videos"][i][0] + '" class="ignore-button-item button-ignored"type="button" data-translate-text data-translate-button>UNDO</button> ' +
                            '</div>' +
                            '</div>' +

                            '</li>'
                        );
                    }


                }
            }
            var appendButtons = document.querySelectorAll('[data-translate-button]');

            var ignoreButtonItem = document.getElementsByClassName("ignore-button-item");
            for (var i = 0; i < ignoreButtonItem.length; i++) {
                ignoreButtonItem[i].addEventListener("click", function () {

                    var videoItem = this.closest(".youtube-item");

                    var ignoredElement = document.querySelector('[data-ignored-video-id="' + videoItem.id + '"]');
                    if (ignoredElement != null) {
                        videoItem.classList.remove("video-ignored");
                        this.classList.remove("button-ignored");
                        this.innerHTML = "IGNORE";
                        ignoredElement.closest("li").remove();
                        if (appendButtons) {
                            translatePage(appendButtons, currentHtmlLanguage(htmlItem.lang), appendTranslations);
                        }

                    }
                    else {
                        videoItem.classList.add("video-ignored");
                        this.classList.add("button-ignored");
                        this.innerHTML = "UNDO";
                        if (appendButtons) {
                            translatePage(appendButtons, currentHtmlLanguage(htmlItem.lang), appendTranslations);
                        }

                        $("#modal-ignored-list-id").append(
                            '<li>' +
                            '<div class="ignored-video-list-item" data-ignored-video-id="' + videoItem.id + '">' +
                            '<img class="ignored-picture"' +
                            'src="' + videoItem.dataset.videoImageUrl + '" />' +
                            '<div class="ignored-title">' +
                            '<a target="_blank" href="https://www.youtube.com/watch?v=' + videoItem.id + '" >' + videoItem.dataset.videoTitle + '</a>' +
                            '</div>' +
                            '</div>' +
                            '</li>'
                        );


                    }

                    var ignoredElement = document.querySelector('[data-ignored-video-id]');
                    if (ignoredElement == null) {
                        document.getElementById("ignore-message-id").classList.add("active");
                    }
                    else {
                        document.getElementById("ignore-message-id").classList.remove("active");
                    }
                });
            };

            if (appendButtons) {
                translatePage(appendButtons, currentHtmlLanguage(htmlItem.lang), appendTranslations);
            }
        },
    });


};

//Gets and resets the currently selected playlist.
function clearPlaylistsSelected() {

    try {
        var selectedPlaylist = document.querySelector('.youtube-list-item.selected');
        selectedPlaylist.classList.remove('selected');
    }
    catch{
        return
    }
}

//Feeds the video section with the current selected playlist's content. goTo is set in order to get the first page's content.
function feedVideoList(playlist_id) {
    var goTo = "NULL";
    ajaxSender(playlist_id, goTo);
};

//Clears the previous playlist' videos
//Changes the visuals of the currently selected playlist
//Feeds the video section with the playlist' content.
//Sets the current playlist in a variable
function SelectPlaylistItems(id) {
    clearPlaylistsSelected();
    document.getElementById(id).classList.add('selected');
    feedVideoList(id);
    var currentPlaylist = document.getElementById("current-playlist-id");
    currentPlaylist.setAttribute("data-playlist", id);
};

//Listens for every playlist in the list to be clicked. Triggers to the function SelectPlaylistItems.
const selectPlaylist = () => {
    playlistInputs = document.querySelectorAll('.youtube-list-item');
    playlistInputs.forEach(div => {
        div.addEventListener('click', function () { SelectPlaylistItems(this.id) })
    });
}

selectPlaylist();

//Asks for the next or previous page information. Then feeds the video section with the videos of the previous or next Youtube page.
function goToPage(pageData) {
    var currentPlaylist = document.getElementById("current-playlist-id").getAttribute("data-playlist");
    ajaxSender(currentPlaylist, pageData);
};

//Listens for both next page and previous page buttons and triggers the function goToPage when clicked.
arrows.forEach(div => {
    div.addEventListener("click", function () { goToPage(this.getAttribute("data-page")) });
});

//#endregion


/////////////////////////////
//  SELECT ALL CHECBBOX
/////////////////////////////
//#region 
const selectAll = () => {
    for (var i = 0; i < selectAllCheckboxArray.length; i++) {
        selectAllCheckboxArray[i].addEventListener('click', function () { selectAllCheckbox(this.id, this.getAttribute('data-checkbox-class')) });
    }
}

selectAll();

//Verifies wether the clicked select-all checkbox is checked or not. sets and unsets the checked property of the correct checkbox if checked.
function selectAllCheckbox(id, checkboxClass) {
    var elements = document.getElementsByClassName(checkboxClass);
    if (document.getElementById(id).checked) {
        for (var i = 0; i < elements.length; i++) {
            elements[i].checked = true;
        };
    } else {
        for (var i = 0; i < elements.length; i++) {
            elements[i].checked = false;
        };
    }
}

//#endregion


/////////////////////////////
//  SET A COOKIE
/////////////////////////////
//#region

//Lets the user set a cookie with by asking for his name and value
function setCookie(cookieName, cookieValue) {
    document.cookie = cookieName + "=" + cookieValue + " ; expires=Thu, 25 Dec 2021 12:00:00 UTC; path=/";
}

//#endregion


/////////////////////////////
//  CHANGE THE LANGUAGE
/////////////////////////////
//#region

//Listen to the language options to be clicked, then reads every div in the file with data-translation and translates it to the desired language
translateItem.forEach(div => {
    div.addEventListener('click', () => {
        upgradeFlag(div.dataset.translation);
        allTranslateText = document.querySelectorAll('[data-translate-text]');
        translatePage(allTranslateText, div.dataset.translation, translations);
    })
})

//Reads the desired language and changes the flag to the correct language
function upgradeFlag(id) {
    allFlags.forEach(div => { div.classList.remove('active'); });
    document.getElementById(id).classList.add('active');
}

//Asks for the divs to be translated, the desired language and the dictionary to be user for translation
//Sets the html language to the desired language
//Sets a cookie with the desired language
//Reads every value in the array made of divs to be translated and translates the content with the 'translateText' function.
function translatePage(translateArray, language, dictionaryArray) {
    htmlItem.lang = currentLanguage(language);
    setCookie("language", language);

    for (var i = 0; i < translateArray.length; i++) {
        let sourceText = translateArray[i].innerHTML;
        translateArray[i].innerHTML = translateText(sourceText, language, dictionaryArray);
    }
};

//Gets the div in turn to be translated, the desired language and the dictionary to be used to translate
//Set a function for translation 
//Lets a value to get the object of the traslation object array, then returns the object of the object array that includes the div to translate
//finds the exact part of the object that contains the same div text but in the desired language
function translateText(sourceText, language, dictionaryArray) {
    function translate(translationObject) {
        let valuesOfObject = Object.values(translationObject);
        return valuesOfObject.includes(sourceText);
    };
    return dictionaryArray.find(translate)[language];
};

//Function that reads a language name and returns its language code
function currentLanguage(language) {
    switch (language) {
        case "English":
            return "en"
        case "Japanese":
            return "ja"
        case "Spanish":
            return "es"
        default:
            return "en"
    }
};

//Function that reads a language code and returns its language name
function currentHtmlLanguage(language) {
    switch (language) {
        case "en":
            return "English"
        case "ja":
            return "Japanese"
        case "es":
            return "Spanish"

        default:
            return "en"
    }
};

//Gets the user prefered language cookie
//If there's such cookie, translates the site into the desired language and changes the correct flag icon. 
//If there is not a language cookie, the default language is English.
const userLanguage = () => {
    let defaultLanguage = getCookie("language");
    if (defaultLanguage) {
        translatePage(allTranslateText, defaultLanguage, translations);
        upgradeFlag(defaultLanguage);
    }
    else {
        upgradeFlag("English");
    }
}
//Runs on load
userLanguage();

//#endregion


/////////////////////////////
//  CHANGE TO DARK MODE
/////////////////////////////
//#region

//Listen to the Dark mode option button. Changes the light mode into dark mode and vice versa when clicked, also sets a cookie when dark mode is selected.
document.querySelector("#dark-mode-option").addEventListener('click', () => {
    document.querySelector(".dark-mode-item").classList.toggle('active');

    if (document.body.classList.contains('dark')) {
        document.body.classList.remove('dark');
        document.cookie = "mode=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }
    else {
        document.body.classList.add('dark');
        setCookie("mode", "dark");
    }
});

//Gets the user mode cookie
//If there's such cookie, turns the mode button and turns on the dark mode.
const userMode = () => {
    let defaultMode = getCookie("mode");
    if (defaultMode) {
        darkModeItem.classList.add('active');
        document.body.classList.add(defaultMode);
    }
}

//Runs on load
userMode();

//#endregion


/////////////////////////////
//  LOG OUT
/////////////////////////////
//#region

//Sends an ajax post to delete the sessin cookie and reloads the page
function logOutfromSession() {
    $.ajax({
        url: "https://yssync.herokuapp.com/yssync/logout/",
        //url: "http://localhost:8000/yssync/logout/",
        type: 'post',
        beforeSend: function (request) {
            request.setRequestHeader('X-CSRFToken', csrftoken);
        },
        data: 'dummyData',
        success: function (response) {
            location.reload(true);
        },
    });
}

//Listen the user when change unser button is clicked to log out.
logOutButton.addEventListener('click', () => { logOutfromSession(); });

//Listen the user when change unser button is clicked to start change user function.
changeUserButton.addEventListener('click', function () { auth2.grantOfflineAccess().then(signInCallback) })

//#endregion


/////////////////////////////
//  TUTORIAL
/////////////////////////////
//#region 

//Listen to the right and left buttons of the tutorial section in order to make it work
leftButton.addEventListener('click', function () { prevInstruction() });
rigthButton.addEventListener('click', function () { nextInstruction() });

//Updates the instruction and the image in turn, then checks if there is a previous instruction to make it the current one.
//If it doesn't success, the current instruction remains as is. if it's the first instruction turns the 'prev' button inaccessible.
function prevInstruction() {
    currentInstruction = document.querySelector('.instruction.active');
    currentImage = document.querySelector('.tutorial-image.active');

    if (currentInstruction.previousElementSibling) {
        currentInstruction.classList.remove('active')
        currentInstruction.previousElementSibling.classList.add('active');

        currentImage.classList.remove('active')
        currentImage.previousElementSibling.classList.add('active');
    }

    currentInstruction = document.querySelector('.instruction.active');

    if (currentInstruction.nextElementSibling) {
        rigthButton.classList.add('active')
    }

    if (!currentInstruction.previousElementSibling) {
        leftButton.classList.remove('active')
    }
}

//Updates the instruction and the image in turn, then checks if there is a next instruction to make it the current one.
//If it doesn't success, the current instruction remains as is. if it's the last instruction and turns the 'next' button inaccessible.
function nextInstruction() {
    currentInstruction = document.querySelector('.instruction.active');
    currentImage = document.querySelector('.tutorial-image.active');

    if (currentInstruction.nextElementSibling) {
        currentInstruction.classList.remove('active')
        currentInstruction.nextElementSibling.classList.add('active');

        currentImage.classList.remove('active')
        currentImage.nextElementSibling.classList.add('active');
    }

    currentInstruction = document.querySelector('.instruction.active');

    if (currentInstruction.previousElementSibling) {
        leftButton.classList.add('active')
    }

    if (!currentInstruction.nextElementSibling) {
        rigthButton.classList.remove('active')
    }
}

//#endregion


/////////////////////////////
//  FAQ
/////////////////////////////
//#region

//Listen for every question in the FAQ section to be clicked, then expands the answer and focus the question when clicked. The rest of the questions go back to normal.
allQuestions.forEach(div => {
    div.addEventListener('click', () => {

        for (var i = 0; i < allActiveQuestions.length; i++) {
            allActiveQuestions[i].classList.remove('active');
        }

        for (var i = 0; i < allActiveAnswers.length; i++) {
            allActiveAnswers[i].classList.remove('active');
        }

        div.closest('li').classList.add('active');
        div.nextElementSibling.classList.add('active');
    })
})

//#endregion


/////////////////////////////
//  MODALS
/////////////////////////////
//#region

//Listens to every button that contains a content target to be clicked, then displays the modal with the correct modal code when clicked.
openModalButtons.forEach(div => {
    div.addEventListener('click', () => {
        const modal = document.querySelector(div.dataset.modalTarget)
        openModal(modal)
    })
})

//Verifies is there's actually a modal to be displayed. Displays the desired modal.
function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active');
    overlay.classList.add('active');
};

//Verifies if there's actually a modal to be hidden. Hides the desired modal.
function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active');
    overlay.classList.remove('active');
};

//Listens to every button that contains a content option target to be clicked, then displays the option modal with the correct modal code when clicked.
openOptionButtons.forEach(div => {
    div.addEventListener('click', () => {
        const modal = document.querySelector(div.dataset.optionTarget)
        openOption(modal)
    })
})

//Verifies if there's actually an option modal to be displayed. Displays and hides the option modal.
function openOption(modal) {

    if (modal == null) return

    if (modal.classList.contains('active')) {
        modal.classList.remove('active');
    }
    else {

        for (var i = 0; i < allModal.length; i++) {
            allModal[i].classList.remove('active');
        }

        modal.classList.add('active');
    }
};

//Listens to the whole document to be clicked, hides every option modal when clicked.
document.addEventListener('click', hideOptionMenu);

//Verifies if the part of the document clicked is not the option menu of if it doesn't contain target data. If not, reads the option modal displayed and removes hides it.
function hideOptionMenu(event) {
    if (!event.target.closest('.user-option-menu') && !event.target.dataset.close) {
        var closeOptionItem = document.querySelector('.user-option-menu.active');
        closeOptionItem.classList.remove('active');
    }
}

//Listens to every close-button inside the modals, and closes the modal that contains the button when clicked.
closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal')
        closeModal(modal)
    })
})

//Listens to the dark ovverlay screen to be clicked. Hides the currently displayed modal when clicked.
overlay.addEventListener('click', () => {
    const modals = document.querySelectorAll('.modal.active')
    modals.forEach(modal => {
        closeModal(modal)
    })
})

//#endregion


/////////////////////////////
//  SYNC
/////////////////////////////
//#region

//Listen to the window to storage new information. Starts syncing process when information is stored.
//window.addEventListener("storage", syncPlaylists);
window.addEventListener("storage", syncPlaylists);

//Creates a window with the information od the Spotify App we created and lets the user login.
function spotifyLogin() {
    var SPOTIPY_CLIENT_ID = "0693e474b35d441987e83f0de3c6fa85"
    var SPOTIPY_REDIRECT_URI = "https://yssync.herokuapp.com/yssync/callback/"
    //var SPOTIPY_REDIRECT_URI = "http://localhost:8000/yssync/callback/"
    var spotifyScope = "playlist-modify-public"
    var spotifyAuthEndpoint = "https://accounts.spotify.com/authorize?" + "client_id=" + SPOTIPY_CLIENT_ID + "&redirect_uri=" + SPOTIPY_REDIRECT_URI + "&scope=" + spotifyScope + "&response_type=token&state=123";
    var wnd = window.open(spotifyAuthEndpoint, 'callBackWindow', 'height=500,width=400');
}

//Listents to the button sync to be clicked, logs into Spotify when cklicked.
buttonSync.addEventListener('click', () => {
    spotifyLogin();
})

//Synchronizes the playlists
//Reads the accessToken from the storage trigger
//Verifies if at least one playlist is selected to be synchronized
//Displays the overlay and the loading icons
//Feeds an array with the items the user ignored.
//Gets the spotify access token, the form that contains the playlists' ids and the ignored videos array.
//sends an ajax post 
//Once the sync process is done, hides the overlay and loading items
//Proceeds to show the results' modal with the information of the synchronized playlists.
function syncPlaylists(event) {
    if (event.key == "accessToken") {
        var isEmpty = true;
        var checkboxList = document.querySelectorAll('input[type=checkbox]');

        for (var i = 0; i < checkboxList.length; i++) {
            if (checkboxList[i].checked == true) {
                isEmpty = false;
            }
        }

        if (isEmpty == true) {
            alert("Please select at least one playlist");
        }
        else {
            overlay.classList.add('active');
            loadingItem.classList.add('active');
            modalResult.classList.remove("active");

            ignoredArray = [];
            let ignoredItems = document.querySelectorAll('[data-ignored-video-id]')
            for (var i = 0; i < ignoredItems.length; i++) {
                ignoredArray.push(ignoredItems[i].dataset.ignoredVideoId);
            }

            var spAccessToken = event.newValue;
            var playlistForm = document.getElementById("form-id");
            var playlistFormData = new FormData(playlistForm);

            playlistFormData.append('accessToken', spAccessToken);
            playlistFormData.append('ignored_array', ignoredArray);

            xhr = $.ajax({
                url: "https://yssync.herokuapp.com/yssync/ajax/",
                //url: "http://localhost:8000/yssync/ajax/",
                type: 'post',
                beforeSend: function (request) {
                    request.setRequestHeader('X-CSRFToken', csrftoken);
                },
                data: playlistFormData,
                processData: false,
                contentType: false,
                success: function (response) {

                    overlay.classList.remove('active');
                    loadingItem.classList.remove('active');
                    modalResult.classList.add("active");
                    var json_data = JSON.parse(response);

                    var list = document.getElementById("modal-list-id");
                    while (list.firstChild) {
                        list.removeChild(list.firstChild);
                    }
                    Object.keys(json_data).forEach(function (key) {
                        $("#modal-list-id").append(
                            '<li>' +
                            '<div class="list-name">' + key + '</div>' +
                            '<div class="list-status ' + json_data[key] + ' "></div>' +
                            '</li>'
                        );
                    })
                },
                error: function (response) {
                    overlay.classList.remove('active');
                    loadingItem.classList.remove('active');

                    if(htmlItem.lang == "es"){
                        alert("This is a trail version of YSSYNC. This playlist can't be synchronized because it's too large and can't be processed by HEROKU. Official version of YSSYNC is comming soon.");
                    }

                    if(htmlItem.lang == "en"){
                        alert("Esta es una versión de prueba de YSSYNC. Esta playlist no puede ser sincronizada porque es muy larga y no puede ser procesada por HEROKU. La versión oficial de YSSYNC estará disponible próximamente");
                     }       
                }
            });
        }
    }
    else {
        alert('error');
    }
}

//#endregion


/////////////////////////////
//  MENU
/////////////////////////////
//#region

//Listens to the burger menu icon to be clicked, hides 
burgerIcon.addEventListener('click', () => hideMenu())

//Verifies wich menu list is hidden and dsplays it. Also hides the currently diplayed one.
function hideMenu() {
    menuList.classList.toggle('hidden');
    shirnkMenuList.classList.toggle('hidden');
}

//Gets the selected menu option id and resets the rest of the options.
function clearSelected(id) {

    var selectedOption = document.querySelector('.item-hover.selected');
    selectedOption.classList.remove('selected');

    try {
        var selectedItem = document.querySelector('.hidden-item.shown');
        selectedItem.classList.remove('shown');
    }
    catch (err) {

    }

    if (id != "app-info" && id != "ignored-list") {
        var ul = document.getElementById("youtube-video-list-id");
        while (ul.firstChild) ul.removeChild(ul.firstChild);

        var elements = document.getElementsByClassName('playlist-list');
        for (var i = 0; i < elements.length; i++) {
            elements[i].classList.add('hidden');
        };
    }
}

//Asks for the id of the menu option, its child id and the related playlist' id.
//Clears the menu list
//Changes the background color of the selected menu option, shows its child and changes the playlists only if it's not the app-info or ignored-list option.
function SelectItems(id, childId, playlistId) {

    clearSelected(id);
    document.getElementById(id).classList.add('selected');

    try {
        document.getElementById(childId).classList.add('shown');
    }
    catch (err) {

    }

    if (id != "app-info" && id != "ignored-list") {
        document.getElementById(playlistId).classList.remove('hidden');
    }

};

//Listens for every menu item to be clicked, 
menuOptions.forEach(div => {
    div.addEventListener("click", function () { SelectItems(this.id, this.getAttribute('data-hidden-id-info'), this.getAttribute('data-hidden-playlist-id')) });
});

//#endregion


/////////////////////////////
//  ON LOAD
/////////////////////////////
//#region

//Everytime the website loads, put some default properties.
const onLoad = () => {
    document.getElementById("my-playlist").className = 'item-hover selected';
    document.getElementById("hidden-my-playlist").className = 'hidden-item shown  ';
    document.getElementById("playlist-list-id").className = 'playlist-list';

    var elements = document.getElementsByClassName(checkboxClass);
    for (var i = 0; i < elements.length; i++) {
        elements[i].checked = false;
    };
}

onLoad();

//#endregion



