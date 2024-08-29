import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1200x800")

        # Load data
        self.data = self.load_data()

        # Variable to track if sorting is enabled
        self.sort_enabled = tk.BooleanVar(value=False)

        # Create main frames
        self.create_header()
        self.create_sidebar()
        self.create_main_content()

        # Initialize with default view
        self.show_revenue_by_region()

    def load_data(self):
        try:
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

        # Buttons for various charts
        ttk.Button(sidebar_frame, text="Revenue by Region", command=self.show_revenue_by_region).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar_frame, text="Profit by Country", command=self.show_profit_by_country).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar_frame, text="Sales by Item", command=self.show_sales_by_item).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar_frame, text="Sales Over Time", command=self.show_sales_over_time).pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(sidebar_frame, text="Sales by Channel", command=self.show_sales_by_channel).pack(pady=5, padx=10, fill=tk.X)

        # Checkbox to toggle sorting
        ttk.Checkbutton(sidebar_frame, text="Sort all", command=self.show_revenue_by_region, variable=self.sort_enabled).pack(pady=5, padx=10)

    def create_main_content(self):
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Create a Text widget for the summary report
        self.summary_text = tk.Text(self.content_frame, height=10, wrap=tk.WORD)
        self.summary_text.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    def update_chart(self, fig, summary):
        plt.close(fig)
        # Clear existing widgets in the content_frame (except the text box)
        for widget in self.content_frame.winfo_children():
            if not isinstance(widget, tk.Text):
                widget.destroy()

        # Update the chart
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Update the summary report
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    def annotate_bars(self, ax,dol='$'):
        for bar in ax.patches:
            ax.annotate(f'{dol}{bar.get_height()/1_000_000:.1f}M', 
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                        xytext=(0, -12), 
                        textcoords="offset points", 
                        ha='center', 
                        va='bottom')
        plt.tight_layout()

    def show_revenue_by_region(self):
        data_grouped = self.data.groupby('Region')['Total Revenue'].sum()
        if self.sort_enabled.get():
            data_grouped = data_grouped.sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        plt.close(fig)
        bars = data_grouped.plot(kind='bar', ax=ax)

        # Set title and labels
        ax.set_title('Revenue by Region')
        ax.set_ylabel('Total Revenue')

        # Format the y-axis to display revenue in $100.0M
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1e6:.0f}M'))

        # Annotate bars
        self.annotate_bars(ax)

        summary = "Revenue by Region:\n" + data_grouped.apply(lambda x: f'${x/1_000_000:.1f}M').to_string()
        self.update_chart(fig, summary)

    def show_profit_by_country(self):
        data_grouped = self.data.groupby('Country')['Total Profit'].sum()
        if self.sort_enabled.get():
            data_grouped = data_grouped.sort_values(ascending=False)

        half_count = len(data_grouped) // 2
        data_grouped = data_grouped.head(half_count)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = data_grouped.plot(kind='bar', ax=ax)

        # Set title and labels
        ax.set_title('Profit by Country')
        ax.set_ylabel('Total Profit')

        # Format the y-axis to display profit in $100.0M
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1e6:.0f}M'))

        # Annotate bars
        self.annotate_bars(ax)

        summary = "Top countries by profit:\n" + data_grouped.apply(lambda x: f'${x/1_000_000:.1f}M').to_string()
        self.update_chart(fig, summary)

    def show_sales_by_item(self):
        data_grouped = self.data.groupby('Item Type')['Units Sold'].sum()
        if self.sort_enabled.get():
            data_grouped = data_grouped.sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = data_grouped.plot(kind='bar', ax=ax)

        # Set title and labels
        ax.set_title('Sales by Item')
        ax.set_ylabel('Units Sold')

        # Annotate bars
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1e6:.0f}M'))
        self.annotate_bars(ax,"")
        summary = "Sales by Item Type:\n" + data_grouped.apply(lambda x: f'${x/1_000_000:.1f}M').to_string()
        self.update_chart(fig, summary)

    def show_sales_over_time(self):
        dfy = self.data.copy()
        dfy['year'] = dfy['Order Date'].dt.year
        data_grouped = dfy.groupby('year')['Total Revenue'].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        lines = data_grouped.plot(kind='line', ax=ax)

        # Set title and labels
        ax.set_title('Sales Over Time')
        ax.set_ylabel('Total Revenue')
        ax.set_xlabel('Year')

        # Format the y-axis to display revenue in $100.0M
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1e6:.1f}M'))

        plt.tight_layout()
        summary = "Sales Over Time:\n" + data_grouped.apply(lambda x: f'${x/1_000_000:.1f}M').to_string()
        self.update_chart(fig, summary)

    def show_sales_by_channel(self):
        data_grouped = self.data.groupby('Sales Channel')['Total Revenue'].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('Revenue by Channel')
        plt.tight_layout()

        summary = "Sales by Channel:\n" + data_grouped.apply(lambda x: f'${x/1_000_000_000:.1f}B').to_string()
        self.update_chart(fig, summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()
