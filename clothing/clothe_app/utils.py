
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.mail import send_mail

def generate_invoice(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, "INVOICE / BILL")
    y -= 50

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Order ID: {order.id}")
    y -= 20
    p.drawString(50, y, f"Name: {order.fname} {order.lname}")
    y -= 20
    p.drawString(50, y, f"Email: {order.email}")
    y -= 20
    p.drawString(50, y, f"Address: {order.address}")
    y -= 20
    p.drawString(50, y, f"Phone: {order.phone}")
    y -= 40

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Products")
    y -= 30

    p.setFont("Helvetica", 12)
    total = 0
    for item in order.items.all():
        p.drawString(60, y, f"{item.product_size.product.name} ({item.product_size.size.name}) x {item.quantity}")
        p.drawRightString(500, y, f"₹{item.price * item.quantity}")
        total += item.price * item.quantity
        y -= 20

    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total Amount: ₹{total}")
    y -= 20
    p.drawString(50, y, f"Payment Method: {order.payment_method}")
    y -= 20
    p.drawString(50, y, f"Payment Status: {order.payment_status}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
