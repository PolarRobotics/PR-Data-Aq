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
        
        // Make an AJAX request
        $.ajax({
            // The type of request (POST)
            type: 'POST',
            // The URL to send the request to
            url: '/start_serial_monitor',
            // The data to send with the request
            data: $('#loopForm').serialize(),
            // The function to run when the request is successful
            success: function(response) {
                // Log the response for debugging
                console.log(response);
            },
            // The function to run when the request fails
            error: function(error) {
                // Log the error for debugging
                console.log(error);
            }
        });
    });

    // When the stop button is clicked
    $('input[name="stop_button"]').click(function(e) {
        document.getElementById("programStatus").textContent = "Program STOPPED.";
        // Prevent the default form submission
        e.preventDefault();
        // Set the action to 'stop'
        $('#action').val('stop');

        // Make an AJAX request
        $.ajax({
            // The type of request (POST)
            type: 'POST',
            // The URL to send the request to
            url: '/stop_serial_monitor',
            // The data to send with the request
            data: $('#loopForm').serialize(),
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