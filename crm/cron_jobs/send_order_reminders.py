
import os,sys
from gql import gql,Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime,timedelta
import django


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

LOG_FILE="/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = os.environ.get("GRAPHQL_ENDPOINT", "http://localhost:8000/graphql")


def send_order_reminders():
    one_week_ago=(datetime.now()-timedelta(days=7)).strftime('%Y-%m-%d')

    query=gql("""
            query($since:DateTime!){
              allOrders(orderDateGte:$since,orderBy:"order_date"){
                edges{
                    node{
                        id
                        customer{
                        email
                        }
                        orderDate
              
                            }
              
              
                        }
              
                 }
              
              
              }
""")
    
    transport=RequestsHTTPTransport(url=GRAPHQL_ENDPOINT,verify=True,retries=3)
    client=Client(transport=transport,fetch_schema_from_transport=True)

    result=client.execute(query,variable_values={"since": one_week_ago})
    orders=result.get("allOrders",{}).get("edges",[])
    with open(LOG_FILE, 'a') as f:
        for order_edge in orders:
            order=order_edge["node"]
            log_line=f"{datetime.now().strftime('%Y-%m-%d')}-Oder ID: {order['id']}, Customer: {order['customer']['email']}, Order Date: {order['orderDate']}\n"
            f.write(log_line)
    print("Order reminders processed!")



if __name__=="__main__":
    send_order_reminders()