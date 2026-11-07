
import osmnx as ox

# Identify our application to the OSM geocoding service
ox.settings.nominatim_user_agent = (
    "SmartRouteAI/0.1 (academic routing project)"
)

print("Connecting to OpenStreetMap...")

try:
    location = ox.geocode("Westlands, Nairobi, Kenya")

    latitude, longitude = location

    print("\nLOCATION FOUND")
    print("-----------------------------")
    print("Latitude:", latitude)
    print("Longitude:", longitude)

except Exception as error:
    print("\nOpenStreetMap request failed:")
    print(error)
