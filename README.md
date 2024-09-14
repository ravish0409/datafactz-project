# Sales Data Dashboard

The **Sales Data Dashboard** is a Python-based project developed during the DataFactZ workshop. The goal of the project is to create an interactive dashboard that helps users visualize and analyze sales data. The dashboard offers various features like data filtering, sorting, and graphical visualizations.

![image](https://github.com/user-attachments/assets/23c15d38-9573-4725-803d-3b44ce6a09b4)

### Key Technologies:
- **Tkinter**: Used for building the graphical user interface (GUI).
- **Pandas**: For data manipulation and analysis.
- **Matplotlib**: To create visualizations such as charts and graphs.

### Code Structure


 
- **Dashboard Class:** Manages all the functions of the dashboard.
- **__init__ Method:** Sets up the layout, loads the data, and displays the default view.
- **load_data Method:** Reads the CSV file and clean the data for use.
- **create_header and create_sidebar Methods:** Set up the header and sidebar where users can control the dashboard.
- **create_main_content Method:** Displays the main area for data visualizations.
- **Visualization Methods:** Show different graphs, like revenue by region.
  
![image](https://github.com/user-attachments/assets/8f3d8662-141d-444f-934d-b6beadc89717)

---

## Setup Process

### 1. Clone the Repository:
First, clone the repository from GitHub to your local machine:
```bash
git clone https://github.com/ravish0409/datafactz-project.git
cd datafactz-project
```
### 2. Set Up a Virtual Environment (Optional but Recommended):
Setting up a virtual environment helps manage dependencies and avoid conflicts with other projects.
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Install Dependencies:
Once the environment is active, install the required dependencies listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```
### 4. Run the Project:
After installing the dependencies, you can launch the dashboard by running the sales_analyze.py script:
```bash
python sales_analyze.py
```
### Future Enhancements
- Add more data filters, such as filtering by product type or date.
- Provide the option to export graphs and reports in formats like PDF or Excel.
- Optimize performance for larger datasets through lazy loading or data chunking.
