import streamlit as st
import pandas as pd
import boto3

boto3.setup_default_session(profile_name='manpa_barman_fellow_dssgx_24')

bucket = "dssgx-munich-2024-bavarian-forest"

def get_the_df_from_csv():
    """
    Get the dataframe from the csv file.
    """
    # Load the data
    df = pd.read_csv("outputs/dummy.csv")
    return df

def get_files_from_aws(selected_category):
  
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)


    # get the preprocessed folder
    folder = f"preprocessed_data/bf_preprocessed_files/{selected_category}/"

    
    

    for object_summary in my_bucket.objects.filter(Prefix=f"preprocessed_data/bf_preprocessed_files/{selected_category}/"):
        # list only the files in the folder
        if object_summary.key.endswith('.parquet'):
            # st.write(object_summary.key)
            # list all the files in a list
            selected_file = object_summary.key
            # convert the selected file to a dataframe
            retrieved_df  = pd.read_parquet(selected_file, engine='pyarrow')
            # get the dates out from the file name
            dates = selected_file.split("/")[-1].split("_")[1:3]
            # get the start and end date
            start_date = dates[0]
            end_date = dates[1]
            status = f"{selected_category} data from {start_date} to {end_date} retrieved successfully"
        # if the data folder is empty return as no data found
        else:
            # return an empty dataframe
            retrieved_df = pd.DataFrame()
            status = "No data found from the selected category"

        return retrieved_df, status

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

    retrieved_df, status = get_files_from_aws(selected_category)
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

