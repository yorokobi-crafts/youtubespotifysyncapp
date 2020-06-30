//Display animations only after load / Prevents animation on load
document.addEventListener("DOMContentLoaded", function (event) {
    document.querySelector('.body').classList.remove('preload');
});

//Variable declarations
const misteryBox = document.querySelector('.mistery-box');
const yssyncHomepageImg = document.querySelector('.yssync-homepage-img');
const yssyncSyncingImg = document.querySelector('.yssync-syncing-img');
const yssyncCompleteImg = document.querySelector('.yssync-complete-img');

const youtubeItem1 = document.querySelector('.youtube-playlist-item.item-one');
const youtubeItem2 = document.querySelector('.youtube-playlist-item.item-two');
const youtubeItem3 = document.querySelector('.youtube-playlist-item.item-three');

const spotifyItem1 = document.querySelector('.spotify-playlist-item.item-one');
const spotifyItem2 = document.querySelector('.spotify-playlist-item.item-two');
const spotifyItem3 = document.querySelector('.spotify-playlist-item.item-three');
const cursorIcon = document.querySelector('.cursor-icon');

const thumbnails = document.querySelectorAll('.thumbnail-container');

const footerBackgroundImg = document.querySelector('.fixed.fixed.login-topic-background.footer-img');

const realLaptop = document.querySelector('.fixed.login-topic-laptop.original');
const iconLaptop = document.querySelector('.login-topic-laptop.child-item');

const title1 = document.querySelector('.title-item.title-1');
const title2 = document.querySelector('.title-item.title-2');
const title4 = document.querySelector('.title-item.title-4');

var pageHeight = document.documentElement.scrollHeight;
var height = this.scrollY;

const logInButtons = document.querySelectorAll('.google-login');

const mobileChecker = () => {
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        const mobileMode = document.querySelector('.mobile-mode');
        mobileMode.classList.add('active');
    }
    else {
        const pcMode = document.querySelector('.pc-mode');
        pcMode.classList.add('active');
    }
}

mobileChecker();

//Add the log in function to every button on click
logInButtons.forEach(button => {
    button.addEventListener('click', function(){ auth2.grantOfflineAccess().then(signInCallback) } )
});

//Read the height of the device and check the scroll position to start the proper animanimations
const storeScroll = () => {
    pageHeight = document.documentElement.scrollHeight;
    height = this.scrollY;
    misteryBox.innerHTML = (height / pageHeight).toFixed(2);

    if (height > pageHeight * 0.10) {
        misteryBox.classList.add('one');
        title1.classList.add('hidden');
        title2.classList.add('shown');

    }
    else {
        misteryBox.classList.remove('one');
        title1.classList.remove('hidden');
        title2.classList.remove('shown');
    }

    if (height >= pageHeight * 0.11) {
        youtubeItem1.classList.add('one');
    }
    else {
        youtubeItem1.classList.remove('one');
    }

    if (height >= pageHeight * 0.12) {
        youtubeItem2.classList.add('one');
    }
    else {
        youtubeItem2.classList.remove('one');
    }

    if (height >= pageHeight * 0.13) {
        youtubeItem3.classList.add('one');
    }
    else {
        youtubeItem3.classList.remove('one');
    }

    if (height >= pageHeight * 0.22) {
        youtubeItem1.classList.add('two');
        youtubeItem2.classList.add('two');
        youtubeItem3.classList.add('two');

        yssyncSyncingImg.classList.add('one');
    }
    else {
        youtubeItem1.classList.remove('two');
        youtubeItem2.classList.remove('two');
        youtubeItem3.classList.remove('two');

        yssyncSyncingImg.classList.remove('one');
    }

    if (height >= pageHeight * 0.30) {
        spotifyItem1.classList.add('one');
        spotifyItem2.classList.add('one');
        spotifyItem3.classList.add('one');

        yssyncCompleteImg.classList.add('one');
    }
    else {
        spotifyItem1.classList.remove('one');
        spotifyItem2.classList.remove('one');
        spotifyItem3.classList.remove('one');

        yssyncCompleteImg.classList.remove('one');
    }

    if (height >= pageHeight * 0.37) {
        spotifyItem1.classList.add('two');
        spotifyItem2.classList.add('two');
        spotifyItem3.classList.add('two');
    }
    else {
        spotifyItem1.classList.remove('two');
        spotifyItem2.classList.remove('two');
        spotifyItem3.classList.remove('two');
    }

    if (height >= pageHeight * 0.40) {
        footerBackgroundImg.classList.add('visible');
    }
    else {
        footerBackgroundImg.classList.remove('visible');
    }

    if (height >= pageHeight * 0.50) {
        iconLaptop.classList.add('one');
        title2.classList.add('hidden');
        title4.classList.add('shown');
        for (var i = 0; i < thumbnails.length; i++) {
            thumbnails[i].classList.add('one');
        }
    }
    else {
        iconLaptop.classList.remove('one');
        title4.classList.remove('shown');
        title2.classList.remove('hidden');
        for (var i = 0; i < thumbnails.length; i++) {
            thumbnails[i].classList.remove('one');
        }
    }

    if (height >= pageHeight * 0.54) {
        realLaptop.classList.add('hidden');
        cursorIcon.classList.add('one');
    }
    else {
        realLaptop.classList.remove('hidden');
        cursorIcon.classList.remove('one');
    }

    if (height >= pageHeight * 0.56) {
        cursorIcon.classList.add('kurikku');
        var eraseThumbnail1 = document.querySelector('.thumbnail-container.back.toVanish.one');
        eraseThumbnail1.classList.add('vanish');
    }
    else {
        cursorIcon.classList.remove('kurikku');
        var eraseThumbnail1 = document.querySelector('.thumbnail-container.back.toVanish.one');
        eraseThumbnail1.classList.remove('vanish');
    }

    if (height >= pageHeight * 0.58) {
        cursorIcon.classList.add('two');
    }
    else {
        cursorIcon.classList.remove('two');
    }

    if (height >= pageHeight * 0.60) {
        cursorIcon.classList.add('kurikku2');
        var eraseThumbnail2 = document.querySelector('.thumbnail-container.side.toVanish.one');
        eraseThumbnail2.classList.add('vanish');
    }
    else {
        cursorIcon.classList.remove('kurikku2');
        var eraseThumbnail2 = document.querySelector('.thumbnail-container.side.toVanish.one');
        eraseThumbnail2.classList.remove('vanish');
    }

    if (height >= pageHeight * 0.68) {
        cursorIcon.classList.add('vanish');
        for (var i = 0; i < thumbnails.length; i++) {
            thumbnails[i].classList.add('two');
        }
    }
    else {
        cursorIcon.classList.remove('vanish');
        for (var i = 0; i < thumbnails.length; i++) {
            thumbnails[i].classList.remove('two');
        }
    }
}

//Listen for the scrolling and the resize activitu of the user
document.addEventListener('scroll', storeScroll);
document.addEventListener('resize', storeScroll);

//Run the animation function for the first time
storeScroll();