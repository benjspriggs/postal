from geolocation.main import GoogleMaps

address = "New York City Wall Street 12"

google_maps = GoogleMaps(api_key='your_google_maps_key') 

location = google_maps.search(location=address) # sends search to Google Maps.

print(location.all()) # returns all locations.
