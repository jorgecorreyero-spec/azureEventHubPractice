API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

# Event Hub connection config
EVENTHUB_CONNECTION_STR = "Endpoint=sb://dataeventhub123.servicebus.windows.net/;SharedAccessKeyName=earthquakes_ManageSAS;SharedAccessKey=NlTT4zrHdZVed8sbTCm7i8o5bagDZV2kR+AEhOCAFpQ="
EVENTHUB_NAME = "earthquakes"

# Time waited for new request to the API
FETCH_INTERVAL = 60