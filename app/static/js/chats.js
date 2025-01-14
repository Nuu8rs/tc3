$(document).ready(function () {
    const $overlay = $("#chats-overlay");
    const $formContainer = $("#form-container");
    const $inputField = $("#new-source");
    const hideForm = () => {
        $overlay.hide();
        $formContainer.hide();
        $inputField.val("");
    }


    $("#open-form").on("click", function () {
        $overlay.show();
        $formContainer.show();
    });

    $overlay.on("click", function () {
        hideForm();
    });

    $('#submit-source').on('click', () => {
        let url = $('#new-source').val();
        if (!url) {
            alert('{{ _("Please enter a URL!") }}');
            return;
        }
        $('#submit-source').prop('disabled', true).addClass('disabled');
        sendRequest(
            '/add-chat',
            type='POST',
            rawData={url},
            success_callback=(response) => {
                if (response.status == "OK") {
                    alert('Success!');
                    window.location.reload();
                } else {
                    alert(response.status);
                }

            },
            complete_callback =()=> {
                $('#submit-source').prop('disabled', false).removeClass('disabled');
                hideForm();
            }
        );
    });
});