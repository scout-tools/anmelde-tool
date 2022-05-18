from django.contrib import admin

from event.cash import models as cash_models

admin.site.register(cash_models.CashIncome)
