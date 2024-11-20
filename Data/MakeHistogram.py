from ExtractData import find_orders_by_item, parse_orders, write_to_file, find_orders_by_item, print_specific_items


#TODO: create a histogram using function from Extract Data. We want to find the frequency of an item based on time of day.

from ExtractData import find_orders_by_item, parse_orders
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter

# Function to load and extract wine names
def get_wine_names(file_path):
    orders = parse_orders(file_path)
    wine_names = set()  # Use a set to avoid duplicates
    for order in orders:
        # Loop through items in each order and add them to the wine_names set
        for item in order["items"]:
            wine_names.add(item)
    return sorted(wine_names)

# Function to count item purchases by hour (24-hour period) for a specific date
def count_item_frequency_by_hour_and_date(orders, item_name, date):
    hourly_item_counter = Counter()
    matching_orders = find_orders_by_item(orders, item_name)
    
    for order in matching_orders:
        timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
        if timestamp.date() == date:
            hour = timestamp.hour
            hourly_item_counter[hour] += 1
    
    return hourly_item_counter

# Function to count item purchases by hour (all-time 24-hour distribution)
def count_item_frequency_by_hour(orders, item_name):
    hourly_item_counter = Counter()
    matching_orders = find_orders_by_item(orders, item_name)
    
    for order in matching_orders:
        timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
        hour = timestamp.hour
        hourly_item_counter[hour] += 1
    
    return hourly_item_counter

# Function to count item purchases by day (all-time daily distribution)
def count_item_frequency_by_day(orders, item_name):
    daily_item_counter = Counter()
    matching_orders = find_orders_by_item(orders, item_name)
    
    for order in matching_orders:
        timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
        day = timestamp.date()
        daily_item_counter[day] += 1
    
    return daily_item_counter

# Function to plot the histogram based on hourly data
def plot_item_frequency_by_hour(hourly_item_counter, item_name, date=None):
    hours = list(range(24))
    item_counts = [hourly_item_counter.get(hour, 0) for hour in hours]
    
    plt.figure(figsize=(12, 6))
    plt.bar(hours, item_counts, color='skyblue', edgecolor='black')
    title = f"Frequency of '{item_name}' Ordered by Hour of Day"
    if date:
        title += f" (Date: {date})"
    plt.title(title)
    plt.xlabel("Hour of Day")
    plt.ylabel("Frequency of Item Ordered")
    plt.xticks(hours)
    plt.tight_layout()
    plt.show()

# Function to plot the histogram based on daily data
def plot_item_frequency_by_day(daily_item_counter, item_name):
    days = list(daily_item_counter.keys())
    item_counts = [daily_item_counter[day] for day in days]
    
    plt.figure(figsize=(12, 6))
    plt.bar(days, item_counts, color='skyblue', edgecolor='black')
    plt.title(f"Frequency of '{item_name}' Ordered by Day")
    plt.xlabel("Day")
    plt.ylabel("Frequency of Item Ordered")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to generate the graph based on user selections
def generate_graph():
    selected_wine = wine_combobox.get()
    period = period_var.get()
    date_str = date_entry.get().strip() if period == "Specific Date" else None

    if not selected_wine:
        print("Debug: No wine selected.")
        return

    file_path = 'CsvReaderOutput.txt'
    orders = parse_orders(file_path)

    if period == "24-hour period":
        hourly_item_counter = count_item_frequency_by_hour(orders, selected_wine)
        plot_item_frequency_by_hour(hourly_item_counter, selected_wine)
    elif period == "All days period":
        daily_item_counter = count_item_frequency_by_day(orders, selected_wine)
        plot_item_frequency_by_day(daily_item_counter, selected_wine)
    elif period == "Specific Date":
        try:
            selected_date = datetime.strptime(date_str, "%m/%d/%Y").date()
            hourly_item_counter = count_item_frequency_by_hour_and_date(orders, selected_wine, selected_date)
            plot_item_frequency_by_hour(hourly_item_counter, selected_wine, date_str)
        except ValueError:
            print("Debug: Invalid date format. Please use MM/DD/YYYY.")

# Set up the main Tkinter window
root = tk.Tk()
root.title("Wine Sales Frequency")

# Get the list of wine names dynamically
wine_names = get_wine_names('CsvReaderOutput.txt')

# Create a StringVar to hold the selected period (24-hour, all days, specific date)
period_var = tk.StringVar(value="24-hour period")

# Create and pack the dropdown for wine selection
wine_combobox = ttk.Combobox(root, values=wine_names, state="normal", width=40)
wine_combobox.pack(pady=10)

# Create and pack the radio buttons for selecting the time period
period_24hr = ttk.Radiobutton(root, text="24-hour period", variable=period_var, value="24-hour period")
period_all_days = ttk.Radiobutton(root, text="All days period", variable=period_var, value="All days period")
period_specific_date = ttk.Radiobutton(root, text="Specific Date", variable=period_var, value="Specific Date")
period_24hr.pack()
period_all_days.pack()
period_specific_date.pack()

# Create a date entry field that appears only when "Specific Date" is selected
date_entry_label = tk.Label(root, text="Enter Date (MM/DD/YYYY):")
date_entry = ttk.Entry(root, width=20)
date_entry_label.pack_forget()  # Initially hidden
date_entry.pack_forget()       # Initially hidden

# Show/Hide the date entry field based on selected period
def toggle_date_entry():
    if period_var.get() == "Specific Date":
        date_entry_label.pack(pady=5)
        date_entry.pack(pady=5)
    else:
        date_entry_label.pack_forget()
        date_entry.pack_forget()

# Bind the period change to toggle the date entry visibility
period_24hr.config(command=toggle_date_entry)
period_all_days.config(command=toggle_date_entry)
period_specific_date.config(command=toggle_date_entry)

# Create and pack the Generate Graph button
generate_button = ttk.Button(root, text="Generate Graph", command=generate_graph)
generate_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()





# # The code below handles makes a histogram based on price.
# import matplotlib.pyplot as plt
# import re
# from datetime import datetime

# # Initialize lists to store parsed data
# timestamps = []
# prices = []
# items_list = []

# # Read the data from the file
# with open("Orders.txt", "r") as file:
#     # Read each line and parse blocks
#     content = file.read().split("----------------------------------------\n")
#     for block in content:
#         if block.strip():  # Only process non-empty blocks
#             # Use regex to find each field
#             timestamp_match = re.search(r"Order Timestamp: (.+)", block)
#             price_match = re.search(r"Total Cost: ([\d.]+)", block)
#             items_match = re.search(r"Items: (.+)", block)
            
#             # Parse and append each field if found
#             if timestamp_match and price_match:
#                 try:
#                     timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d %H:%M:%S")
#                     price = float(price_match.group(1))  # Convert price to float
#                     items = items_match.group(1) if items_match else ""
                    
#                     timestamps.append(timestamp)
#                     prices.append(price)
#                     items_list.append(items)
#                 except ValueError:
#                     # Skip entries that cannot be parsed properly
#                     continue

# # Plot histogram for prices
# plt.figure(figsize=(10, 6))
# plt.hist(prices, bins=10, color='skyblue', edgecolor='black')
# plt.title("Distribution of Order Prices")
# plt.xlabel("Price")
# plt.ylabel("Frequency")
# plt.show()

# # The code below creates a histogram based on the item's frequency.
# import matplotlib.pyplot as plt
# import re
# from collections import Counter

# # Initialize a Counter to store item frequencies
# item_counter = Counter()

# # Read the data from the file
# with open("Orders.txt", "r") as file:
#     # Read each line and parse blocks
#     content = file.read().split("----------------------------------------\n")
#     for block in content:
#         if block.strip():  # Only process non-empty blocks
#             # Use regex to find the items
#             items_match = re.search(r"Items: (.+)", block)
            
#             if items_match:
#                 items = items_match.group(1)
#                 # Split items by comma and strip whitespace
#                 item_list = [item.strip() for item in items.split(",")]
#                 # Update the counter with these items
#                 item_counter.update(item_list)

# # Prepare data for plotting
# items, frequencies = zip(*item_counter.most_common(10))  # Get the top 10 items by frequency

# # Plot histogram for item frequencies
# plt.figure(figsize=(12, 6))
# plt.bar(items, frequencies, color='skyblue', edgecolor='black')
# plt.title("Top 10 Ordered Items by Frequency")
# plt.xlabel("Item Name")
# plt.ylabel("Frequency")
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()
# plt.show()

# # Time based histogram
# import matplotlib.pyplot as plt
# import re
# from datetime import datetime
# from collections import Counter

# # Initialize a Counter for counting items per hour
# hourly_item_counter = Counter()

# # Read the data from the file
# with open("Orders.txt", "r") as file:
#     # Read each line and parse blocks
#     content = file.read().split("----------------------------------------\n")
#     for block in content:
#         if block.strip():  # Only process non-empty blocks
#             # Use regex to find timestamp and items
#             timestamp_match = re.search(r"Order Timestamp: (.+)", block)
#             items_match = re.search(r"Items: (.+)", block)
            
#             if timestamp_match and items_match:
#                 # Parse timestamp and extract hour
#                 timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d %H:%M:%S")
#                 hour = timestamp.hour
                
#                 # Count items in the order
#                 items = items_match.group(1)
#                 item_list = [item.strip() for item in items.split(",")]
#                 num_items = len(item_list)
                
#                 # Update hourly count
#                 hourly_item_counter[hour] += num_items

# # Prepare data for plotting
# hours = list(range(24))  # Create a list for 24 hours
# item_counts = [hourly_item_counter.get(hour, 0) for hour in hours]  # Get item counts for each hour

# # Plot histogram for item count by hour
# plt.figure(figsize=(12, 6))
# plt.bar(hours, item_counts, color='skyblue', edgecolor='black')
# plt.title("Number of Items Ordered by Hour of Day")
# plt.xlabel("Hour of Day")
# plt.ylabel("Number of Items Ordered")
# plt.xticks(hours)  # Label each hour from 0 to 23
# plt.tight_layout()
# plt.show()

# # Based on time and frequency of all items.
# import matplotlib.pyplot as plt
# import re
# from datetime import datetime
# from collections import defaultdict, Counter

# # Dictionary to store item frequencies by hour
# hourly_item_counts = defaultdict(lambda: Counter())

# # Read the data from the file
# with open("Orders.txt", "r") as file:
#     # Read each line and parse blocks
#     content = file.read().split("----------------------------------------\n")
#     for block in content:
#         if block.strip():  # Only process non-empty blocks
#             # Use regex to find timestamp and items
#             timestamp_match = re.search(r"Order Timestamp: (.+)", block)
#             items_match = re.search(r"Items: (.+)", block)
            
#             if timestamp_match and items_match:
#                 # Parse timestamp and extract hour
#                 timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d %H:%M:%S")
#                 hour = timestamp.hour
                
#                 # Extract and clean item list
#                 items = items_match.group(1)
#                 item_list = [item.strip() for item in items.split(",")]
                
#                 # Update hourly count for each item
#                 for item in item_list:
#                     hourly_item_counts[item][hour] += 1

# # Get the top 5 most common items overall
# total_item_counts = Counter({item: sum(hour_counts.values()) for item, hour_counts in hourly_item_counts.items()})
# top_items = [item for item, _ in total_item_counts.most_common(20)]

# # Plot frequency of each top item by hour
# plt.figure(figsize=(12, 8))

# for item in top_items:
#     # Extract the hourly counts for the current item
#     item_hour_counts = [hourly_item_counts[item].get(hour, 0) for hour in range(24)]
#     plt.plot(range(24), item_hour_counts, label=item, marker='o')

# # Add plot details
# plt.title("Frequency of Top 5 Ordered Items by Hour of Day")
# plt.xlabel("Hour of Day")
# plt.ylabel("Frequency")
# plt.xticks(range(24))  # Set x-axis to show each hour
# plt.legend(title="Items")
# plt.grid(True)
# plt.tight_layout()
# plt.show()
