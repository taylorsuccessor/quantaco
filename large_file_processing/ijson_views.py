import os
from datetime import datetime
from decimal import Decimal

import ijson
from django.db import transaction as db_transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from large_file_processing.models import Store, Transaction, TransactionItem, Venue

#from large_file_processing.tasks.process_file import process_large_file
from large_file_processing.tasks.process_file_chunks import process_large_file


class ProcessLargeFileViewSet(viewsets.ViewSet):
    """
    API to process a large nested JSON file in a memory-efficient way.
    """

    @action(detail=False, methods=["post"], url_path="start-processing-celery")
    def start_processing_ijson_celery(self, request, *args, **kwargs):
        file_path = "/var/www/large_file.json"
        process_large_file.delay(file_path)
        return Response({"status": "processing started"}, status=200)

    @action(detail=False, methods=["post"], url_path="process-one-transaction")
    def process_transaction(self, request):
        """
        Function to process and save a single transaction.
        """
        venue_id = request.data.get("venue_id")
        venue_name = request.data.get("venue_name")
        store_id = request.data.get("store_id")
        store_name = request.data.get("store_name")
        transaction = request.data.get("transaction")

        venue_obj, _ = Venue.objects.get_or_create(id=venue_id, defaults={"name": venue_name})

        store_obj, _ = Store.objects.get_or_create(
            id=store_id, defaults={"name": store_name, "venue": venue_obj}
        )

        txn_obj = Transaction(
            store=store_obj,
            transaction_id=transaction["TransactionID"],
            transaction_type=transaction["TransactionType"],
            datetime_utc=datetime.strptime(transaction["DateTimeUTC"], "%d/%m/%Y %I:%M:%S %p"),
            operator_number=transaction.get("OperatorNumber"),
            operator_name=transaction.get("OperatorName"),
            till_id=transaction.get("TillID"),
            till_name=transaction.get("TillName"),
            service_charge=Decimal(transaction.get("ServiceCharge", 0)),
            nett_total=Decimal(transaction.get("NettTotal", 0)),
            nett_sales=Decimal(transaction.get("NettSales", 0)),
            gross_sales=Decimal(transaction.get("GrossSales", 0)),
            order_discount=Decimal(transaction.get("OrderDiscount", 0)),
            total_discount=Decimal(transaction.get("TotalDiscount", 0)),
            taxable=Decimal(transaction.get("Taxable", 0)),
            non_taxable=Decimal(transaction.get("NonTaxable", 0)),
            tax_amount=Decimal(transaction.get("TaxAmount", 0)),
        )

        with db_transaction.atomic():
            txn_obj.save()

            transaction_items_objects = []
            for item_data in transaction.get("Items", []):
                product = item_data.get("Product", {})

                item_obj = TransactionItem(
                    transaction=txn_obj,
                    line_id=item_data["LineID"],
                    product_id=item_data["ProductID"],
                    quantity=Decimal(item_data["Quantity"]),
                    nett_price=Decimal(item_data["NettPrice"]),
                    gross_price=Decimal(item_data["GrossPrice"]),
                    item_discount=Decimal(item_data["ItemDiscount"]),
                    is_condiment=item_data["IsCondiment"],
                    nett_total=Decimal(item_data["NettTotal"]),
                    product_name=product.get("ProductName", ""),
                    category=product.get("Category", ""),
                    category_group=product.get("CategoryGroup", ""),
                    size=product.get("Size", ""),
                    barcode=product.get("Barcode", ""),
                )
                transaction_items_objects.append(item_obj)

            TransactionItem.objects.bulk_create(transaction_items_objects, batch_size=1000)
        return Response({"status": "Transaction successfully processed"}, status=200)
