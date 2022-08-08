from django.contrib import admin

# Register your models here.
from UniQInvoice.models import Company_Master, Dealer_Master
# Register your models here.
admin.site.register(Company_Master)

admin.site.register(Dealer_Master)