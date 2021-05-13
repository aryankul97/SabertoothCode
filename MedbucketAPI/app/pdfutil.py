from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import blue
from app.models import *

def get_bill_pdf(bill, billitems, customer):
	pdf_name=str(bill.bill_id)+'.pdf'
	canvas = Canvas(pdf_name, pagesize=A4)

	canvas.setFont("Helvetica-Bold", 24)
	canvas.drawString(3.5 * inch, 11 * inch, "Invoice")

	canvas.setFont("Courier-Bold", 18)
	canvas.drawString(3.3 * inch, 10.6 * inch, str(bill.store_id))

	canvas.setFont("Helvetica-Bold", 16)
	canvas.drawString(3.45 * inch, 10.2 * inch, "Tax Invoice")

	canvas.setFont("Courier-Bold", 14)
	canvas.drawString(0.5 * inch, 9.7 * inch, str(customer.customer_name))

	canvas.setFont("Courier", 14)
	canvas.drawString(0.5 * inch, 9.5 * inch, str(customer.customer_id))

	canvas.setFont("Helvetica-Bold", 14)
	canvas.drawString(6 * inch, 9.7 * inch, "Date :")

	canvas.setFont("Courier", 14)
	canvas.drawString(6.6 * inch, 9.7 * inch, str(bill.bill_date))

	canvas.setFont("Helvetica-Bold", 14)
	canvas.drawString(5.5 * inch, 9.4 * inch, "Invoice ID :")

	canvas.setFont("Courier", 14)
	canvas.drawString(6.6 * inch, 9.4 * inch, str(bill.bill_id))

	canvas.setFont("Helvetica-Bold", 14)
	canvas.drawString(0.5 * inch, 9 * inch, "SR")
	canvas.drawString(1 * inch, 9 * inch, "Name")
	canvas.drawString(5 * inch, 9 * inch, "Qty")
	canvas.drawString(5.5 * inch, 9 * inch, "Price")
	canvas.drawString(6.5 * inch, 9 * inch, "Amount")
	canvas.line(0 * inch,8.9 * inch,8.75 * inch,8.9 * inch)

	canvas.setFont("Courier", 12)
	a=8.65
	b=8.45
	c=8.25
	sr=1
	last_size_line=0.0
	last_size=0.0
	for x in billitems:
		#Item 1
		med=MedicineData.objects.filter(medicine_id=x.medicine_id)[0]
		canvas.drawString(0.5 * inch, a * inch, str(sr))
		canvas.drawString(0.5 * inch, b * inch, "ID : "+str(x.medicine_id))
		canvas.drawString(1 * inch, a * inch, str(med.medicine_name))
		canvas.drawString(5 * inch, a * inch, str(x.quantity))
		canvas.drawString(5.5 * inch, a * inch, str(med.medicine_mrp))
		canvas.drawString(6.5 * inch, a * inch, str(x.amount))
		canvas.drawString(6.5 * inch, b * inch, "Discount "+str(x.discount_amount))
		canvas.drawString(6.5 * inch, c * inch, "GST @ "+str(med.medicine_gst)+"%")

		last_size=c-0.35
		last_size_line=c-0.1
		a=a-0.65
		b=b-0.65
		c=c-0.65
		sr=sr+1

	canvas.line(0 * inch,last_size_line * inch,8.75 * inch,last_size_line * inch)

	canvas.setFont("Helvetica-Bold", 12)
	canvas.drawString(0.5 * inch, last_size * inch, "Total")
	canvas.setFont("Courier", 12)

	#Total
	canvas.drawString(6.5 * inch, last_size * inch, str(bill.total_amount))

	canvas.setFont("Helvetica-Bold", 12)
	canvas.drawString(5 * inch, (last_size-0.3) * inch, "Discount")
	canvas.drawString(6.2 * inch, (last_size-0.3) * inch, ":")
	canvas.drawString(5 * inch, (last_size-0.5) * inch, "Tax")
	canvas.drawString(6.2 * inch, (last_size-0.5) * inch, ":")
	canvas.drawString(5 * inch, (last_size-0.7) * inch, "Total")
	canvas.drawString(6.2 * inch, (last_size-0.7) * inch, ":")
	canvas.drawString(5 * inch, (last_size-0.9) * inch, "Received")
	canvas.drawString(6.2 * inch, (last_size-0.9) * inch, ":")
	canvas.drawString(5 * inch, (last_size-1.1) * inch, "Balance")
	canvas.drawString(6.2 * inch, (last_size-1.1) * inch, ":")

	#Total Details
	canvas.setFont("Courier", 12)
	canvas.drawString(6.5 * inch, (last_size-0.3) * inch, str(bill.total_discount_amount))
	canvas.drawString(6.5 * inch, (last_size-0.5) * inch, str(bill.total_tax_amount))
	canvas.drawString(6.5 * inch, (last_size-0.7) * inch, str(bill.total_amount_to_pay))
	
	canvas.setFont("Helvetica-Bold", 12)
	canvas.drawString(5 * inch, (last_size-1.4) * inch, "Tax Details")
	canvas.drawString(6.2 * inch, (last_size-1.4) * inch, ":")
	canvas.setFont("Helvetica", 12)
	canvas.drawString(5 * inch, (last_size-1.7) * inch, "SGST :")
	canvas.drawString(5 * inch, (last_size-1.9) * inch, "CGST :")

	#Tax
	canvas.setFont("Courier", 12)
	canvas.drawString(6.5 * inch, (last_size-1.7) * inch, str(float(bill.total_tax_amount)/2))
	canvas.drawString(6.5 * inch, (last_size-1.9) * inch, str(float(bill.total_tax_amount)/2))

	canvas.save()