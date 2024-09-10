import streamlit as st
import pandas as pd
import boto3
import awswrangler as wr

# AWS Setup
bucket = "dssgx-munich-2024-bavarian-forest"

def get_the_df_from_csv():
    """
    Get the dataframe from the csv file.
    """
    # Load the data
    df = wr.s3.read_csv("s3://dssgx-munich-2024-bavarian-forest/preprocessed_data/weather_2020_01_01_to_2023_12_31_dummy.csv")
    return df

# def get_files_from_aws(selected_category):

#     s3 = boto3.resource('s3')
#     my_bucket = s3.Bucket(bucket)

#     retrieved_df = pd.DataFrame()
#     status = "No data found from the selected category"

#     for object_summary in my_bucket.objects.filter(Prefix=f"/preprocessed_data/bf_preprocessed_files/{selected_category}/"):
#         print(object_summary.key)
#         # list only the files in the folder
#         if object_summary.key.endswith('.parquet'):
#             # st.write(object_summary.key)
#             # list all the files in a list
#             print(object_summary.key)
#             selected_file = object_summary.key
#             print(selected_file)
#             # convert the selected file to a dataframe
#             retrieved_df  = pd.read_parquet(selected_file, engine='pyarrow')
#             print(retrieved_df)
#             # get the dates out from the file name
#             dates = selected_file.split("/")[-1].split("_")[1:3]
#             # get the start and end date
#             start_date = dates[0]
#             end_date = dates[1]
#             status = f"{selected_category} data from {start_date} to {end_date} retrieved successfully"
#             break
#         # if the data folder is empty return as no data found

#     return retrieved_df, status


def get_files_from_aws(selected_category):

    # Specify the S3 bucket and folder path
    prefix = "preprocessed_data/bf_preprocessed_files/{selected_category}"  # Make sure to include trailing slash
    # folder = f"s3://dssgx-munich-2024-bavarian-forest/preprocessed_data/bf_preprocessed_files/weather/{selected_category}"
    # List all objects in the specified S3 folder
    objects = wr.s3.list_objects(f"s3://{bucket}/{prefix}")

    # Check if there are any objects
    if not objects:
        print("No files found in the specified S3 folder.")
    else:
        # get the file 
        selected_file = objects[0]
        print(selected_file)

        # Load the file into a DataFrame
        df = wr.s3.read_parquet(f"s3://{bucket}/{selected_file}")
        # # Sort objects by the 'LastModified' attribute and get the latest file
        # latest_file = max(objects, key=lambda obj: obj['LastModified'])

        # print(f"Latest file: {latest_file['Key']}")

        # # Load the latest file into a DataFrame
        # df = wr.s3.read_parquet(f"s3://{bucket}/{latest_file['Key']}")

        return df



def get_data_for_type_1_query(retrieved_df):
    return

def get_data_for_type_2_query(retrieved_df):    
    return

def get_data_for_type_3_query(retrieved_df):
    return

def get_data_from_query(queries_dict, selected_query, selected_category):
    """
    Get the data from the query.
    """
    # get the file from aws preprocessed folder
    print(selected_category)
    retrieved_df = get_files_from_aws(selected_category)
    print(retrieved_df)

    # # find the key for the selected query in the queries_dict
    # for key, value in queries_dict.items():
    #     if value == selected_query:
    #         selected_key = key
    
    # if selected_key == "type1": 
    #     # get the data from the csv file
    #     get_data_for_type_1_query(retrieved_df)
    # elif selected_key == "type2":
    #     # get the data from the csv file
    #     get_data_for_type_2_query(retrieved_df)
    # elif selected_key == "type3":
    #     # get the data from the csv file
    #     get_data_for_type_3_query(retrieved_df)

    
    return 


def get_retrieved_df():
    """
    Get the retrieved dataframe.
    """
    # get the data from the query
    retrieved_df = get_the_df_from_csv()

    return retrieved_df

