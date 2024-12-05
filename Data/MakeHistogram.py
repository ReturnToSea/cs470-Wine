from ExtractData import find_orders_by_item, parse_orders, write_to_file, find_orders_by_item, print_specific_items


#TODO: create a histogram using function from Extract Data. We want to find the frequency of an item based on time of day.

from ExtractData import find_orders_by_item, parse_orders
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter

# Function grabs wines based off of keyword.
def get_items_by_keyword(file_path, keyword):
    orders = parse_orders(file_path)
    matching_items = set()
    for order in orders:
        for item in order["items"]:
            if keyword.lower() in item.lower():
                matching_items.add(item)
    return sorted(matching_items)

# multi histogram code maybe
def count_items_frequency_by_hour(orders, items):
    hourly_item_counter = Counter()
    for item_name in items:
        matching_orders = find_orders_by_item(orders, item_name)
        for order in matching_orders:
            timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
            hour = timestamp.hour
            hourly_item_counter[hour] += 1
    return hourly_item_counter


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
def count_item_frequencies_by_hour(orders, matching_items):
    """
    Count the hourly frequency for multiple distinct items.
    Returns a dictionary with item names as keys and hourly counters as values.
    """
    item_hourly_counts = {}
    for item in matching_items:
        hourly_item_counter = Counter()
        matching_orders = find_orders_by_item(orders, item)
        for order in matching_orders:
            timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
            hour = timestamp.hour
            hourly_item_counter[hour] += 1
        item_hourly_counts[item] = hourly_item_counter
    return item_hourly_counts

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

def plot_item_frequencies_by_hour_grouped(item_hourly_counts, keyword):
    """
    Plot a histogram with separate bars for each item in the group.
    """
    hours = list(range(24))
    plt.figure(figsize=(12, 6))

    for item, hourly_counter in item_hourly_counts.items():
        item_counts = [hourly_counter.get(hour, 0) for hour in hours]
        plt.bar(
            hours,
            item_counts,
            alpha=0.6,  # Transparency to handle overlaps
            label=item
        )

    plt.title(f"Frequency of Items Matching '{keyword}' by Hour of Day")
    plt.xlabel("Hour of Day")
    plt.ylabel("Frequency of Items Ordered")
    plt.xticks(hours)
    plt.legend(loc='upper right')
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

def count_grouped_item_frequencies_by_day(orders, matching_items):
    """
    Count the daily frequency for multiple distinct items.
    Returns a dictionary with item names as keys and daily counters as values.
    """
    grouped_daily_counts = {}
    for item in matching_items:
        daily_item_counter = Counter()
        matching_orders = find_orders_by_item(orders, item)
        for order in matching_orders:
            timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
            day = timestamp.date()
            daily_item_counter[day] += 1
        grouped_daily_counts[item] = daily_item_counter
    return grouped_daily_counts


def plot_grouped_item_frequencies_by_day(grouped_daily_counts, keyword):
    """
    Plot a grouped bar chart showing the daily frequency of items.
    """
    all_days = sorted(set(day for counter in grouped_daily_counts.values() for day in counter.keys()))
    x = range(len(all_days))  # Positions for days on the x-axis

    plt.figure(figsize=(12, 6))

    bar_width = 0.2  # Width of each bar
    offset = 0       # Initial offset for bar positions

    for item, daily_counter in grouped_daily_counts.items():
        item_counts = [daily_counter.get(day, 0) for day in all_days]
        plt.bar(
            [pos + offset for pos in x],  # Offset the bars for this item
            item_counts,
            width=bar_width,
            label=item,
            alpha=0.7  # Slight transparency to make overlaps more visible
        )
        offset += bar_width  # Shift the next group of bars

    plt.title(f"Frequency of Items Matching '{keyword}' by Day")
    plt.xlabel("Day")
    plt.ylabel("Frequency of Items Ordered")
    plt.xticks([pos + bar_width * (len(grouped_daily_counts) / 2 - 0.5) for pos in x],
               [day.strftime("%Y-%m-%d") for day in all_days], rotation=45)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


# Function to generate the graph based on user selections
def generate_graph():
    keyword = wine_combobox.get()
    period = period_var.get()
    date_str = date_entry.get().strip() if period == "Specific Date" else None

    if not keyword:
        print("Debug: No keyword entered.")
        return

    file_path = 'CsvReaderOutput.txt'
    orders = parse_orders(file_path)
    matching_items = get_items_by_keyword(file_path, keyword)

    if not matching_items:
        print(f"Debug: No items found for keyword '{keyword}'.")
        return

    if period == "24-hour period":
        # Handle 24-hour distribution for grouped items
        item_hourly_counts = count_item_frequencies_by_hour(orders, matching_items)
        plot_item_frequencies_by_hour_grouped(item_hourly_counts, keyword)
    elif period == "All days period":
        # Handle all-day distribution for grouped items
        grouped_daily_counts = count_grouped_item_frequencies_by_day(orders, matching_items)
        plot_grouped_item_frequencies_by_day(grouped_daily_counts, keyword)
    elif period == "Specific Date":
        try:
            # Handle specific date distribution for grouped items
            selected_date = datetime.strptime(date_str, "%m/%d/%Y").date()
            item_hourly_counts = {}
            for item in matching_items:
                hourly_counter = count_item_frequency_by_hour_and_date(orders, item, selected_date)
                item_hourly_counts[item] = hourly_counter
            plot_item_frequencies_by_hour_grouped(item_hourly_counts, keyword)
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
wine_combobox.insert(0, "Enter keyword (e.g., LITTLE GIANT)")

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
