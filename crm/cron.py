from datetime import datetime
import os
from gql import gql,Client
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import ConnectionError
from gql.transport.exceptions import TransportQueryError

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_ENDPOINT = os.environ.get("GRAPHQL_ENDPOINT", "http://localhost:8000/graphql")

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



