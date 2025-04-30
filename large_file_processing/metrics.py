from prometheus_client import Counter

transaction_success_counter = Counter("transaction_success_total", "Total successful transactions")

transaction_failed_counter = Counter("transaction_failed_total", "Total failed transactions")

transaction_incomplete_counter = Counter(
    "transaction_incomplete_total", "Total incomplete transactions"
)

transaction_sent_to_celery_counter = Counter(
    "transaction_sent_to_celery_total", "Total sent to celery transactions"
)
