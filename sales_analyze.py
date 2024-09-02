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
        self.root.geometry("1760x990")

        # Load data
        self.data = self.load_data()

        # Variable to track sorting order
        self.sort_var = tk.StringVar(value="none")

        # Variable to track active button
        self.active_button = None

        # Variable to track selected region
        self.region_var = tk.StringVar(value="Asia")

        # Create main frames
        self.create_header()
        self.create_sidebar()
        self.create_main_content()

        # Initialize with default view
        self.show_revenue_by_region()
    def load_data(self):
        try:
            df = pd.read_csv("5000 Sales Records.csv")

            df.dropna(inplace=True)
            df.drop_duplicates(inplace=True)
            
            df['Order Date'] = pd.to_datetime(df['Order Date'])
            df['Ship Date'] = pd.to_datetime(df['Ship Date'])
            
 
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            
            cols_to_numeric = ['Units Sold', 'Unit Price', 'Unit Cost', 'Total Revenue', 'Total Cost', 'Total Profit']
            # create a NaN value if any of these column contain other then numeric value
            df[cols_to_numeric] = df[cols_to_numeric].apply(pd.to_numeric, errors='coerce') 
            
            df.dropna(inplace=True)
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
        ttk.Label(header_frame, text="Sales Data Analysis with python", font=("Helvetica", 24, "bold")).pack(pady=10)

    def create_sidebar(self):
        sidebar_frame = ttk.Frame(self.root, width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Buttons for various charts
        self.buttons = {
            "Revenue by Region": ttk.Button(sidebar_frame, text="Revenue by Region", command=lambda: self.show_revenue_by_region()),
            "Profit by Country": ttk.Button(sidebar_frame, text="Profit by Country", command=lambda: self.show_profit_by_country()),
            "Sales by Item": ttk.Button(sidebar_frame, text="Sales by Item", command=lambda: self.show_sales_by_item()),
            "Revenue Over Time": ttk.Button(sidebar_frame, text="Revenue Over Time", command=lambda: self.show_sales_over_time()),
            "Sales by Channel": ttk.Button(sidebar_frame, text="Sales by Channel", command=lambda: self.show_sales_by_channel())
        }

        for button in self.buttons.values():
            button.pack(pady=5, padx=10, fill=tk.X)

        # Radio buttons for sorting
        sort_frame = ttk.LabelFrame(sidebar_frame, text="Sort Order")
        sort_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Radiobutton(sort_frame, text="None", variable=self.sort_var, value="none", command=self.update_current_view).pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Ascending", variable=self.sort_var, value="ascending", command=self.update_current_view).pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Descending", variable=self.sort_var, value="descending", command=self.update_current_view).pack(anchor=tk.W)

    def create_main_content(self):
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Create a frame for the region selector at the top
        self.selector_frame = ttk.Frame(self.content_frame)
        self.selector_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Create the region selector (hidden by default)
        self.region_label = ttk.Label(self.selector_frame, text="Select Region:")
        self.region_selector = ttk.Combobox(self.selector_frame, textvariable=self.region_var, state="readonly")
        self.region_selector.bind("<<ComboboxSelected>>", self.update_profit_by_country)

        # Create a frame for the chart
        self.chart_frame = ttk.Frame(self.content_frame)
        self.chart_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Create a Text widget for the summary report
        self.summary_text = tk.Text(self.content_frame, height=12, wrap=tk.WORD)
        self.summary_text.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    def update_chart(self, fig, summary):
        plt.close(fig)
        
        # Clear existing widgets in the chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Update the chart
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Update the summary report
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    def add_BM(self,height,till=0,dol='$') -> str:
        if height >= 1_000_000_000:
            label = f'{dol}{height // 1_000_000_000:.0f},{(height/10_000_000):.{till}f}M'
        elif height>=1_000_000:
            label = f'{dol}{height / 1_000_000:.{till}f}M'
        else:
            label= f'{dol}{height / 1_000_000:.1f}M' if height!=0 else f'{dol}{0}'
        return label

    def annotate_bars(self, ax,dol='$'):
        for bar in ax.patches:
            height = bar.get_height()
            label=self.add_BM(height,1,dol) # add $ and M and B
            ax.annotate(label, 
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                        xytext=(0, 0), 
                        textcoords="offset points", 
                        ha='center', 
                        va='bottom')
        plt.tight_layout()

    def apply_sorting(self, data, q='')-> pd.Series:
        if self.sort_var.get() == "ascending":
            return data.sort_values(ascending=True)
        elif self.sort_var.get() == "descending":
            return data.sort_values(ascending=False)
        return data
    def sort_with_col(self,data_col,col) -> pd.DataFrame:
        if self.sort_var.get() == "ascending":
            return data_col.sort_values(by=col,ascending=True)
        elif self.sort_var.get() == "descending":
            return data_col.sort_values(by=col,ascending=False)
        return data_col
    def highlight_active_button(self, active_button_text):
        # Reset all buttons to default style
        for button in self.buttons.values():
            button.configure(style='TButton')

        # Highlight the active button
        if active_button_text in self.buttons:
            self.buttons[active_button_text].configure(style='Accent.TButton')

        self.active_button = active_button_text

        # Show or hide the region selector based on the active button
        if active_button_text == "Profit by Country":
            self.selector_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        else:
            self.selector_frame.pack_forget()   
    def update_current_view(self):
        if self.active_button == "Revenue by Region":
            self.show_revenue_by_region()
        elif self.active_button == "Profit by Country":
            self.update_profit_by_country()
        elif self.active_button == "Sales by Item":
            self.show_sales_by_item()
        elif self.active_button == "Revenue Over Time":
            self.show_sales_over_time()
        elif self.active_button == "Sales by Channel":
            self.show_sales_by_channel()

    def create_table_str(self,table_name: str, series: pd.Series, col1_name: str, col2_name: str, col_width: int) -> str:
        # Table title with formatting
        table_title = f'{table_name}' 
        # Create the header row with custom column names
        header = f'| {col1_name:<{col_width}}|  {col2_name:<{col_width}}|'
        separator = '+'+'-' * (len(header)-2)+'+'
        rows = [table_title,separator , header, separator]

        for i, value in series.items():
            row = f'| {i:<{col_width}}|  {value:<{col_width}}|'
            rows.append(row)

        return '\n'.join(rows)+'\n'+ separator
    def create_df_str(self,table_name: str, dataframe: pd.DataFrame, col1_name: str, all_column_names: list[str], col_width: int) -> str:

        table_title = f'{table_name}'

        header = f'| {col1_name:<{col_width}}|  '  
        for col in all_column_names:
            header += f'{col:<{col_width}}|  '
        
   
        separator = '+'+'-' * (len(header)-4)+'+'
        
    
        rows = [table_title,separator, header, separator]
        
        # Loop through the DataFrame and format each index and row
        for i, row in dataframe.iterrows():
            row_str = f'| {i:<{col_width}}|  '  # Add index
            for col in all_column_names:
                row_str += f'{str(row[col]):<{col_width}}|  '  # Add each column value
            rows.append(row_str)
        
        # Join all rows into a single string with line breaks
        return '\n'.join(rows)+'\n'+separator
    def show_revenue_by_region(self):
        data_grouped = self.data.groupby('Region')['Total Revenue'].sum()
        data_grouped = self.apply_sorting(data_grouped)

        fig, ax = plt.subplots(figsize=(10, 6))

        data_grouped.plot(kind='bar', ax=ax)
        
        # Set title and labels
        ax.set_title('Revenue by Region')
        ax.set_ylabel('Total Revenue')
        plt.xticks(rotation=25, ha='right')
        # Format the y-axis to display revenue in $100.0M
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: self.add_BM(x) ))

        # Annotate bars
        self.annotate_bars(ax)
        plt.tight_layout()
        summary = self.create_table_str("Revenue by Region:",data_grouped.apply(lambda x: self.add_BM(x,2) ),'Region','Total Revenue',35)
        self.update_chart(fig, summary)
        self.highlight_active_button("Revenue by Region")

    def show_profit_by_country(self):
        # Get unique regions and update the region selector
        regions = sorted(self.data['Region'].unique())
        self.region_selector['values'] = regions
        
        # Show the region selector
        self.region_label.pack(side=tk.LEFT, padx=5)
        self.region_selector.pack(side=tk.LEFT, padx=5)

        self.update_profit_by_country()

        self.highlight_active_button("Profit by Country")
    def update_profit_by_country(self, event=None):
        selected_region = self.region_var.get()
        
        # Filter data for the selected region
        region_data = self.data[self.data['Region'] == selected_region]
        
        data_grouped = region_data.groupby('Country')['Total Profit'].sum()
        data_grouped = self.apply_sorting(data_grouped)

        half_count = len(data_grouped) // 2
        data_grouped = data_grouped.head(half_count)

        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='bar', ax=ax)

        # Set title and labels
        ax.set_title(f'Profit by Country in {selected_region}')
        ax.set_ylabel('Total Profit')

        # Format the y-axis to display profit in $100.0M
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: self.add_BM(x)))
        # Annotate bars
        self.annotate_bars(ax)

        plt.tight_layout()
        def var_name()-> pd.Series:
            if self.sort_var.get() == "ascending":
                return 'Bottom '
            elif self.sort_var.get() == "descending":
                return 'Top '
            return ""
            
        summary = self.create_table_str(f"{var_name()}countries by profit in {selected_region}:", data_grouped.apply(lambda x: self.add_BM(x,2)), 'Country', 'Total Profit', 25)
        self.update_chart(fig, summary)
    def show_sales_by_item(self):
        data_grouped = self.data.groupby('Item Type')['Units Sold'].sum()
        data_grouped = self.apply_sorting(data_grouped)

        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='bar', ax=ax)

        # Set title and labels
        ax.set_title('Sales by Item')
        ax.set_ylabel('Units Sold')
        plt.xticks(rotation=25, ha='right')
        # Annotate bars
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: self.add_BM(x,0,"") ))

        self.annotate_bars(ax,"")

        plt.tight_layout()
        mk=self.data.groupby('Item Type').agg({
            'Units Sold': 'sum',
            'Unit Price': 'mean',
            'Unit Cost': 'mean',
            'Total Profit': 'sum'
        })
  
        mk=self.sort_with_col(mk,'Total Profit')
        mk['Total Profit']=mk['Total Profit'].apply(lambda x: self.add_BM(x,2))
        mk['Unit Price']=mk['Unit Price'].apply(lambda x: f'${x:.0f}')
        mk['Unit Cost']=mk['Unit Cost'].apply(lambda x: f'${x:.0f}')
        mk['Units Sold']=mk['Units Sold'].apply(lambda x: self.add_BM(x,2,""))
        summary = "Sales by Item Type:\n" + mk.to_string()
        summary=self.create_df_str("Sales by Item Type:",mk,'Item Type',mk.columns,15)
        self.update_chart(fig, summary)
        self.highlight_active_button("Sales by Item")

    def show_sales_over_time(self):
        dfy = self.data.copy()
        dfy['year'] = dfy['Order Date'].dt.year
        data_grouped = dfy.groupby('year')['Total Revenue'].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='line', ax=ax)
        ax.plot(data_grouped.index, data_grouped.values, 'o', color='darkblue', markersize=8)
        # Set title and labels
        ax.set_title('Total Revenue Over Time')
        ax.set_ylabel('Total Revenue')
        ax.set_xlabel('Year')

        # Format the y-axis to display revenue in $100.0M
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: self.add_BM(x)))
        for year, revenue in data_grouped.items():
            ax.annotate(self.add_BM(revenue, 1), 
                        xy=(year, revenue), 
                        xytext=(0, 5),  # Offset the text slightly above the point
                        textcoords='offset points', 
                        ha='center', 
                        va='bottom')
        plt.tight_layout()
        data_grouped = self.apply_sorting(data_grouped)
        summary = self.create_table_str("Total Revenue Over Time:",data_grouped.apply(lambda x: self.add_BM(x,2) ),'year','Total Revenue',15)
        self.update_chart(fig, summary)
        self.highlight_active_button("Revenue Over Time")

    def show_sales_by_channel(self):
        data_grouped = self.data.groupby('Sales Channel')['Total Revenue'].sum()
        data_grouped = self.apply_sorting(data_grouped)

        fig, ax = plt.subplots(figsize=(10, 6))
        data_grouped.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('Revenue by Channel')
        plt.tight_layout()

        summary = self.create_table_str("Sales by Channel:",data_grouped.apply(lambda x: self.add_BM(x,2) ),'Sales Channel','Total Revenue',20)
        self.update_chart(fig, summary)
        self.highlight_active_button("Sales by Channel")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('Accent.TButton', background='green')
    app = Dashboard(root)
    root.mainloop()