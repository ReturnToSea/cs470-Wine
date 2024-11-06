from ExtractData import find_orders_by_item

#TODO: create a histogram using function from Extract Data. We want to find the frequency of an item based on time of day.

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

import matplotlib.pyplot as plt
import re
from datetime import datetime
from collections import defaultdict, Counter

# Dictionary to store item frequencies by hour
hourly_item_counts = defaultdict(lambda: Counter())

# Read the data from the file
with open("Orders.txt", "r") as file:
    # Read each line and parse blocks
    content = file.read().split("----------------------------------------\n")
    for block in content:
        if block.strip():  # Only process non-empty blocks
            # Use regex to find timestamp and items
            timestamp_match = re.search(r"Order Timestamp: (.+)", block)
            items_match = re.search(r"Items: (.+)", block)
            
            if timestamp_match and items_match:
                # Parse timestamp and extract hour
                timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d %H:%M:%S")
                hour = timestamp.hour
                
                # Extract and clean item list
                items = items_match.group(1)
                item_list = [item.strip() for item in items.split(",")]
                
                # Update hourly count for each item
                for item in item_list:
                    hourly_item_counts[item][hour] += 1

# Get the top 5 most common items overall
total_item_counts = Counter({item: sum(hour_counts.values()) for item, hour_counts in hourly_item_counts.items()})
top_items = [item for item, _ in total_item_counts.most_common(20)]

# Plot frequency of each top item by hour
plt.figure(figsize=(12, 8))

for item in top_items:
    # Extract the hourly counts for the current item
    item_hour_counts = [hourly_item_counts[item].get(hour, 0) for hour in range(24)]
    plt.plot(range(24), item_hour_counts, label=item, marker='o')

# Add plot details
plt.title("Frequency of Top 5 Ordered Items by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Frequency")
plt.xticks(range(24))  # Set x-axis to show each hour
plt.legend(title="Items")
plt.grid(True)
plt.tight_layout()
plt.show()
