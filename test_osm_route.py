
# test_osm_route.py
# Test real-world road-network retrieval

from osm_data import get_osm_road_graph


def main():

    start = "Westlands, Nairobi, Kenya"
    destination = "Jomo Kenyatta International Airport, Nairobi, Kenya"

    try:

        result = get_osm_road_graph(
            start,
            destination
        )

        print("\nSMARTROUTEAI OSM TEST")
        print("=" * 45)

        print("Starting location:", result["start_place"])
        print("Destination:", result["destination_place"])

        print("Starting coordinates:", result["start_coordinates"])
        print("Destination coordinates:", result["goal_coordinates"])

        print("Start node:", result["start_node"])
        print("Goal node:", result["goal_node"])

        print(
            "\nSUCCESS: Real-world road graph retrieved."
        )

    except Exception as error:

        print("\nOSM ROUTING DATA ERROR")
        print(error)


if __name__ == "__main__":
    main()
