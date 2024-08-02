function addInvoice(event) {
    
        event.preventDefault();
        
        invoiceNr = document.getElementById('invoice-nr').value;
        fileUrl = document.getElementById('file-url').value;
        dateCreated = document.getElementById('date-created').value;
        dueDate = document.getElementById('due-date').value;
        amount = document.getElementById('amount').value;

        url = 'http://destined-ideal-sculpin.ngrok-free.app/add_invoice';

        data = {
            invoiceNumber: invoiceNr,
            fileUrl: fileUrl,
            dateCreated: dateCreated,
            dueDate: dueDate,
            amount: amount
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
