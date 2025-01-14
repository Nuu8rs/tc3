const sendRequest = (url, type, rawData, success_callback = () => {}, complete_callback = () => {}) => {
    $.ajax({
        url: url,
        type: type,
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(rawData),
        success: success_callback,
        error: (xhr) => {
            try {
                const response = JSON.parse(xhr.responseText);
                if (response.detail) {
                    alert(response.detail);
                } else {
                    alert("An unknown error occurred.");
                }
            } catch (e) {
                alert("Invalid response from server!");
            }
        },
        complete: complete_callback
    });
};

$(document).ready(() => {
    const currentLocation = window.location.pathname;
    const cookieLanguage = $.cookie('CurLang');
    let currentLanguage;
    if (cookieLanguage) {
        currentLanguage = cookieLanguage || browserLanguage.split('-')[0];
    } else {
        browserLanguage = navigator.language || navigator.userLanguage;
        currentLanguage = browserLanguage.split('-')[0].toUpperCase();
    }
    const hideLangs = () => {
        $('div.lang-item').each(function () {
            let langText = $(this).text().replace(/\s/g, '');
            if (langText == currentLanguage.toUpperCase()) {
                $(this).addClass('active');
                $.cookie('CurLang', currentLanguage);
            } else {
                $(this).addClass('hidden');
            }
        });
    }
    const highlightCurrentPage = () => {
        $('a.nav-link').each(function() {
            if ($(this).attr('href') === currentLocation) {
                $(this).addClass('active');
            }
        });
    }

    $('.menu-button').on('click', () => {
        $('.menu-container').toggleClass('opened');
    });

    $('.language-picker').on('click', () => {
        $('.language-picker').toggleClass('opened');
        $('#langArrow').toggleClass('flipped');
    });

    highlightCurrentPage()
    hideLangs()
});