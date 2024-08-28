import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class SalesDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Dashboard")
        self.root.geometry("1200x800")

        # Load data
        self.df = self.load_sample_data()

        # Create main frames
        self.create_header()
        self.create_sidebar()
        self.create_main_content()

        # Initialize with default view
        self.show_revenue_by_region()

    def load_sample_data(self):
        # Generate sample data
        data = pd.read_csv("5000 Sales Records.csv")
        data[['Order ID',"Units Sold",'Unit Price','Unit Cost', 'Total Revenue', 'Total Cost', 'Total Profit']]=data[['Order ID','Units Sold','Unit Price','Unit Cost', 'Total Revenue', 'Total Cost', 'Total Profit']].astype(int)
        data['Order Date']=pd.to_datetime(data['Order Date'])
        data['Ship Date']=pd.to_datetime(data['Ship Date'])

        return data

    def create_header(self):
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X)
        ttk.Label(header, text="Sales Dashboard", font=("Helvetica", 24, "bold")).pack(pady=10)

    def create_sidebar(self):
        sidebar = ttk.Frame(self.root, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Button(sidebar, text="Revenue by Region", command=self.show_revenue_by_region).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar, text="Profit by Country", command=self.show_profit_by_country).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar, text="Sales by Item Type", command=self.show_sales_by_item_type).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar, text="Sales Over Time", command=self.show_sales_over_time).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar, text="Sales Channel Analysis", command=self.show_sales_channel_analysis).pack(pady=5, padx=10, fill=tk.X)

    def create_main_content(self):
        self.main_content = ttk.Frame(self.root)
        self.main_content.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    def update_plot(self, fig):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.main_content)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def show_revenue_by_region(self):
        revenue_by_region = self.df.groupby('Region')['Total Revenue'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        revenue_by_region.plot(kind='bar', ax=ax)
        ax.set_title('Revenue by Region')
        ax.set_ylabel('Total Revenue')
        plt.tight_layout()
        self.update_plot(fig)

    def show_profit_by_country(self):
        profit_by_country = self.df.groupby('Country')['Total Profit'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        profit_by_country.plot(kind='bar', ax=ax)
        ax.set_title('Profit by Country')
        ax.set_ylabel('Total Profit')
        plt.tight_layout()
        self.update_plot(fig)

    def show_sales_by_item_type(self):
        sales_by_item = self.df.groupby('Item Type')['Units Sold'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sales_by_item.plot(kind='bar', ax=ax)
        ax.set_title('Sales by Item Type')
        ax.set_ylabel('Units Sold')
        plt.tight_layout()
        self.update_plot(fig)

    def show_sales_over_time(self):
        sales_over_time = self.df.groupby('Order Date')['Total Revenue'].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        sales_over_time.plot(kind='line', ax=ax)
        ax.set_title('Sales Over Time')
        ax.set_ylabel('Total Revenue')
        ax.set_xlabel('Order Date')
        plt.tight_layout()
        self.update_plot(fig)

    def show_sales_channel_analysis(self):
        channel_sales = self.df.groupby('Sales Channel')['Total Revenue'].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        channel_sales.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('Sales Channel Analysis')
        plt.tight_layout()
        self.update_plot(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesDashboard(root)
    root.mainloop()