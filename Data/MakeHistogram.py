from ExtractData import find_orders_by_item, parse_orders, write_to_file, find_orders_by_item, print_specific_items


#TODO: create a histogram using function from Extract Data. We want to find the frequency of an item based on time of day.

from ExtractData import find_orders_by_item, parse_orders
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import Counter

# List of promotions with associated wine keywords
PROMOTIONS = {
    "2022-12-01": "BATCH BTL",
    "2022-12-08": "PLANTATION",
    "2022-12-09": "HAWKES",
    "2022-12-15": "LITTLE GIANT",
    "2022-12-16": "BURLEIGH",
    "2022-12-22": "ARIANE VODKA",
    "2022-12-23": "ARIANE VODKA"
}

# Function to load and extract wine names
def get_wine_names(file_path):
    orders = parse_orders(file_path)
    wine_names = set()
    for order in orders:
        for item in order["items"]:
            wine_names.add(item)
    return sorted(wine_names)

# Function to get top N wines by frequency
def get_top_n_wines(file_path, top_n=20):
    orders = parse_orders(file_path)
    wine_counter = Counter()
    for order in orders:
        for item in order["items"]:
            wine_counter[item] += 1
    top_wines = [wine for wine, _ in wine_counter.most_common(top_n)]
    return sorted(top_wines)

# Function to count item purchases by hour
def count_item_frequency_by_hour(orders, item_name):
    hourly_item_counter = Counter()
    matching_orders = find_orders_by_item(orders, item_name)
    for order in matching_orders:
        timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
        hour = timestamp.hour
        hourly_item_counter[hour] += 1
    return hourly_item_counter

# Function to count item purchases by hour for a specific date
def count_item_frequency_by_hour_and_date(orders, item_name, date):
    hourly_item_counter = Counter()
    matching_orders = find_orders_by_item(orders, item_name)
    for order in matching_orders:
        timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
        if timestamp.date() == date:
            hour = timestamp.hour
            hourly_item_counter[hour] += 1
    return hourly_item_counter

# Function to count item purchases by day
def count_item_frequency_by_day(orders, item_name):
    daily_item_counter = Counter()
    matching_orders = find_orders_by_item(orders, item_name)
    for order in matching_orders:
        timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S")
        day = timestamp.date()
        daily_item_counter[day] += 1
    return daily_item_counter

# Function to count item purchases by date range
def count_item_frequency_by_date_range(orders, wine_keyword, start_date, end_date):
    counter = Counter()
    for order in orders:
        for item in order["items"]:
            if wine_keyword in item.upper():
                timestamp = datetime.strptime(order["order_timestamp"], "%Y-%m-%d %H:%M:%S").date()
                if start_date <= timestamp <= end_date:
                    counter[timestamp] += 1
    return counter

# Function to highlight top N values in the histogram
def highlight_top_n_bars(ax, values, top_n, color='yellow'):
    top_indices = sorted(range(len(values)), key=lambda i: values[i], reverse=True)[:top_n]
    for i in top_indices:
        ax.patches[i].set_facecolor(color)

# Function to plot the histogram based on hourly data with top N highlighted
def plot_item_frequency_by_hour(hourly_item_counter, item_name, date=None, top_n=2):
    hours = list(range(24))
    item_counts = [hourly_item_counter.get(hour, 0) for hour in hours]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(hours, item_counts, color='skyblue', edgecolor='black')
    title = f"Frequency of '{item_name}' Ordered by Hour of Day"
    if date:
        title += f" (Date: {date})"
    ax.set_title(title)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Frequency of Item Ordered")
    ax.set_xticks(hours)

    # Highlight the top N bars
    highlight_top_n_bars(ax, item_counts, top_n)

    plt.tight_layout()
    plt.show()

# Function to plot the histogram based on daily data with top N highlighted
def plot_item_frequency_by_day(daily_item_counter, item_name, top_n=5):
    days = list(daily_item_counter.keys())
    item_counts = [daily_item_counter[day] for day in days]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(days, item_counts, color='skyblue', edgecolor='black')
    ax.set_title(f"Frequency of '{item_name}' Ordered by Day")
    ax.set_xlabel("Day")
    ax.set_ylabel("Frequency of Item Ordered")
    ax.set_xticks(days)

    # Highlight the top N bars
    highlight_top_n_bars(ax, item_counts, top_n)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to create histograms for promoted items
def plot_promoted_item_histograms(orders, promotion_date, wine_keyword):
    promotion_datetime = datetime.strptime(promotion_date, "%Y-%m-%d").date()
    week_before_start = promotion_datetime - timedelta(days=7)
    week_before_end = promotion_datetime - timedelta(days=1)
    week_after_start = promotion_datetime + timedelta(days=1)
    week_after_end = promotion_datetime + timedelta(days=7)

    week_before_counts = count_item_frequency_by_date_range(orders, wine_keyword, week_before_start, week_before_end)
    week_of_counts = count_item_frequency_by_date_range(orders, wine_keyword, promotion_datetime, promotion_datetime + timedelta(days=6))
    week_after_counts = count_item_frequency_by_date_range(orders, wine_keyword, week_after_start, week_after_end)

    def prepare_data(counter, start_date):
        return [counter.get(start_date + timedelta(days=i), 0) for i in range(7)]

    week_before_data = prepare_data(week_before_counts, week_before_start)
    week_of_data = prepare_data(week_of_counts, promotion_datetime)
    week_after_data = prepare_data(week_after_counts, week_after_start)

    week_before_labels = [(week_before_start + timedelta(days=i)).strftime("%m/%d") for i in range(7)]
    week_of_labels = [(promotion_datetime + timedelta(days=i)).strftime("%m/%d") for i in range(7)]
    week_after_labels = [(week_after_start + timedelta(days=i)).strftime("%m/%d") for i in range(7)]

    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.bar(week_before_labels, week_before_data, color="skyblue", edgecolor="black")
    plt.title(f"Week Before Promotion ({week_before_start.strftime('%m/%d')} - {week_before_end.strftime('%m/%d')})")
    plt.xlabel("Date")
    plt.ylabel("Sales")

    plt.subplot(1, 3, 2)
    plt.bar(week_of_labels, week_of_data, color="yellow", edgecolor="black")
    plt.title(f"Week of Promotion ({promotion_datetime.strftime('%m/%d')} - {(promotion_datetime + timedelta(days=6)).strftime('%m/%d')})")
    plt.xlabel("Date")

    plt.subplot(1, 3, 3)
    plt.bar(week_after_labels, week_after_data, color="green", edgecolor="black")
    plt.title(f"Week After Promotion ({week_after_start.strftime('%m/%d')} - {week_after_end.strftime('%m/%d')})")
    plt.xlabel("Date")

    plt.tight_layout()
    plt.show()

# Function to generate the graph based on user selections
def generate_graph():
    selected_wine = wine_combobox.get()
    period = period_var.get()
    date_str = date_entry.get().strip() if period == "Specific Date" else None

    if period == "Promoted Items":
        selected_promotion = promotion_date_combobox.get()
        if not selected_promotion:
            print("Debug: No promotion selected.")
            return
        promotion_date, wine_keyword = selected_promotion.split(" - ", 1)
        file_path = 'CsvReaderOutput.txt'
        orders = parse_orders(file_path)
        plot_promoted_item_histograms(orders, promotion_date, wine_keyword)
    elif period == "Top 20 Wines":
        selected_top_wine = top_wine_combobox.get()
        if not selected_top_wine:
            print("Debug: No top wine selected.")
            return
        file_path = 'CsvReaderOutput.txt'
        orders = parse_orders(file_path)
        hourly_item_counter = count_item_frequency_by_hour(orders, selected_top_wine)
        plot_item_frequency_by_hour(hourly_item_counter, selected_top_wine)
    else:
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

# Tkinter UI Setup
root = tk.Tk()
root.title("Wine Sales Frequency")

# Get wine names and promotion dates
wine_names = get_wine_names('CsvReaderOutput.txt')
promotion_options = [f"{date} - {wine}" for date, wine in PROMOTIONS.items()]
top_wine_names = get_top_n_wines('CsvReaderOutput.txt', top_n=20)

# Create UI elements
wine_combobox = ttk.Combobox(root, values=wine_names, state="normal", width=40)
wine_combobox.pack(pady=10)

period_var = tk.StringVar(value="24-hour period")

period_24hr = ttk.Radiobutton(root, text="24-hour period", variable=period_var, value="24-hour period")
period_all_days = ttk.Radiobutton(root, text="All days period", variable=period_var, value="All days period")
period_specific_date = ttk.Radiobutton(root, text="Specific Date", variable=period_var, value="Specific Date")
period_promoted_items = ttk.Radiobutton(root, text="Promoted Items", variable=period_var, value="Promoted Items")
period_top_20_wines = ttk.Radiobutton(root, text="Top 20 Wines", variable=period_var, value="Top 20 Wines")
period_24hr.pack()
period_all_days.pack()
period_specific_date.pack()
period_promoted_items.pack()
period_top_20_wines.pack()

date_entry_label = tk.Label(root, text="Enter Date (MM/DD/YYYY):")
date_entry = ttk.Entry(root, width=20)
date_entry_label.pack_forget()
date_entry.pack_forget()

promotion_date_label = tk.Label(root, text="Select Promotion Date:")
promotion_date_combobox = ttk.Combobox(root, values=promotion_options, state="readonly", width=40)
promotion_date_label.pack_forget()
promotion_date_combobox.pack_forget()

top_wine_label = tk.Label(root, text="Select Top Wine:")
top_wine_combobox = ttk.Combobox(root, values=top_wine_names, state="readonly", width=40)
top_wine_label.pack_forget()
top_wine_combobox.pack_forget()

def toggle_date_entry():
    if period_var.get() == "Specific Date":
        date_entry_label.pack(pady=5)
        date_entry.pack(pady=5)
        promotion_date_label.pack_forget()
        promotion_date_combobox.pack_forget()
        top_wine_label.pack_forget()
        top_wine_combobox.pack_forget()
    elif period_var.get() == "Promoted Items":
        date_entry_label.pack_forget()
        date_entry.pack_forget()
        promotion_date_label.pack(pady=5)
        promotion_date_combobox.pack(pady=5)
        top_wine_label.pack_forget()
        top_wine_combobox.pack_forget()
    elif period_var.get() == "Top 20 Wines":
        date_entry_label.pack_forget()
        date_entry.pack_forget()
        promotion_date_label.pack_forget()
        promotion_date_combobox.pack_forget()
        top_wine_label.pack(pady=5)
        top_wine_combobox.pack(pady=5)
    else:
        date_entry_label.pack_forget()
        date_entry.pack_forget()
        promotion_date_label.pack_forget()
        promotion_date_combobox.pack_forget()
        top_wine_label.pack_forget()
        top_wine_combobox.pack_forget()

period_24hr.config(command=toggle_date_entry)
period_all_days.config(command=toggle_date_entry)
period_specific_date.config(command=toggle_date_entry)
period_promoted_items.config(command=toggle_date_entry)
period_top_20_wines.config(command=toggle_date_entry)

generate_button = ttk.Button(root, text="Generate Graph", command=generate_graph)
generate_button.pack(pady=10)

root.mainloop()