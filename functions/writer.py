import requests
import json
import time
from azure.eventhub import EventData, EventHubProducerClient
from config import EVENTHUB_CONNECTION_STR, EVENTHUB_NAME, API_URL, FETCH_INTERVAL

# Track already sent event IDs with a 'set' to avoid duplicates
sent_event_ids = set()

# -----------------------------------
# Fetch Earthquake Data from USGS
# -----------------------------------
def fetch_earthquake_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

# -----------------------------------
# Send new events to Event Hub
# -----------------------------------
def send_new_events_to_eventhub(new_features):
    producer = EventHubProducerClient.from_connection_string(
        conn_str = EVENTHUB_CONNECTION_STR,
        eventhub_name = EVENTHUB_NAME
    )

    try:
        event_data_batch = producer.create_batch()

        for feature in new_features:
            event_data_batch.add(EventData(json.dumps(feature)))
            print(f"Sending new event ID: {feature.get('id')}")

        producer.send_batch(event_data_batch)
        print(f"Sent {len(new_features)} new events")

    except Exception as e:
        print(f"Error sending events: {e}")

    finally:
        producer.close()

# -----------------------------------
# Main
# -----------------------------------
if __name__ == "__main__":
    print("Starting sending events...")

    while True:
        try:
            data = fetch_earthquake_data()
            features = data.get("features", [])

            # Filter only new events
            new_features = [f for f in features if f.get('id') not in sent_event_ids]

            if new_features:
                send_new_events_to_eventhub(new_features)

                # Update sent IDs
                for f in new_features:
                    sent_event_ids.add(f.get('id'))
            else:
                print("No new events found.")
                
        except Exception as ex:
            print(f"Error in processing loop: {ex}")

        time.sleep(FETCH_INTERVAL)
