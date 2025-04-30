from django.contrib import admin

from large_file_processing.models import Store, Transaction


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id",)
    search_fields = ("transaction_id",)
    list_filter = ("transaction_id",)
