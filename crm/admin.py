from django.contrib import admin
from .models import Enquiry, Waitlist, EmailTemplate

admin.site.register(Enquiry)
admin.site.register(Waitlist)
admin.site.register(EmailTemplate)
