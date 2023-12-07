import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pyodbc
from time_analysis import byTime

# Replace with the actual path of your data file
#file_path = 'querymetrics.csv'

# Load the dataset
#data = pd.read_csv(file_path)

def byDay():
    # Database connection parameters
    server = '10.1.1.7'  # e.g., 'localhost'
    database = 'xalt_prod'  # e.g., 'mydatabase'
    username = 'submstromme'  # e.g., 'user'
    password = 'Emmabean13!'  # e.g., 'password'

    # SQL query
    query = """
    SELECT *
    FROM QueryMetrics
    where RunDate > '2023-10-31'
    """

    try:
        # Establishing the connection
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                            ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

        # Running the query and loading into a DataFrame
        data = pd.read_sql(query, conn)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()

    # Convert 'RunDate' to datetime format
    data['RunDate'] = pd.to_datetime(data['RunDate'])

    # Convert 'RunDate' to datetime format and filter for 'Job Costing Labor View'
    data['RunDate'] = pd.to_datetime(data['RunDate'])
    labor_view_data = data[data['QueryName'] == 'Job Costing Labor View']

    # Creating the scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(labor_view_data['RunDate'], labor_view_data['ElapsedTime'], c=labor_view_data['AvgFragmentationInPercent'], cmap='viridis')
    plt.colorbar(label='Avg Percent of Fragmentation')

    # Setting the date format and interval to every four days
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))

    # Rotate date labels
    plt.xticks(rotation=45)

    plt.title('Elapsed Time vs Avg Percent of Fragmentation (Job Costing Labor View)')
    plt.xlabel('Run Date')
    plt.ylabel('Elapsed Time (ms)')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot
    #scatter_plot_path = 'scatter_plot_elapsed_time_vs_fragmentation_labor_view_four_days.png'
    #plt.savefig(scatter_plot_path)

    plt.show(block=False)


if __name__ == '__main__':

    byDay()
    byTime()
    plt.show()

