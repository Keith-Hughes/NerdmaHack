function addClient(event) {


    event.preventDefault();

    nameInput = document.getElementById("name").value;
    surname = document.getElementById("surname").value;
    cellNumber = document.getElementById("phone").value;
    emails = document.getElementById("email").value;

    url = 'https://destined-ideal-sculpin.ngrok-free.app/add_client';

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