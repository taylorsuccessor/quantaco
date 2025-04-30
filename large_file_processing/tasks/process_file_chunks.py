import ijson
import requests
from celery import shared_task
from django.conf import settings

from large_file_processing.metrics import transaction_sent_to_celery_counter
from large_file_processing.utils import convert_decimal_to_float

from .process_transaction_chunk import process_transaction_task


@shared_task
def call_process_transaction_api(venue_id, venue_name, store_id, store_name, transaction):
    url = settings.API_PROCESS_TRANSACTION

    payload = {
        "venue_id": venue_id,
        "venue_name": venue_name,
        "store_id": store_id,
        "store_name": store_name,
        "transaction": transaction,
    }

    payload = convert_decimal_to_float(payload)

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Transaction processed successfully")
    else:
        print(f"Failed to process transaction: {response.status_code} - {response.text}")


def process_one_store(store, venue_id, venue_name, chunk_size=100):
    store_id = store.get("StoreID")
    store_name = store.get("StoreName")

    transactions = store.get("Transactions", [])

    for i in range(0, len(transactions), chunk_size):
        transactions_chunk = transactions[i : i + chunk_size]

        transaction_sent_to_celery_counter.inc(len(transactions_chunk))

        process_transaction_task.delay(
            venue_id,
            venue_name,
            store_id,
            store_name,
            transactions_chunk,
        )


def process_one_venue(venue):
    venue_id = venue.get("VenueID")
    venue_name = venue.get("VenueName")

    for store in venue.get("Stores", []):
        process_one_store(store, venue_id, venue_name)


@shared_task
def process_large_file(file_path):
    with open(file_path, "rb") as f:
        venues = ijson.items(f, "item")
        for venue in venues:
            process_one_venue(venue)
