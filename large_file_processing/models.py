from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Store(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="stores")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="transactions")
    transaction_id = models.BigIntegerField(unique=True)
    transaction_type = models.CharField(max_length=50)
    datetime_utc = models.DateTimeField()
    operator_number = models.CharField(max_length=50, blank=True, null=True)
    operator_name = models.CharField(max_length=255, blank=True, null=True)
    till_id = models.IntegerField()
    till_name = models.CharField(max_length=255)
    service_charge = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.0"))]
    )
    nett_total = models.DecimalField(max_digits=10, decimal_places=2)
    nett_sales = models.DecimalField(max_digits=10, decimal_places=2)
    gross_sales = models.DecimalField(max_digits=10, decimal_places=2)
    order_discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2)
    taxable = models.DecimalField(max_digits=10, decimal_places=2)
    non_taxable = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction {self.transaction_id}"


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="items")
    line_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    nett_price = models.DecimalField(max_digits=10, decimal_places=2)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_discount = models.DecimalField(max_digits=10, decimal_places=2)
    is_condiment = models.BooleanField(default=False)
    nett_total = models.DecimalField(max_digits=10, decimal_places=2)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    category_group = models.CharField(max_length=255)
    size = models.CharField(max_length=50, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.product_name} (Transaction {self.transaction.transaction_id})"
