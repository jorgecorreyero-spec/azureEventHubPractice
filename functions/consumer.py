from azure.eventhub import EventHubConsumerClient
import json
import pandas as pd
from config import EVENTHUB_CONNECTION_STR

# Global 'list' to store all events
event_list = []

# This callback will be called for each received event
def on_event(partition_context, event):
    #print(f"Data: {event.body_as_str()}")
    try:
        data = json.loads(event.body_as_str())

        if data not in event_list:  # To avoid duplicates
            event_list.append(data)  # Store in global list
            print(f"Received event ID: {data.get('id')}")
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
    
    partition_context.update_checkpoint(event)

def fill_dataframe():
    client = EventHubConsumerClient.from_connection_string(
        conn_str = EVENTHUB_CONNECTION_STR,
        consumer_group = "$Default"
    )

    try:
        print("Starting to receive events...")
        with client:
            a = client.receive(
                on_event=on_event,
                starting_position="-1",  # "-1" is from the beginning of the partition
            )
            print(a)
    except KeyboardInterrupt:
        print("Stopped receiving Events.")

        # Check global list of events
        df = pd.DataFrame(event_list)        

        print("\n--- Collected DataFrame ---")
        print("Collected " + str(len(df)) + " events.")
        print(df.head())

        print(list(df.columns))


if __name__ == "__main__":
    fill_dataframe()
