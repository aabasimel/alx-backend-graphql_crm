from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query for total customers, orders, and revenue
    query = gql("""
    query {
        totalCustomers: allCustomers {
            totalCount
        }
        totalOrders: allOrders {
            totalCount
            edges {
                node {
                    totalAmount
                }
            }
        }
    }
    """)

    try:
        result = client.execute(query)

        customers = result.get('totalCustomers', {}).get('totalCount', 0)
        orders = result.get('totalOrders', {}).get('totalCount', 0)
        revenue = sum([node['node']['totalAmount'] for node in result.get('totalOrders', {}).get('edges', [])])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

        with open(LOG_FILE, 'a') as f:
            f.write(log_line)

        print("CRM report generated!")

    except Exception as e:
        with open(LOG_FILE, 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error: {e}\n")
