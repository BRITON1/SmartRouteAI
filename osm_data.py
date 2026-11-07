
# osm_data.py
# OpenStreetMap road-network retrieval for SmartRouteAI

import math
import osmnx as ox


# Identify our application when communicating with OSM
ox.settings.nominatim_user_agent = (
    "SmartRouteAI/0.1 (academic routing project)"
)

# Enable OSMnx caching to reduce repeated downloads
ox.settings.use_cache = True


def haversine_distance(point1, point2):
    """
    Calculate the great-circle distance between two
    geographical coordinates.

    Coordinates are (latitude, longitude).
    Returns distance in metres.
    """

    lat1, lon1 = point1
    lat2, lon2 = point2

    radius = 6_371_000

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * radius * math.asin(math.sqrt(a))


def get_location_coordinates(place_name):
    """Convert a place name into latitude and longitude."""

    location = ox.geocode(place_name)

    if location is None:
        raise ValueError(
            f"Could not locate the place: {place_name}"
        )

    return location


def convert_to_adjacency_list(network):
    """
    Convert an OSMnx directed road network into
    a weighted adjacency dictionary.

    Edge weights represent road lengths in metres.

    One-way roads remain one-way.
    """

    road_graph = {}

    for node in network.nodes:

        road_graph[node] = {}

    for u, v, data in network.edges(data=True):

        distance = data.get("length")

        if distance is None:
            continue

        # If multiple road edges connect the same nodes,
        # retain the shortest available edge.
        previous = road_graph[u].get(v, float("inf"))

        if distance < previous:
            road_graph[u][v] = distance

    return road_graph




def extract_edge_geometries(network):
    """
    Preserve the actual geographical geometry of each road.

    Returns coordinates in (latitude, longitude) order.
    For parallel edges, retain the geometry of the
    shortest edge, matching our adjacency-list conversion.
    """

    edge_geometries = {}

    for u, v, key, data in network.edges(
        keys=True,
        data=True
    ):

        distance = data.get("length")

        if distance is None:
            continue

        edge = (u, v)

        previous = edge_geometries.get(edge)

        if previous is None or distance < previous["length"]:

            geometry = data.get("geometry")

            if geometry is not None:

                # Shapely geometry uses (longitude, latitude)
                road_coordinates = [
                    (lat, lon)
                    for lon, lat in geometry.coords
                ]

            else:

                # Fallback for edges without geometry
                road_coordinates = [
                    (
                        network.nodes[u]["y"],
                        network.nodes[u]["x"]
                    ),
                    (
                        network.nodes[v]["y"],
                        network.nodes[v]["x"]
                    )
                ]

            # Ensure geometry follows the directed edge u -> v
            start = (
                network.nodes[u]["y"],
                network.nodes[u]["x"]
            )

            if (
                haversine_distance(
                    road_coordinates[0],
                    start
                )
                >
                haversine_distance(
                    road_coordinates[-1],
                    start
                )
            ):
                road_coordinates.reverse()

            edge_geometries[edge] = {
                "length": distance,
                "coordinates": road_coordinates
            }

    return {
        edge: data["coordinates"]
        for edge, data in edge_geometries.items()
    }


def get_osm_road_graph(
    start_place,
    destination_place,
    buffer_m=5000
):
    """
    Retrieve a driving-road network covering two locations.

    Returns:
        road_graph
        start_node
        goal_node
        coordinates
        location information
    """

    print("Locating starting point...")
    start_coordinates = get_location_coordinates(start_place)

    print("Locating destination...")
    goal_coordinates = get_location_coordinates(destination_place)

    # Find the approximate centre of the journey
    center_lat = (
        start_coordinates[0] + goal_coordinates[0]
    ) / 2

    center_lon = (
        start_coordinates[1] + goal_coordinates[1]
    ) / 2

    center = (center_lat, center_lon)

    # Calculate enough radius to include both locations
    journey_distance = haversine_distance(
        start_coordinates,
        goal_coordinates
    )

    radius = journey_distance / 2 + buffer_m

    print("\nDownloading OpenStreetMap driving network...")
    print(f"Search radius: {radius / 1000:.2f} km")

    network = ox.graph_from_point(
        center,
        dist=radius,
        network_type="drive",
        simplify=True
    )

    if network.number_of_nodes() == 0:
        raise ValueError("No road network was retrieved.")

    # Find the closest road-network nodes
    start_node = ox.distance.nearest_nodes(
        network,
        X=start_coordinates[1],
        Y=start_coordinates[0]
    )

    goal_node = ox.distance.nearest_nodes(
        network,
        X=goal_coordinates[1],
        Y=goal_coordinates[0]
    )

    # Convert road network into our graph structure
    road_graph = convert_to_adjacency_list(network)
    edge_geometries = extract_edge_geometries(network)

    # Save coordinates for every road-network node
    coordinates = {
        node: (
            data["y"],
            data["x"]
        )
        for node, data in network.nodes(data=True)
    }

    print("\nROAD NETWORK READY")
    print("-----------------------------")
    print("Road nodes:", len(road_graph))
    print(
        "Directed road connections:",
        sum(len(neighbours) for neighbours in road_graph.values())
    )

    print("Starting node:", start_node)
    print("Destination node:", goal_node)

    return {
        "graph": road_graph,
        "start_node": start_node,
        "goal_node": goal_node,
        "coordinates": coordinates,
        "edge_geometries": edge_geometries,
        "start_coordinates": start_coordinates,
        "goal_coordinates": goal_coordinates,
        "start_place": start_place,
        "destination_place": destination_place
    }
