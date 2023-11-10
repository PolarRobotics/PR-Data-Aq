$(document).ready(function() {
    $('input[name="start_button"]').click(function(e) {
        e.preventDefault();
        $('#action').val('start');
        $('#loopForm').submit();
    });

    $('input[name="stop_button"]').click(function(e) {
        e.preventDefault();
        $('#action').val('stop');
        $('#loopForm').submit();
    });
    
    $('#loopForm').submit(function(event) {
        event.preventDefault();
        
        var url = '/start_serial_monitor';
        var formData = $(this).serialize();
        console.log(formData);

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});