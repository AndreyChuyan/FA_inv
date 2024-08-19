$(document).ready(function() {
    $('#exportButton').on('click', function() {
        event.preventDefault(); // Добавлено для предотвращения перехода по ссылке
        $.ajax({
            url: '/base_export_script',
            type: 'GET',
            success: function(response) {
                showMessage('База успешно экспортирована в папку Export', 'success');
            },
            error: function(xhr, status, error) {
                var errorMessage = xhr.status + ': ' + xhr.responseText;
                if (errorMessage.indexOf("Permission denied") !== -1) {
                    showMessage("Закройте файл exel", 'danger');
                } else {
                    showMessage('Error: ' + errorMessage, 'danger');
                }
            }
        });
    });

    function showMessage(message, type) {
        var messageBox = $('#messageBox');
        messageBox.removeClass();
        messageBox.addClass('alert');  
        messageBox.addClass('alert-' + type);
        messageBox.text(message);
        messageBox.show();

        setTimeout(function() {
            messageBox.hide();
        }, 10000);  // Hide after 5 seconds
    }
});