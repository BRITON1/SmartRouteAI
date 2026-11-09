import folium
from streamlit_folium import st_folium

import time

import streamlit as st

from dijkstra_search import dijkstra_search
from osm_data import get_osm_road_graph
from osm_search import (
    greedy_best_first_search_osm,
    a_star_search_osm
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Real-World Routing | SmartRouteAI",
    page_icon="🌍",
    layout="wide"
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🌍 Real-World Route Planner")

st.markdown(
    "Plan journeys using real road networks from OpenStreetMap "
    "and compare intelligent search algorithms."
)

st.divider()


# --------------------------------------------------
# JOURNEY INPUTS
# --------------------------------------------------

st.subheader("Journey Configuration")

col1, col2 = st.columns(2)

with col1:
    start_location = st.text_input(
        "Starting location",
        value="Westlands, Nairobi, Kenya"
    )

with col2:
    destination = st.text_input(
        "Destination",
        value="Lavington, Nairobi, Kenya"
    )


st.info(
    "Enter recognizable place names. "
    "The system will retrieve the actual driving-road network."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "osm_data" not in st.session_state:
    st.session_state.osm_data = None
    
if "algorithm_results" not in st.session_state:
    st.session_state.algorithm_results = None

# --------------------------------------------------
# RETRIEVE ROAD NETWORK
# --------------------------------------------------

if st.button(
    "🌍 Prepare Road Network",
    use_container_width=True
):

    if not start_location.strip() or not destination.strip():

        st.warning("Please enter both locations.")

    elif start_location.strip().lower() == destination.strip().lower():

        st.warning("Starting location and destination must be different.")

    else:

        try:

            with st.spinner(
                "Locating places and downloading the road network..."
            ):

                road_data = get_osm_road_graph(
                    start_location.strip(),
                    destination.strip()
                )

                st.session_state.osm_data = road_data
                st.session_state.algorithm_results = None

            st.success("OpenStreetMap road network retrieved successfully!")

        except Exception as error:

            st.session_state.osm_data = None
            st.session_state.algorithm_results = None

            st.error(f"Could not prepare the road network: {error}")


# --------------------------------------------------
# DISPLAY ROAD NETWORK INFORMATION
# --------------------------------------------------

road_data = st.session_state.osm_data

if road_data is not None:

    st.divider()

    st.subheader("Road Network Information")

    graph = road_data["graph"]

    total_nodes = len(graph)

    total_connections = sum(
        len(neighbours)
        for neighbours in graph.values()
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Road Nodes", f"{total_nodes:,}")

    with metric2:
        st.metric("Directed Connections", f"{total_connections:,}")

    with metric3:
        st.metric(
            "Network Status",
            "Ready",
            delta="Successfully retrieved"
        )

    st.divider()

    st.subheader("Journey Details")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Starting Location**")

        st.write(road_data["start_place"])

        st.write(
            "Coordinates:",
            road_data["start_coordinates"]
        )

        st.write(
            "Nearest road node:",
            road_data["start_node"]
        )

    with col2:

        st.markdown("**Destination**")

        st.write(road_data["destination_place"])

        st.write(
            "Coordinates:",
            road_data["goal_coordinates"]
        )

        st.write(
            "Nearest road node:",
            road_data["goal_node"]
        )

    st.success(
        "The road graph is ready for Greedy Best-First Search "
        "and A* Search."
    )


# --------------------------------------------------
# RUN SEARCH ALGORITHMS
# --------------------------------------------------

if road_data is not None:

    st.divider()

    st.subheader("AI Route Optimization")

    st.write(
        "Run Greedy Best-First Search, A* Search, "
        "and Dijkstra on the retrieved road network."
    )

    if st.button(
        "🚀 Calculate Routes",
        width="stretch"
    ):

        graph = road_data["graph"]
        start_node = road_data["start_node"]
        goal_node = road_data["goal_node"]
        coordinates = road_data["coordinates"]

        try:

            with st.spinner(
                "Running the three search algorithms..."
            ):

                # GREEDY SEARCH
                start_time = time.perf_counter()

                greedy_result = greedy_best_first_search_osm(
                    graph,
                    start_node,
                    goal_node,
                    coordinates
                )

                greedy_time = (
                    time.perf_counter() - start_time
                ) * 1000

                greedy_result["execution_time"] = greedy_time

                # A* SEARCH
                start_time = time.perf_counter()

                astar_result = a_star_search_osm(
                    graph,
                    start_node,
                    goal_node,
                    coordinates
                )

                astar_time = (
                    time.perf_counter() - start_time
                ) * 1000

                astar_result["execution_time"] = astar_time

                # DIJKSTRA SEARCH
                start_time = time.perf_counter()

                dijkstra_result = dijkstra_search(
                    graph,
                    start_node,
                    goal_node
                )

                dijkstra_time = (
                    time.perf_counter() - start_time
                ) * 1000

                dijkstra_result["execution_time"] = dijkstra_time

                # SAVE RESULTS
                st.session_state.algorithm_results = {
                    "greedy": greedy_result,
                    "astar": astar_result,
                    "dijkstra": dijkstra_result
                }

            st.success("All three algorithms completed!")

        except Exception as error:

            st.session_state.algorithm_results = None

            st.error(f"Algorithm execution failed: {error}")


# --------------------------------------------------
# DISPLAY ALGORITHM RESULTS
# --------------------------------------------------

algorithm_results = st.session_state.algorithm_results

if algorithm_results is not None:

    greedy = algorithm_results["greedy"]
    astar = algorithm_results["astar"]
    dijkstra = algorithm_results["dijkstra"]

    st.divider()

    st.subheader("Algorithm Performance Comparison")

    if all(
        result["found"]
        for result in [greedy, astar, dijkstra]
    ):

        # DISTANCE COMPARISON
        st.markdown("### Route Distances")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Greedy Distance",
                f"{greedy['distance_km']:.3f} km"
            )

        with col2:
            st.metric(
                "A* Distance",
                f"{astar['distance_km']:.3f} km"
            )

        with col3:
            st.metric(
                "Dijkstra Distance",
                f"{dijkstra['distance_km']:.3f} km"
            )

        # SEARCH EFFORT
        st.markdown("### Search Effort")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Greedy Expanded Nodes",
                f"{greedy['expanded_nodes']:,}"
            )

        with col2:
            st.metric(
                "A* Expanded Nodes",
                f"{astar['expanded_nodes']:,}"
            )

        with col3:
            st.metric(
                "Dijkstra Expanded Nodes",
                f"{dijkstra['expanded_nodes']:,}"
            )

        # EXECUTION TIME
        st.markdown("### Execution Time")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Greedy Time",
                f"{greedy['execution_time']:.3f} ms"
            )

        with col2:
            st.metric(
                "A* Time",
                f"{astar['execution_time']:.3f} ms"
            )

        with col3:
            st.metric(
                "Dijkstra Time",
                f"{dijkstra['execution_time']:.3f} ms"
            )

        # SHORTEST PATH VERIFICATION
        st.markdown("### Shortest-Path Verification")

        if abs(astar["cost"] - dijkstra["cost"]) < 0.001:

            st.success(
                "VERIFIED: A* matches Dijkstra's shortest "
                "distance in the retrieved road network."
            )

        else:

            st.warning(
                "A* and Dijkstra returned different distances. "
                "Further investigation is required."
            )

        # GREEDY ROUTE QUALITY
        difference = (
            greedy["distance_km"] - dijkstra["distance_km"]
        )

        if dijkstra["distance_km"] > 0:

            percentage = (
                difference / dijkstra["distance_km"]
            ) * 100

            st.markdown("### Greedy Route Analysis")

            st.write(
                f"Greedy route is {difference:.3f} km "
                f"longer than the Dijkstra benchmark."
            )

            st.write(
                f"Distance above benchmark: {percentage:.2f}%"
            )

        # ROUTE NODE COUNTS
        st.markdown("### Route Information")

        st.write(
            f"Greedy route: {len(greedy['path'])} road nodes"
        )

        st.write(
            f"A* route: {len(astar['path'])} road nodes"
        )

        st.write(
            f"Dijkstra route: {len(dijkstra['path'])} road nodes"
        )

    else:

        st.error(
            "At least one algorithm could not find a route "
            "inside the retrieved road network."
        )


# --------------------------------------------------
# BUILD ACTUAL ROAD GEOMETRY FOR A ROUTE
# --------------------------------------------------

def build_route_coordinates(path, road_data):

    node_coordinates = road_data["coordinates"]
    edge_geometries = road_data.get("edge_geometries", {})

    route_coordinates = []

    for index in range(len(path) - 1):

        current_node = path[index]
        next_node = path[index + 1]

        edge = (current_node, next_node)

        # Use the actual OpenStreetMap road geometry
        road_shape = edge_geometries.get(edge)

        if road_shape:

            if route_coordinates:
                route_coordinates.extend(road_shape[1:])
            else:
                route_coordinates.extend(road_shape)

        else:

            # Fallback to the coordinates of the two road nodes
            if not route_coordinates:
                route_coordinates.append(
                    node_coordinates[current_node]
                )

            route_coordinates.append(
                node_coordinates[next_node]
            )

    # Handle a journey where start and destination are the same node
    if len(path) == 1:
        route_coordinates.append(node_coordinates[path[0]])

    return route_coordinates



# --------------------------------------------------
# INTERACTIVE OPENSTREETMAP ROUTE VISUALIZATION
# --------------------------------------------------

if algorithm_results is not None:

    if all(
        result["found"]
        for result in [greedy, astar, dijkstra]
    ):

        st.divider()
        st.subheader("Interactive Road Map")

        st.write(
            "Choose which algorithm routes you want to "
            "visualize on the OpenStreetMap."
        )

        # AVAILABLE ROUTES
        route_definitions = [
            {
                "name": "Greedy Best-First Search",
                "result": greedy,
                "color": "#f59e0b",
                "weight": 6,
                "dash": None
            },
            {
                "name": "A* Search",
                "result": astar,
                "color": "#22d3ee",
                "weight": 6,
                "dash": None
            },
            {
                "name": "Dijkstra",
                "result": dijkstra,
                "color": "#22c55e",
                "weight": 5,
                "dash": "10, 8"
            }
        ]

        available_routes = [
            route["name"]
            for route in route_definitions
        ]

        # ROUTE SELECTION
        selected_routes = st.multiselect(
            "Select algorithms to display",
            options=available_routes,
            default=available_routes,
            key="selected_route_layers"
        )

        if not selected_routes:

            st.info(
                "Select at least one algorithm to display its route."
            )

        else:

            # JOURNEY COORDINATES
            start_coordinates = road_data["start_coordinates"]
            goal_coordinates = road_data["goal_coordinates"]

            center_lat = (
                start_coordinates[0] + goal_coordinates[0]
            ) / 2

            center_lon = (
                start_coordinates[1] + goal_coordinates[1]
            ) / 2

            # CREATE MAP
            route_map = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=14,
                tiles="OpenStreetMap",
                control_scale=True
            )

            # START MARKER
            folium.Marker(
                location=start_coordinates,
                popup=f"Start: {road_data['start_place']}",
                tooltip="Starting Location",
                icon=folium.Icon(
                    color="green",
                    icon="play",
                    prefix="fa"
                )
            ).add_to(route_map)

            # DESTINATION MARKER
            folium.Marker(
                location=goal_coordinates,
                popup=f"Destination: {road_data['destination_place']}",
                tooltip="Destination",
                icon=folium.Icon(
                    color="red",
                    icon="flag",
                    prefix="fa"
                )
            ).add_to(route_map)

            # DRAW SELECTED ROUTES
            for route in route_definitions:

                if route["name"] not in selected_routes:
                    continue

                route_group = folium.FeatureGroup(
                    name=route["name"],
                    show=True
                )

                route_coordinates = build_route_coordinates(
                    route["result"]["path"],
                    road_data
                )

                line_options = {
                    "locations": route_coordinates,
                    "color": route["color"],
                    "weight": route["weight"],
                    "opacity": 0.9,
                    "tooltip": (
                        f"{route['name']} - "
                        f"{route['result']['distance_km']:.3f} km"
                    )
                }

                if route["dash"]:
                    line_options["dash_array"] = route["dash"]

                folium.PolyLine(
                    **line_options
                ).add_to(route_group)

                route_group.add_to(route_map)

            # MAP LAYER CONTROL
            folium.LayerControl(
                collapsed=False
            ).add_to(route_map)

            # FIT MAP TO JOURNEY
            route_map.fit_bounds(
                [
                    start_coordinates,
                    goal_coordinates
                ],
                padding=(40, 40)
            )

            # DISPLAY MAP
            st_folium(
                route_map,
                width=None,
                height=650,
                key="smart_route_map"
            )

            st.caption(
                "Map data © OpenStreetMap contributors. "
                "Routes calculated by SmartRouteAI."
            )

            # ROUTE LEGEND
            st.markdown("### Route Legend")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("🟠 **Greedy**")

            with col2:
                st.markdown("🔵 **A***")

            with col3:
                st.markdown("🟢 **Dijkstra (dashed)**")
