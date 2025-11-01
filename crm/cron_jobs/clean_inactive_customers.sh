#!/bin/bash

source /c/Users/Ahmed/alx-backend-graphql_crm/venv/Scripts/activate

deleted_count=$(python manage.py shell -c "

from crm.models import Custormer
from django.utils import timezone
from datetime import timedelta

one_year_ago=timezone.now()-timedelta(days=365)
inactive_customers=Customer.objects.get(orders__order_date__lte=one_year_ago).distinct()
count=inactive_customers.count()
inactive_ustomers.delete()
print(count)


")
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted ${deleted_count} inactive customers" >> /tmp/customer_cleanup_log.txt
