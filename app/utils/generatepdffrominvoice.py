from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime, timedelta

# Define the invoice dictionary
invoice = {
    "invoice_number": "INV-123456",
    "date": "2024-07-31",
    "due_date": "2024-08-14",
    "customer": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-1234",

    },
    "items": [
        {"description": "Widget A", "unit_price": 15.00, "total": 150.00},
        {"description": "Widget B", "unit_price": 25.00, "total": 125.00},
        {"description": "Widget C", "unit_price": 50.00, "total": 100.00}
    ],
    "subtotal": 375.00,
    "tax_rate": "7.00%",
    "total_amount_due": 401.25,
    "notes": "Thank you for your business!"
}

def create_invoice_dict(project_id, first_name, last_name, email, phone_number, project_name, invoice_description, amount ):
    time_delta = timedelta(days=30)
    current_date = datetime.now()
    due_date = datetime.now() + time_delta
    due_date_str = due_date.strftime("%d-%m-%Y")

    invoice = {
    "invoice_number": f"INV-{project_id}",
    "date": str(current_date),
    "due_date": due_date_str,
    "customer": {
        "name": first_name+' '+ last_name,
        "email": email,
        "phone": phone_number,

    },
    "items": [
        {"description": project_name+": "+invoice_description, "unit_price": 1, "total": amount},
    ],
    "subtotal": amount,
    "tax_rate": "15.00%",
    "total_amount_due": (amount*0.15) + amount,
    "notes": "Thank you for your business!"
    }

    return invoice

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
    c.drawString(72, height - 175, f"Email: {invoice['customer']['email']}")
    c.drawString(72, height - 190, f"Phone: {invoice['customer']['phone']}")

    # Item table header
    c.drawString(72, height - 300, "Description")
    c.drawString(300, height - 300, "Quantity")
    c.drawString(400, height - 300, "Unit Price")
    c.drawString(500, height - 300, "Total")

    # Draw item rows
    y_position = height - 330
    for item in invoice['items']:
        c.drawString(72, y_position, item['description'])
        c.drawString(300, y_position, "1")
        c.drawString(400, y_position, f"R{item['unit_price']:.2f}")
        c.drawString(500, y_position, f"R{item['total']:.2f}")
        y_position -= 15

    # Draw totals
    c.drawString(400, y_position - 30, f"Subtotal: R{invoice['subtotal']:.2f}")
    c.drawString(400, y_position - 45, f"Tax ({invoice['tax_rate']}): R{invoice['total_amount_due'] - invoice['subtotal']:.2f}")
    c.drawString(400, y_position - 60, f"Total Amount Due: R{invoice['total_amount_due']:.2f}")

    # Add notes
    c.drawString(72, y_position - 120, f"Notes: {invoice['notes']}")

    # Save PDF
    c.save()
    buffer.seek(0)

    invoice_name = f"{invoice['invoice_number']}.pdf"
    
    with open(invoice_name, "wb") as f:
        f.write(buffer.getvalue())
    # Return the buffer
    return invoice_name


