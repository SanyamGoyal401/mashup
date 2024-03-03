// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Get the form element
    const form = document.getElementById('form1');
    const spinner = document.querySelector('.spinner-border');
    console.log(spinner);
    // Hide the Bootstrap loader in case of an error
    spinner.style.display = 'none';
    // Add a submit event listener to the form
    form.addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        // Display the Bootstrap loader
        spinner.style.display = 'flex';

        // Make a Fetch API POST request
        fetch('/submitform', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Handle the response from the server
            console.log('Server response:', data);
            // Hide the Bootstrap loader after the fetch request completes
            spinner.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle errors, e.g., display an error message to the user
            // Hide the Bootstrap loader in case of an error
            spinner.style.display = 'none';
        });
    });
});
