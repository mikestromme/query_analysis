import pandas as pd
import matplotlib.pyplot as plt
import pyodbc

def byTime():
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

    # Convert 'RunDate' to datetime and extract time
    data['RunDate'] = pd.to_datetime(data['RunDate'])
    data['Time'] = data['RunDate'].dt.time

    data['Hour'] = data['RunDate'].dt.hour

    # Group by Hour and calculate average elapsed time
    hour_grouped = data.groupby('Hour')['ElapsedTime'].mean()

    # Group by Time and calculate average elapsed time
    #time_grouped = data.groupby('Time')['ElapsedTime'].mean()

    # Plotting
    plt.figure(figsize=(12, 6))
    hour_grouped.plot(kind='bar')
    plt.title('Average Elapsed Time by Time of Day')
    plt.xlabel('Time of Day')
    plt.ylabel('Average Elapsed Time (ms)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
