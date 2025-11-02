from datetime import datetime
import os,sys
import django
from gql import gql,Client
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import ConnectionError
from gql.transport.exceptions import TransportQueryError

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_ENDPOINT = os.environ.get("GRAPHQL_ENDPOINT", "http://localhost:8000/graphql")
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

def log_crm_heartbeat():
    """Logs a heartbeat with timestamp"""
    timestamp=datetime.now().strftime("/%d/%m/%Y-%H:%M:%S")

    status=""
    try:
        transport=RequestsHTTPTransport(url=GRAPHQL_ENDPOINT,verify=True,retries=3)
        client=Client(transport=transport,fetch_schema_from_transport=False)
        query=gql("{hello}")
        result=client.execute(query)
        
        if result and result.get('hello'):
            status=f"Graphql OK {result.get('hello')}"
        else:
            status=f"Query returned unexpected data: {result}"
    except ConnectionError:
        status=f"Error: Connection failed to {GRAPHQL_ENDPOINT} server is down "
    except Exception as e:
        status=f"Excepton: {e}"
    message=f"{timestamp} CRM is alive"
    try:
         
        with open(LOG_FILE, 'a') as f:
            f.write(message)
    except Exception as e:
        print(f"Error writing to the file {LOG_FILE}: {e}")

LOW_STOCK_LOG_FILE = "/tmp/low_stock_updates_log.txt"

def update_low_stock():
    """Updates low stock products mutation via Graphql and los the products"""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    messages = [f"--- Cron Job Start: {timestamp} ---"]
    try:
        transport=RequestsHTTPTransport(url=GRAPHQL_ENDPOINT,verify=True,retries=3)
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql("""
                mutation UpdateStock {
                        updateLowStockProducts {
                            products {
                                name
                                stock
                            }
                                message
                    }
            }
""")


        result=client.execute(mutation)

        if result and 'updateLowStockProducts' in result:
            data=result['updateLowStockProducts']
            messages.append(f"GraphQL OK: {data.get('message')}")

            products=data.get('products',[])

            if products:
                messages.append("Updated poducts")
                for prod in products:
                    messages.append(f"name: {prod.get('name')}, new stock: {prod.get('stock')}")
            else:
                messages.append(f"No products were updated")
        else:
            messages.append(f"Query returned unexpected data:{result}")

    except ConnectionError:
        messages.append(f"Failed to connect to graphql end point at {GRAPHQL_ENDPOINT}")
    except Exception as e:
        messages.append(f"Exception: {e}")
    
    try:
        with open(LOW_STOCK_LOG_FILE,'a') as f:
            for line in messages:
                f.write(f"{line}\n")
    except Exception as e:
        messages.append(f"Error writing to the file: {e}")

if __name__ == "__main__":
    update_low_stock()
    print("Starting low stock update cron...")

