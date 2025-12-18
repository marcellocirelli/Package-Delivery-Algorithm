import hash_table
import datetime

# Instantiates hash table
table = hash_table.HashTable()

# Package class for creating package objects with CSV fields
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, special_notes, loading_time, delivery_time):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.loading_time = loading_time
        self.delivery_time = delivery_time

    # str and repr methods for debugging
    def __str__(self):
        return (
            f"Package {self.package_id} | "
            f"Address: {self.address}, {self.city}, {self.state} {self.zip_code} | "
            f"Deadline: {self.deadline} | "
            f"Weight: {self.weight} | "
            f"Notes: {self.special_notes} | "
            f"Loaded at: {self.loading_time} | "
            f"Delivered at: {self.delivery_time}"
        )

    def __repr__(self):
        return (
            f"Package {self.package_id} | "
            f"Address: {self.address}, {self.city}, {self.state} {self.zip_code} | "
            f"Deadline: {self.deadline} | "
            f"Weight: {self.weight} | "
            f"Notes: {self.special_notes} | "
            f"Loaded at: {self.loading_time} | "
            f"Delivered at: {self.delivery_time}"
        )

# Opens the package file and inserts packages to the hash table
with open("package_file.csv", "r") as package_file:
    header = package_file.readline()

    for line in package_file:
        parts = line.strip().split(",")

        package_id = int(parts[0])
        address = parts[1]
        city = parts[2]
        state = parts[3]
        zip_code = parts[4]
        deadline = parts[5]
        weight = parts[6]
        special_notes = parts[7] if len(parts) > 7 else ""

        package = Package(
            package_id,
            address,
            city,
            state,
            zip_code,
            deadline,
            weight,
            special_notes,
            loading_time=None,
            delivery_time=None
        )

        table.insert(package)

distances = []
address_index_map = {}

# Stores an address distance map from the distance table CSV
with open("distance_table.csv", "r") as distance_file:
    index_counter = 0
    for line in distance_file:
        parts = line.strip().split(",")
        address = parts.pop(0)
        address_index_map[address] = index_counter
        distances.append(parts)
        index_counter += 1

# Function that parses package deadlines into datetime
def parse_deadline(deadline_string):
    text = deadline_string.strip()
    if text.upper() == "EOD":
        return datetime.datetime(2025, 10, 31, 23, 59)
    return datetime.datetime.strptime(
        "2025-10-31 " + text,
        "%Y-%m-%d %I:%M %p"
    )

# Main self-adjusting greedy algorithm for package routing
def deliver_package(truck_packages, start_time):
    current_location = "4001 South 700 East"
    current_time = start_time
    total_miles = 0.0

    # Keeps delivering until the truck has no packages
    while len(truck_packages) > 0:
        closest_package = None
        closest_deadline = None
        closest_distance = None

        # Checks the distance between addresses for every package on a truck
        for truck_package in truck_packages:
            pkg_obj = table.lookup(truck_package)

            from_address = current_location
            to_address = pkg_obj.address

            i = address_index_map[from_address]
            j = address_index_map[to_address]

            d = distances[i][j]
            if d == "":
                d = distances[j][i]
            miles = float(d)

            pkg_deadline = parse_deadline(pkg_obj.deadline)

            # Prefer the package with the earliest deadline
            # If theres a tie, chooses the closest one
            if closest_distance is None:
                closest_package = truck_package
                closest_deadline = pkg_deadline
                closest_distance = miles
            else:
                if pkg_deadline < closest_deadline:
                    closest_package = truck_package
                    closest_deadline = pkg_deadline
                    closest_distance = miles
                elif pkg_deadline == closest_deadline and miles < closest_distance:
                    closest_package = truck_package
                    closest_deadline = pkg_deadline
                    closest_distance = miles

        # Looks up the chosen next package from the hash table
        deliverable_package = table.lookup(closest_package)

        # Gets the distance of the next leg in miles, and how long
        from_address = current_location
        to_address = deliverable_package.address
        i = address_index_map[from_address]
        j = address_index_map[to_address]
        d = distances[i][j]
        if d == "":
            d = distances[j][i]
        leg_miles = float(d)

        hours = leg_miles / 18.0
        minutes = hours * 60.0

        current_time = current_time + datetime.timedelta(minutes=minutes)

        # Timestamp the package/truck loading and delivery times
        if deliverable_package.loading_time is None:
            deliverable_package.loading_time = start_time
        deliverable_package.delivery_time = current_time

        # Increments the total mileage by the current leg
        total_miles += leg_miles

        # Moves the truck's current location to where we just delivered
        current_location = to_address
        # Removes a package from potential candidates
        truck_packages.remove(closest_package)

    # Final distance and time calculation for returning to the hub
    if current_location != "4001 South 700 East":
        from_address = current_location
        to_address = "4001 South 700 East"

        i = address_index_map[from_address]
        j = address_index_map[to_address]
        d = distances[i][j]
        if d == "":
            d = distances[j][i]
        back_miles = float(d)

        hours = back_miles / 18.0
        minutes = hours * 60.0

        current_time = current_time + datetime.timedelta(minutes=minutes)
        total_miles += back_miles

    return total_miles, current_time

# Loaded trucks
truck1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
truck2 = [3, 6, 8, 10, 11, 12, 17, 18, 21, 23, 25, 27, 28, 32, 36, 38]
truck3 = [2, 4, 5, 7, 9, 22, 24, 26, 33, 35, 39]

# For identifying which package is on which truck
package_to_truck = {}
for pid in truck1:
    package_to_truck[pid] = 1
for pid in truck2:
    package_to_truck[pid] = 2
for pid in truck3:
    package_to_truck[pid] = 3

# Start times for each truck
start_time_truck1 = datetime.datetime(2025, 10, 31, 8, 0)
start_time_truck2 = datetime.datetime(2025, 10, 31, 9, 5)
start_time_truck3 = datetime.datetime(2025, 10, 31, 10, 20)

# Runs the package routing
miles1, end1 = deliver_package(truck1, start_time_truck1)
miles2, end2 = deliver_package(truck2, start_time_truck2)
miles3, end3 = deliver_package(truck3, start_time_truck3)

# Function for returning the package status
def status_for(pkg, t):
    # Edge case for delayed packages
    flight_delay_time = datetime.datetime(2025, 10, 31, 9, 5)
    if pkg.package_id in (6, 25, 28, 32):
        if t < flight_delay_time:
            return "Delayed"

    truck_num = package_to_truck.get(pkg.package_id)

    if truck_num == 1:
        depart_time = start_time_truck1
    elif truck_num == 2:
        depart_time = start_time_truck2
    else:
        depart_time = start_time_truck3

    # Status: Delivered if we have a delivery_time, and it's <= the query time
    if pkg.delivery_time is not None and pkg.delivery_time <= t:
        return "Delivered"

    # Status: At Hub ff it's before the truck leaves
    if t < depart_time:
        return "At Hub"

    # Status: En Route if the truck has left but package isn't delivered yet
    return "En Route"

# Small helper for parsing user input time into datetime
def parse_query_time(user_input):
    # expects "HH:MM" 24-hour
    hour_str, minute_str = user_input.strip().split(":")
    h = int(hour_str)
    m = int(minute_str)
    return datetime.datetime(2025, 10, 31, h, m)

# Main user interface
def ui():
    # Prompts the user for a time
    user_t = input("Enter a time (HH:MM in 24-hr, for Oct 31 2025): ").strip()
    query_time = parse_query_time(user_t)

    # Updates the address for package 9 if the user inputs a >= 10:20 AM
    cutoff = datetime.datetime(2025, 10, 31, 10, 20)
    if query_time >= cutoff:
        pkg9 = table.lookup(9)
        pkg9.address = "410 S State St"
        pkg9.city = "Salt Lake City"
        pkg9.state = "UT"
        pkg9.zip_code = "84111"
    else:
        pkg9 = table.lookup(9)
        pkg9.address = "300 State St"
        pkg9.city = "Salt Lake City"
        pkg9.state = "UT"
        pkg9.zip_code = "84103"

    for pid in range(1, 41):
        pkg = table.lookup(pid)
        if pkg is None:
            continue

        truck_num = package_to_truck.get(pid, "N/A")

        # Prints a delivery time if the package has been delivered, otherwise "Not delivered"
        if pkg.delivery_time is None:
            delivered_txt = "Not delivered"
        else:
            delivered_txt = pkg.delivery_time.strftime("%I:%M %p").lstrip("0")

        deadline_txt = pkg.deadline
        status_txt = status_for(pkg, query_time)

        # Main print line
        print(
            f"Package {pkg.package_id} | "
            f"Delivery Address: {pkg.address}, {pkg.city}, {pkg.state} {pkg.zip_code} | "
            f"Delivery Time: {delivered_txt} | "
            f"Delivery Deadline: {deadline_txt} | "
            f"Truck Number: {truck_num} | "
            f"Delivery Status: {status_txt}"
        )


        finished_time = max(end1, end2, end3)
        total_miles = miles1 + miles2 + miles3

    # Shows the total mileage if the user inputs a time after all trucks have finished
    if query_time >= finished_time:
        print(f"\nTotal truck mileage: {total_miles:.1f} miles")

ui()