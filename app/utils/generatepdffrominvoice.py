from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from io import BytesIO

# Define the invoice dictionary
invoice = {
    "invoice_number": "INV-123456",
    "date": "2024-07-31",
    "due_date": "2024-08-14",
    "customer": {
        "name": "John Doe",
        "address": "123 Elm Street",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62701",
        "email": "john.doe@example.com",
        "phone": "555-1234"
    },
    "items": [
        {"description": "Widget A", "quantity": 10, "unit_price": 15.00, "total": 150.00},
        {"description": "Widget B", "quantity": 5, "unit_price": 25.00, "total": 125.00},
        {"description": "Widget C", "quantity": 2, "unit_price": 50.00, "total": 100.00}
    ],
    "subtotal": 375.00,
    "tax_rate": 0.07,
    "tax_amount": 26.25,
    "total_amount_due": 401.25,
    "notes": "Thank you for your business!"
}


def generate_pdf(invoice):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Set title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Invoice")

    # Invoice details
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 100, f"Invoice Number: {invoice['invoice_number']}")
    c.drawString(72, height - 115, f"Date: {invoice['date']}")
    c.drawString(72, height - 130, f"Due Date: {invoice['due_date']}")

    # Customer details
    c.drawString(72, height - 160, f"Customer: {invoice['customer']['name']}")
    c.drawString(72, height - 175, f"Address: {invoice['customer']['address']}")
    c.drawString(72, height - 190, f"City: {invoice['customer']['city']}, State: {invoice['customer']['state']} {invoice['customer']['zip_code']}")
    c.drawString(72, height - 205, f"Email: {invoice['customer']['email']}")
    c.drawString(72, height - 220, f"Phone: {invoice['customer']['phone']}")

    # Item table header
    c.drawString(72, height - 250, "Description")
    c.drawString(300, height - 250, "Quantity")
    c.drawString(400, height - 250, "Unit Price")
    c.drawString(500, height - 250, "Total")

    # Draw item rows
    y_position = height - 270
    for item in invoice['items']:
        c.drawString(72, y_position, item['description'])
        c.drawString(300, y_position, str(item['quantity']))
        c.drawString(400, y_position, f"<span class="math-inline">\{item\['unit\_price'\]\:\.2f\}"\)
c\.drawString\(500, y\_position, f"</span>{item['total']:.2f}")
        y_position -= 15

    # Draw totals
    c.drawString(400, y_position - 20, f"Subtotal: ${invoice['subtotal']:.2f}")
    c.drawString(400, y_position - 35, f"Tax ({invoice['tax_rate']
