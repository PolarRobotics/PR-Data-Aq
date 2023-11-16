// SerialMonitorForm.js - Corbin Hibler - 2023-11-10
// JavaScript script for calling SerialMonitor.py from Flask.py 

// Wait for the document to be ready
$(document).ready(function() {

    // When the start button is clicked
    $('input[name="start_button"]').click(function(e) {
        document.getElementById("programStatus").textContent = "Program running...";
        // Prevent the default form submission
        e.preventDefault();
        // Set the action to 'start'
        $('#action').val('start');
        // Submit the form
        $('#loopForm').submit();
    });

    // When the stop button is clicked
    $('input[name="stop_button"]').click(function(e) {
        document.getElementById("programStatus").textContent = "Program STOPPED.";
        document.getElementById("savedCsvName").textContent = "Saved CSV File saved to "
        // Prevent the default form submission
        e.preventDefault();
        // Set the action to 'stop'
        $('#action').val('stop');
        // Submit the form
        $('#loopForm').submit();
    });
    
    // When the form is submitted
    $('#loopForm').submit(function(event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // The URL to send the request to
        var url = '/start_serial_monitor';
        // Serialize the form data for the AJAX request
        var formData = $(this).serialize();
        // Log the form data for debugging
        console.log(formData);

        // Make an AJAX request
        $.ajax({
            // The type of request (POST)
            type: 'POST',
            // The URL to send the request to
            url: url,
            // The data to send with the request
            data: formData,
            // The function to run when the request is successful
            success: function(response) {
                // Log the response for debugging
                console.log(response);

                // Display the CSV path to the user
                document.getElementById("savedCsvName").textContent = "CSV File saved to " + response.csv_path;
            },
            // The function to run when the request fails
            error: function(error) {
                // Log the error for debugging
                console.log(error);
            }
        });
    });
});