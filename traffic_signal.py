import time

# Function for signal timing
def get_signal_time(vehicle_count):
    if vehicle_count > 20:
        return 60
    elif vehicle_count > 10:
        return 40
    else:
        return 20

# Input vehicle counts
roads = {}

for i in range(1, 5):
    count = int(input(f"Enter vehicle count for Road {i}: "))
    roads[f"Road {i}"] = count

# Sort roads by vehicle count (highest first)
sorted_roads = sorted(roads.items(), key=lambda x: x[1], reverse=True)

print("\nTraffic Signal Status")
print("=" * 30)

for road, vehicles in sorted_roads:

    green_time = get_signal_time(vehicles)

    print(f"\n{road} --> GREEN")
    print(f"Vehicle Count : {vehicles}")
    print(f"Green Signal Time : {green_time} seconds")

    for other_road in roads:
        if other_road != road:
            print(f"{other_road} --> RED")

    time.sleep(2)
    print(f"{road} --> YELLOW")
    time.sleep(1)

print("\nTraffic Cycle Completed")