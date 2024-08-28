# import libraries
import pandas as pd
import os
import source_data as sd

def process_parking_data(all_parking_data):

    # Fill missing values in the parking data

    # if there are null values in the capacity column, fill them with the with 40 (it is the lowest capacity value from all the sensors)
    all_parking_data['current_capacity'].fillna(40, inplace=True)

    # if there are null values in the occupancy column, fill them with the corresponding capacity value
    all_parking_data['current_occupancy'].fillna(all_parking_data['current_capacity'], inplace=True)

    # if there are null values in the occupancy rate column, fill them with the occupancy divided by the capacity   
    all_parking_data['current_occupancy_rate'].fillna(all_parking_data['current_occupancy']/all_parking_data['current_capacity'], inplace=True)


    # Convert to data type int

    all_parking_data['current_capacity'] = all_parking_data['current_capacity'].astype(int)
    all_parking_data['current_occupancy'] = all_parking_data['current_occupancy'].astype(int)

    return all_parking_data

def main():
    _, all_parking_data,_ = sd.source_all_data()

    all_parking_data = process_parking_data(all_parking_data)

    return all_parking_data

if __name__ == '__main__':
    main()