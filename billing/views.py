import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Invoice, Payment
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from django.core.mail import EmailMessage
from django.conf import settings


# Register a font that supports the Indian Rupee symbol (₹)
_FONT_REGISTERED = False
for _font_file in ["Nirmala.ttf", "arial.ttf", "segoeui.ttf"]:
    _font_path = os.path.join(
        os.environ.get("WINDIR", "C:\\Windows"), "Fonts", _font_file
    )
    if os.path.exists(_font_path):
        try:
            pdfmetrics.registerFont(TTFont("RupeeFont", _font_path))
            _FONT_REGISTERED = True
            break
        except Exception:
            continue


@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(
        booking__pet__owner=request.user
    ).order_by("-issued_date")
    return render(request, "billing/invoice_list.html", {"invoices": invoices})


@login_required
def invoice_detail(request, pk):
    if request.user.is_staff:
        invoice = get_object_or_404(Invoice, pk=pk)
    else:
        invoice = get_object_or_404(
            Invoice, pk=pk, booking__pet__owner=request.user
        )
    return render(request, "billing/invoice_detail.html", {"invoice": invoice})


@login_required
def pay_invoice(request, pk):
    if request.user.is_staff:
        invoice = get_object_or_404(Invoice, pk=pk)
    else:
        invoice = get_object_or_404(
            Invoice, pk=pk, booking__pet__owner=request.user
        )

    # Check if already paid
    if invoice.status == "paid":
        from django.contrib import messages

        messages.info(request, f"Invoice #{invoice.pk} has already been paid.")
        return redirect("invoice_list")

    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "digital")
        try:
            Payment.objects.create(
                invoice=invoice,
                amount_paid=invoice.amount,
                payment_method=payment_method,
            )
            invoice.status = "paid"
            invoice.save()
            
            if invoice.booking:
                invoice.booking.status = "paid"
                invoice.booking.save()
                
            from django.contrib import messages
            messages.success(request, "Payment successful.")
        except Exception as e:
            from django.contrib import messages
            messages.error(request, "Payment failed. Please try again.")
        return redirect("invoice_list")
    return render(request, "billing/pay_invoice.html", {"invoice": invoice})


@login_required
def generate_invoice_pdf(request, pk):
    if request.user.is_staff:
        invoice = get_object_or_404(Invoice, pk=pk)
    else:
        invoice = get_object_or_404(
            Invoice, pk=pk, booking__pet__owner=request.user
        )
    template_path = "billing/invoice_pdf.html"
    context = {"invoice": invoice}

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf in memory
    pdf_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
        
    pdf_content = pdf_file.getvalue()

    # Send Email with Attachment
    try:
        owner_email = invoice.booking.pet.owner.email if invoice.booking and invoice.booking.pet else None
        if owner_email:
            subject = f"VetSphere Invoice: {invoice.booking.pet.name}"
            message = f"Hello {invoice.booking.pet.owner.username},\n\nPlease find attached your invoice PDF document for the amount of Rs.{invoice.amount}.\n\nThank you for choosing VetSphere."
            
            email_msg = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [owner_email],
            )
            email_msg.attach(f"Invoice_{invoice.id}.pdf", pdf_content, "application/pdf")
            email_msg.send(fail_silently=True)
    except Exception:
        pass # Ignore email errors during download so it doesn't break PDF view

    # Return PDF as download response
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{invoice.id}.pdf"'

    return response
