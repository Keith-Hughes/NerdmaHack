function addClient(event) {


    event.preventDefault();

    nameInput = document.getElementById("name").innerText;
    surname = document.getElementById("surname");
    cellNumber = document.getElementById("phone");
    emails = document.getElementById("email");

    url = 'http://https://destined-ideal-sculpin.ngrok-free.app/add_client';

    data = {
        firstName: nameInput,
        lastName: surname,
        phoneNumber: cellNumber,
        email: emails
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
  
    })
    .catch((error) => {
        console.error('Error:', error);
    });

}