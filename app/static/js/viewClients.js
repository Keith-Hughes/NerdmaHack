document.addEventListener("DOMContentLoaded", function() {
    const url = 'https://destined-ideal-sculpin.ngrok-free.app/clients';

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        const clientsContainer = document.getElementById('clients');
        data.forEach(client => {
            const clientCard = document.createElement('div');
            clientCard.classList.add('card');
            clientCard.innerHTML = `
                <h1>${client.firstName} ${client.lastName}</h1>
                <h2>${client.email}</h2>
                <h2>${client.phoneNumber}</h2>
            `;
            clientsContainer.appendChild(clientCard);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});