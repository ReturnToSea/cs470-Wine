
import re
# Split data into lines

#Bugs that need to be fixed due to incosistencies in the data
#TODO: Check if date count is working right

#TODO:  Find fix for formating not always being the same
#           - Date is not always in the right cell
#           - Data is not always appearing in the right cell
#       Find fix for some NO SALE cells still having a charge in the data
#       Find fix for empty sales still having a charge in the data
#       Find fix for a sale having items sold but no total charge
#       Find fix for void just breaking the data sometimes
#TODO:  Change it to read in from a file instead of text
#TODO:  Change it to check for 1 of each recuired cell and if it does not find that void that sale

def is_number(line):
    try:
        float(line)
        return True
    except ValueError:
        return False

def parse_orders(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    lines = data.strip().splitlines()

    orders = []
    current_order = None
    items = []
    total_cost = None
    payment_method = None
    gst_subtotal_count = 0
    gst_amount_count = 0
    date_count = 0



    payment_method_pattern = re.compile(r"(CASH|EFTPOS|AMEX)")

    for i in range(len(lines)):
        line = lines[i]
        if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line):
            date_count += 1
            if current_order is not None:
                if gst_subtotal_count == 1 and gst_amount_count == 1 and date_count == 1:
                    orders.append({
                        "order_timestamp": current_order,
                        "items": items,
                        "total_cost": total_cost,
                        "payment_method": payment_method
                    })
            current_order = line
            items = []
            total_cost = None
            payment_method = None
            gst_subtotal_count = 0
            gst_amount_count = 0
            date_count = 0

        elif "GST Subtotal" in line:
            gst_subtotal_count += 1

        elif "GST Amount" in line:
            gst_amount_count += 1

        elif payment_method_pattern.search(line):
            if i + 1 < len(lines):
                payment_method = payment_method_pattern.search(line).group()
                total_cost = float(lines[i + 1])
        elif "$" not in line and "Discount" not in line and not line.startswith(("-", "CASH", "GST", "SUBTOTAL", "Change", "SKIRMISH/BSHOP", "TODD K", "TRACEY LANGE", "ROUNDING")) and not is_number(line):
            items.append(line.strip())

    if current_order is not None and gst_subtotal_count == 1 and gst_amount_count == 1 and date_count == 1:
        orders.append({
            "order_timestamp": current_order,
            "items": items,
            "total_cost": total_cost,
            "payment_method": payment_method
        })
    
    return orders

def write_to_file(orders, filename="Orders.txt"):
    with open("Orders.txt", "w") as file:
        for order in orders:
            file.write(f"Order Timestamp: {order['order_timestamp']}\n")
            file.write(f"Total Cost: {order['total_cost']}\n")
            file.write(f"Payment Method: {order['payment_method']}\n")
            file.write(f"Items: {', '.join(order['items'])}\n")
            file.write('-' * 40 + "\n")

def find_orders_by_item(orders, item_name):
    matching_orders = []
    for order in orders:
        if any(item_name.lower() in item.lower() for item in order['items']):
            matching_orders.append(order)
    return matching_orders

def print_specific_items(matching_orders):
    #specific_item = "GREAT NTHN ORIGINAL STUB CTN"
    #matching_orders = find_orders_by_item(specific_item)
    if matching_orders:
        for order in matching_orders:
            print(f"Order Timestamp: {order['order_timestamp']}")
            print(f"Total Cost: {order['total_cost']}")
            print(f"Payment Method: {order['payment_method']}")
            print(f"Items: {', '.join(order['items'])}")
            print('-' * 40)

file_path = 'CsvReaderOutput.txt'
orders = parse_orders(file_path)
write_to_file(orders, "Orders.txt")
specific_item = "GREAT NTHN ORIGINAL STUB CTN"
matching_orders = find_orders_by_item(orders, specific_item)
print_specific_items(matching_orders)
