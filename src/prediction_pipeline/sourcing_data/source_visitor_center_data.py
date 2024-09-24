import awswrangler as wr
import pandas as pd


def source_visitor_center_data():
    # Source data - this is the preprocessed data
    visitorcenter_data =  wr.s3.read_csv(path="s3://dssgx-munich-2024-bavarian-forest/preprocessed_data/bf_visitcenters_hourly .csv")

    return visitorcenter_data