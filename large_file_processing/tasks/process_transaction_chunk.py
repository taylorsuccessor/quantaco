from decimal import Decimal

from celery import shared_task
from django.db import IntegrityError
from django.db import transaction as db_transaction

from large_file_processing.decorators.catch_exceptions import catch_exceptions
from large_file_processing.exceptions.transactions import DuplicateTransactionException
from large_file_processing.metrics import (
    transaction_failed_counter,
    transaction_incomplete_counter,
    transaction_success_counter,
)
from large_file_processing.models import Store, Transaction, TransactionItem, Venue
from large_file_processing.utils import parse_datetime_from_custom_format


@shared_task
# @catch_exceptions()
def process_transaction_task(venue_id, venue_name, store_id, store_name, transactions):
    """
    Now handles a list of transactions instead of one transaction.
    """

    transaction_incomplete_counter.inc(len(transactions))  # increment by number of transactions

    venue_obj, _ = Venue.objects.get_or_create(id=venue_id, defaults={"name": venue_name})

    store_obj, _ = Store.objects.get_or_create(
        id=store_id, defaults={"name": store_name, "venue": venue_obj}
    )

    with db_transaction.atomic():
        for transaction in transactions:
            try:
                transaction_data = {
                    "store": store_obj,
                    "transaction_id": transaction["TransactionID"],
                    "transaction_type": transaction["TransactionType"],
                    "datetime_utc": parse_datetime_from_custom_format(transaction["DateTimeUTC"]),
                    "operator_number": transaction.get("OperatorNumber"),
                    "operator_name": transaction.get("OperatorName"),
                    "till_id": transaction.get("TillID"),
                    "till_name": transaction.get("TillName"),
                    "service_charge": Decimal(transaction.get("ServiceCharge", 0)),
                    "nett_total": Decimal(transaction.get("NettTotal", 0)),
                    "nett_sales": Decimal(transaction.get("NettSales", 0)),
                    "gross_sales": Decimal(transaction.get("GrossSales", 0)),
                    "order_discount": Decimal(transaction.get("OrderDiscount", 0)),
                    "total_discount": Decimal(transaction.get("TotalDiscount", 0)),
                    "taxable": Decimal(transaction.get("Taxable", 0)),
                    "non_taxable": Decimal(transaction.get("NonTaxable", 0)),
                    "tax_amount": Decimal(transaction.get("TaxAmount", 0)),
                }

                txn_obj = Transaction(**transaction_data)
                txn_obj.save()

                items_objs = []
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
                    items_objs.append(item_obj)

                TransactionItem.objects.bulk_create(items_objs, batch_size=1000)

                transaction_success_counter.inc()

            except IntegrityError:
                transaction_failed_counter.inc()
                raise DuplicateTransactionException(transaction["TransactionID"])
