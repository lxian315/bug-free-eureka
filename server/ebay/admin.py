from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.html import format_html
from io import StringIO
from decimal import Decimal
from scrapyd_api import ScrapydAPI

import csv
import json

# Register your models here.

from . import models

# connect scrapyd service
scrapyd = ScrapydAPI('http://scrapy:6800')

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_list = ['url', 'name', 'wholesale_price', 'retail_price', 'profit', 'profit_percentage', 'wholesale_weight', 'wholesale_fee', 'units_sold', 'updates']
        field_names = [field.name for field in meta.fields if field.name in field_list]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected"

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class ProfitFilter(admin.SimpleListFilter):
    title = 'profit'
    parameter_name = 'profit'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(profit__gt = 0)
        elif value == 'No':
            return queryset.exclude(profit__gt = 0)
        return queryset

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    date_hierarchy = 'date'

    # list display
    def image(self):
        return format_html("<a href='{}' target='_blank'><img src='{}' alt={} height='82' width='42'></a>".format(self.image, self.image, self.name))

    def link(self):
        return format_html("<a href='{}' target='_blank'>{}</a>".format(self.url, self.ebay_name))
    link.admin_order_field = 'url'

    def wholesale(self):
        return self.wholesale_price
    wholesale.short_description = 'Wholesale ($)'
    wholesale.admin_order_field = 'wholesale_price'

    def retail(self):
        return self.retail_price
    retail.short_description = 'Retail ($)'
    retail.admin_order_field = 'retail_price'

    def profit(self):
        profit = Decimal('{0:.2f}'.format(self.retail_price - self.wholesale_price - self.wholesale_fee))
        return profit
    profit.short_description = 'Profit ($)'
    profit.admin_order_field = 'profit'

    def profit_percentage(self):
        profit_percentage = '{0:.2f}'.format(((self.retail_price - self.wholesale_price - self.wholesale_fee)/self.wholesale_price)*100)

        return profit_percentage
    profit_percentage.short_description = 'Profit (%)'
    profit_percentage.admin_order_field = 'profit_percentage'

    def weight(self):
        return self.wholesale_weight
    weight.short_description = 'Weight (oz)'
    weight.admin_order_field = 'wholesale_weight'

    def fee(self):
        return self.wholesale_fee
    fee.short_description = 'Fees ($)'
    fee.admin_order_field = 'wholesale_fee'

    # def units_sold(self):
    #     return Decimal(self.units_sold.rstrip('sold').replace(',', ''))
    # units_sold.admin_order_field = 'units_sold'

    list_display_links = ('name',)

    list_display = (
        # '__str__',
        # 'url',
        # 'ebay_name',
        image,
        link,
        'name',
        wholesale,
        retail,
        profit,
        profit_percentage,
        weight,
        fee,
        'units_sold',
        # 'wholesale_price',
        # 'retail_price',
        # 'profit',
        # 'profit_percentage',
        # 'wholesale_weight',
        # 'wholesale_fee',
        # 'units_sold',
        'updates',
        # 'date'
    )

    list_filter = ('date', ProfitFilter)

    exclude = ('url', 'ebay_name', 'profit', 'profit_percentage', 'units_sold', 'updates', 'image')

    actions = ["export_as_csv"]

    change_list_template = "ebay/ebay_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            data = []
            csv_file = request.FILES["csv_file"]

            # Read Product objects from passed in data
            csvf = StringIO(csv_file.read().decode())
            reader = csv.reader(csvf, delimiter=',')
            firstline = True
            for row in reader:
                if firstline:   #skip first line
                    firstline = False
                    continue

                data.append(dict(name=row[0], wholesale_price=row[1], wholesale_weight=row[2], wholesale_fee=row[3]))

                # two packs
                data.append(dict(name = '{} 2 Packs'.format(row[0]), wholesale_price = str(Decimal(row[1])*2), wholesale_weight = str(Decimal(row[2])*2), wholesale_fee = str(Decimal(row[3])*2)))

                # three packs
                data.append(dict(name = '{} 3 packs'.format(row[0]), wholesale_price = str(Decimal(row[1])*3), wholesale_weight = str(Decimal(row[2])*3), wholesale_fee = str(Decimal(row[3])*3)))

                # four packs
                data.append(dict(name = '{} 4 packs'.format(row[0]), wholesale_price = str(Decimal(row[1])*4), wholesale_weight = str(Decimal(row[2])*4), wholesale_fee = str(Decimal(row[3])*4)))

            scrapyd.schedule('default', 'ecrawl', rows=json.dumps(data))
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

@admin.register(models.Projection)
class ProjectionAdmin(admin.ModelAdmin):
    # date_hierarchy = 'date'

    def purchase_price(self):
        return self.purchase_price.replace('US $', '')
    purchase_price.short_description = 'Purchase_price ($)'
    purchase_price.admin_order_field = 'purchase_price'

    list_display = (
        '__str__',
        'purchase_name',
        purchase_price,
        'purchase_quantity',
        'purchase_date',
        # 'date'
    )

    list_filter = ('purchase_name',)

    exclude = ('id', 'purchase_name', 'purchase_price', 'purchase_quantity', 'purchase_date')