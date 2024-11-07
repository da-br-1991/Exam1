import csv
import pickle

#exercise 1: Reading Inputs
def csv_import_comma(path):
    data = []

    with open(path, 'r', encoding='utf8') as csv_data:
        next(csv_data)
        reader = csv.reader(csv_data, delimiter=',')
        data_before_split = list(reader)
        for i in data_before_split:
            temp_list = []
            for j in i:
                new_var = j.strip()
                temp_list.append(new_var)
            data.append(temp_list)

        return data

def csv_import_semicolon(path):
    data = []

    with open(path, 'r', encoding='utf8') as csv_data:
        next(csv_data)
        reader = csv.reader(csv_data, delimiter=';')
        data_before_split = list(reader)
        for i in data_before_split:
            temp_list = []
            for j in i:
                new_var = j.strip()
                temp_list.append(new_var)
            data.append(temp_list)

        return data

def txt_import(path):
    data = []

    with open(path, encoding='utf8') as file:
        next(file)
        for line in file:
            line = line.strip()

            if ',' in line:
                customer, order = line.split(',')
                data.append([customer.strip(), order.strip()])
            else:
                customer = line[:-2].strip()
                order = line[-2:]
                data.append([customer , order])

    return data

coordinates_list= csv_import_comma('input_data/coordinates.csv')
distances_list = csv_import_comma('input_data/distance.csv')
facilities_list = csv_import_semicolon('input_data/facilities.csv')
customers_list = txt_import('input_data/customers.txt')

customer_distance_list =[]

for from_to, distance in distances_list:
    parts = from_to.split("->")
    order_person = parts[0].strip()
    location = parts[1].strip()
    distance_to_location = float(distance)
    customer_distance_list.append([order_person, location, distance_to_location])



#variables for exercise 2
capacity_one = int(facilities_list[0][1])
capacity_two = int(facilities_list[1][1])
capacity_three = int(facilities_list[2][1])
capacity_four = int(facilities_list[3][1])

order_amount_list = customers_list
multi_order_amount_list = customers_list

order_list_facility_one = []
order_list_facility_two = []
order_list_facility_three = []
order_list_facility_four = []
outstanding_order_list = []

#variables for exercise 3
multi_capacity_one = int(facilities_list[0][1])
multi_capacity_two = int(facilities_list[1][1])
multi_capacity_three = int(facilities_list[2][1])
multi_capacity_four = int(facilities_list[3][1])
multi_order_list_facility_one = []
multi_order_list_facility_two = []
multi_order_list_facility_three = []
multi_order_list_facility_four = []
multi_outstanding_order_list = []
multi_customer_distance_list = customer_distance_list

#exercise 2:

for from_to, distance in distances_list:
    parts = from_to.split("->")
    order_person = parts[0].strip()
    location = parts[1].strip()
    distance_to_location = float(distance)
    customer_distance_list.append([order_person, location, distance_to_location])

while True:
    if len(order_amount_list) == 0:
        break
    max_order_amount = 0
    max_customer = None
    shortest_distance = float('inf')
    closest_location = None

    for customer, order in order_amount_list:
        if int(order) > max_order_amount:
            max_order_amount = int(order)
            max_customer = customer

    filtered_list = [entry for entry in order_amount_list if entry[0] != max_customer]
    order_amount_list = filtered_list

    filtered_list_two = [entry for entry in multi_customer_distance_list if entry[0] == max_customer]
    sorted_max_customer_distance_list = sorted(filtered_list_two, key=lambda x: x[2])

    for order_person, location, distance in sorted_max_customer_distance_list:
        if order_person == max_customer:
            if max_order_amount is None:
                break
            elif max_order_amount > capacity_one and max_order_amount > capacity_two and max_order_amount > capacity_three and max_order_amount > capacity_four:
                outstanding_order_list.append([max_customer, max_order_amount])
                break
            if location == "Werk 1":
                if max_order_amount <= capacity_one:
                    capacity_one = capacity_one - max_order_amount
                    order_list_facility_one.append([max_customer, max_order_amount])
                    max_order_amount = None
                else:
                    continue
            elif location == "Werk 2":
                if max_order_amount <= capacity_two:
                    capacity_two = capacity_two - max_order_amount
                    order_list_facility_two.append([max_customer, max_order_amount])
                    max_order_amount = None
                else:
                    continue
            elif location == "Werk 3":
                if max_order_amount <= capacity_three:
                    capacity_three = capacity_three - max_order_amount
                    order_list_facility_three.append([max_customer, max_order_amount])
                    max_order_amount = None
                else:
                    continue
            elif location == "Werk 4":
                if max_order_amount <= capacity_four:
                    capacity_four = capacity_four - max_order_amount
                    order_list_facility_four.append([max_customer, max_order_amount])
                    max_order_amount = None
                else:
                    continue

#create pickle file for exercise 2

with open("data/part2.pkl", "wb") as f:
    pickle.dump((order_list_facility_one, order_list_facility_two, order_list_facility_three, order_list_facility_four, outstanding_order_list), f)

#exercise 3:

while True:
    if len(multi_order_amount_list) == 0:
        break
    max_order_amount = 0
    max_customer = None
    shortest_distance = float('inf')
    closest_location = None

    for customer, order in multi_order_amount_list:
        if int(order) > max_order_amount:
            max_order_amount = int(order)
            max_customer = customer

    # Create filtered list without the current Max_Customer for the next run of the While loop
    filtered_list = [entry for entry in multi_order_amount_list if entry[0] != max_customer]
    multi_order_amount_list = filtered_list

    # Create a sorted and filtered distance list by Max_Customer and lowest distance first
    filtered_list_two = [entry for entry in multi_customer_distance_list if entry[0] == max_customer]
    sorted_max_customer_distance_list = sorted(filtered_list_two, key=lambda x: x[2])

    for order_person, location, distance in sorted_max_customer_distance_list:
        if order_person == max_customer:
            if max_order_amount == 0:
                break
            elif location == "Werk 1":
                if max_order_amount <= multi_capacity_one:
                    multi_capacity_one = multi_capacity_one - max_order_amount
                    multi_order_list_facility_one.append([max_customer, max_order_amount])
                    max_order_amount = max_order_amount - max_order_amount
                if max_order_amount > multi_capacity_one:
                    if multi_capacity_one == 0:
                        continue
                    else:
                        split_order  = multi_capacity_one
                        multi_capacity_one = multi_capacity_one - split_order
                        multi_order_list_facility_one.append([max_customer, split_order])
                        max_order_amount = max_order_amount - split_order
            elif location == "Werk 2":
                if max_order_amount <= multi_capacity_two:
                    multi_capacity_two = multi_capacity_two - max_order_amount
                    multi_order_list_facility_two.append([max_customer, max_order_amount])
                    max_order_amount = max_order_amount - max_order_amount
                if max_order_amount > multi_capacity_two:
                    if multi_capacity_two == 0:
                        continue
                    else:
                        split_order = multi_capacity_two
                        multi_capacity_two = multi_capacity_two - split_order
                        multi_order_list_facility_two.append([max_customer, split_order])
                        max_order_amount = max_order_amount - split_order
            elif location == "Werk 3":
                if max_order_amount <= multi_capacity_three:
                    multi_capacity_three = multi_capacity_three - max_order_amount
                    multi_order_list_facility_three.append([max_customer, max_order_amount])
                    max_order_amount = max_order_amount - max_order_amount
                if max_order_amount > multi_capacity_three:
                    if multi_capacity_three == 0:
                        continue
                    else:
                        split_order = multi_capacity_three
                        multi_capacity_three = multi_capacity_three - split_order
                        multi_order_list_facility_three.append([max_customer, split_order])
                        max_order_amount = max_order_amount - split_order
            elif location == "Werk 4":
                if max_order_amount <= multi_capacity_four:
                    multi_capacity_four = multi_capacity_four - max_order_amount
                    multi_order_list_facility_four.append([max_customer, max_order_amount])
                    max_order_amount = max_order_amount - max_order_amount
                if max_order_amount > multi_capacity_four:
                    if multi_capacity_four == 0:
                        continue
                    else:
                        split_order = multi_capacity_four
                        multi_capacity_four = multi_capacity_four - split_order
                        multi_order_list_facility_four.append([max_customer, split_order])
                        max_order_amount = max_order_amount - split_order
            else:
                multi_outstanding_order_list.append([max_customer, max_order_amount])

#create pickle file for exercise 3

with open("data/part3.pkl", "wb") as f:
    pickle.dump((multi_order_list_facility_one, multi_order_list_facility_two, multi_order_list_facility_three, multi_order_list_facility_four, multi_outstanding_order_list), f)


#exercise 4:

#loading pickle data
with open("data/part2.pkl", "rb") as f:
    loaded_data = pickle.load(f)

pkl_facility_one_order_list, pkl_facility_two_order_list, pkl_facility_three_order_list, pkl_facility_four_order_list, pkl_outstanding_order_list = loaded_data

with open("data/part3.pkl", "rb") as f:
    loaded_data2 = pickle.load(f)

pkl_facility_one_multi_order_list, pkl_facility_two_multi_order_list, pkl_facility_three_multi_order_list, pkl_facility_four_multi_order_list, pkl_outstanding_multi_order_list = loaded_data2

cap_util_facility_one = 0
cap_util_facility_two = 0
cap_util_facility_three = 0
cap_util_facility_four = 0
missing_order = 0

cap_util_multi_facility_one = 0
cap_util_multi_facility_two = 0
cap_util_multi_facility_three = 0
cap_util_multi_facility_four = 0
missing_multi_order = 0

#variant 1: single
for customer, order in pkl_facility_one_order_list:
    cap_util_facility_one += order
cap_util_facility_one = round((cap_util_facility_one / int(facilities_list[0][1])) * 100,1)

for customer, order in pkl_facility_two_order_list:
    cap_util_facility_two += order
cap_util_facility_two = round((cap_util_facility_two / int(facilities_list[1][1])) * 100, 1)

for customer, order in pkl_facility_three_order_list:
    cap_util_facility_three += order
cap_util_facility_three = round((cap_util_facility_three / int(facilities_list[2][1])) * 100,1)

for customer, order in pkl_facility_four_order_list:
    cap_util_facility_four += order
cap_util_facility_four = round((cap_util_facility_four / int(facilities_list[3][1])) * 100,1)

for customer, order in pkl_outstanding_order_list:
    missing_order += order


#variant 2: multi
for customer, order in pkl_facility_one_multi_order_list:
    cap_util_multi_facility_one += order
cap_util_multi_facility_one = round((cap_util_multi_facility_one / int(facilities_list[0][1])) * 100,1)

for customer, order in pkl_facility_two_multi_order_list:
    cap_util_multi_facility_two += order
cap_util_multi_facility_two = round((cap_util_multi_facility_two / int(facilities_list[1][1])) * 100, 1)

for customer, order in pkl_facility_three_multi_order_list:
    cap_util_multi_facility_three += order
cap_util_multi_facility_three = round((cap_util_multi_facility_three / int(facilities_list[2][1])) * 100,1)

for customer, order in pkl_facility_four_multi_order_list:
    cap_util_multi_facility_four += order
cap_util_multi_facility_four = round((cap_util_multi_facility_four / int(facilities_list[3][1])) * 100,1)

for customer, order in pkl_outstanding_multi_order_list:
    missing_multi_order += order

#Terminal output:

print("\nExercise 2:","\n")
print("Order list facility 1:", order_list_facility_one)
print("Order list facility 2:", order_list_facility_two)
print("Order list facility 3:", order_list_facility_three)
print("Order list facility 4:", order_list_facility_four, "\n")
print("Outstanding orders:", outstanding_order_list,"\n")
print("Open capacities facility 1:", capacity_one)
print("Open capacities facility 2:", capacity_two)
print("Open capacities facility 3:", capacity_three)
print("Open capacities facility 4:", capacity_four,"\n")

print("Exercise 3:\n")
print("Order list facility 1:",multi_order_list_facility_one)
print("Order list facility 2:",multi_order_list_facility_two)
print("Order list facility 3:",multi_order_list_facility_three)
print("Order list facility 4:",multi_order_list_facility_four,"\n")
print("Outstanding orders:",multi_outstanding_order_list,"\n")
print("Open capacities facility 1:",multi_capacity_one)
print("Open capacities facility 2:",multi_capacity_two)
print("Open capacities facility 3:",multi_capacity_three)
print("Open capacities facility 4:",multi_capacity_four,"\n")

print("Exercise 4:\n")
print("Variant 1 without splitting the order quantity across several locations:")
print("Transport costs:")
print("Capacity utilisation of facility 1:", cap_util_facility_one, "%")
print("Capacity utilisation of facility 2:", cap_util_facility_two, "%")
print("Capacity utilisation of facility 3:", cap_util_facility_three, "%")
print("Capacity utilisation of facility 4:", cap_util_facility_four, "%")
print("Missing order quantities:", missing_order)
print("\nVariant 2 with splitting of the order quantity to several locations:")
print("Transport costs:")
print("Capacity utilisation of facility 1:", cap_util_multi_facility_one, "%")
print("Capacity utilisation of facility 2:", cap_util_multi_facility_two, "%")
print("Capacity utilisation of facility 3:", cap_util_multi_facility_three, "%")
print("Capacity utilisation of facility 4:", cap_util_multi_facility_four, "%")
print("Missing order quantities:", missing_multi_order)