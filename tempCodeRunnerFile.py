import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1200x800")

        # Load data
        self.data = self.load_data()

        # Create main frames
        self.create_header()
        self.create_sidebar()
        self.create_main_content()

        # Initialize with default view
        self.show_revenue_by_region()

    def load_data(self):
        try:
            # Load data from CSV
            df = pd.read_csv("5000 Sales Records.csv")
            df[['Order ID', 'Units Sold', 'Unit Price', 'Unit Cost', 'Total Revenue', 'Total Cost', 'Total Profit']] = df[['Order ID', 'Units Sold', 'Unit Price', 'Unit Cost', 'Total Revenue', 'Total Cost', 'Total Profit']].astype(int)
            df['Order Date'] = pd.to_datetime(df['Order Date'])
            df['Ship Date'] = pd.to_datetime(df['Ship Date'])

            return df
        except FileNotFoundError:
            print("Error: The file '5000_Sales_Records.csv' was not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def create_header(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Dashboard", font=("Helvetica", 24, "bold")).pack(pady=10)

    def create_sidebar(self):
        sidebar_frame = ttk.Frame(self.root, width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Button(sidebar_frame, text="Revenue by Region", command=self.show_revenue_by_region).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar_frame, text="Profit by Country", command=self.show_profit_by_country).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar_frame, text="Sales by Item", command=self.show_sales_by_item).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar_frame, text="Sales Over Time", command=self.show_sales_over_time).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar_frame, text="Sales by Channel", command=self.show_sales_by_channel).pack(pady=5, padx=10, fill=tk.X)

    def create_main_content(self):
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    def update_chart(self, fig):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def show_revenue_by_region(self):
        data_grouped = self.data.groupby('Region')['Total Revenue'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='bar', ax=ax)
        ax.set_title('Revenue by Region')
        ax.set_ylabel('Total Revenue')
        plt.tight_layout()
        self.update_chart(fig)

    def show_profit_by_country(self):
        # todo: 
        data_grouped = self.data.groupby('Country')['Total Profit'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='bar', ax=ax)
        ax.set_title('Profit by Country')
        ax.set_ylabel('Total Profit')
        plt.tight_layout()
        self.update_chart(fig)

    def show_sales_by_item(self):
        data_grouped = self.data.groupby('Item Type')['Units Sold'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='bar', ax=ax)
        ax.set_title('Sales by Item')
        ax.set_ylabel('Units Sold')
        plt.tight_layout()
        self.update_chart(fig)

    def show_sales_over_time(self):
        data_grouped = self.data.groupby('Order Date')['Total Revenue'].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='line', ax=ax)
        ax.set_title('Sales Over Time')
        ax.set_ylabel('Total Revenue')
        ax.set_xlabel('Order Date')
        plt.tight_layout()
        self.update_chart(fig)

    def show_sales_by_channel(self):
        data_grouped = self.data.groupby('Sales Channel')['Total Revenue'].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('Sales by Channel')
        plt.tight_layout()
        self.update_chart(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()
