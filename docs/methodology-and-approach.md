# III. Methodology and Approach

## Repository Overview
- Explanation of the code structure:
    - Overview of folders and files
    - Key scripts and their purposes
    - Description of helper modules

## Description of the Data Sources Used & Methods for Data Sourcing
- List of data sources:
    - **Sensor Data for Visitor Counts**:
        - Detailed visitor counts from various sensors across the park
    - **Weather Data**:
        - Historical weather data relevant to visitor trends
    - **Visitor Center Data**:
        - Visitor statistics from various centers within the park
    - **Parking Data**:
        - Parking usage data to estimate visitor inflow/outflow
- Methods for data sourcing:
    - Data retrieval process
    - Handling different data formats
    - Storage and accessibility

## Streamlit App
### Description of the Data Preprocessing and Cleaning Steps
- Visitor count data:
    - Loading and parsing data
    - Cleaning and handling missing data
    - Sensor replacements and mapping
    - Outlier detection and handling
    - Traffic metrics calculation
- Sensor data preprocessing:
    - Timestamp adjustments
    - Merging and combining sensor data
    - Handling overlapping periods
- Weather data preprocessing:
    - Imputing missing weather values
    - Mapping weather categories
    - Integration with visitor data
- Visitor center and parking data preprocessing:
    - Parsing and cleaning visitor center data
    - Handling missing values in parking data
    - Merging with sensor and weather data

### Data Query/Accessibility/Upload Section
- Explanation of data accessibility:
    - Querying data from AWS S3
    - Handling data uploads and user inputs
    - Data filtering and visualization in the Streamlit app
- Features and Techniques:
    - Data filtering options
    - Visualization techniques used
    - User interface elements

## Prediction Pipeline
### Description of the Data Preprocessing and Cleaning Steps

In our project, we utilized various data sources, including sensor data for visitor counts, weather data, visitor center data, and parking data. These datasets were initially in different formats, necessitating a thorough cleaning and preprocessing process to unify them.

#### Visitor Count Data Preprocessing
For the visitor count data, several crucial steps were taken:

- **Removing Unwanted Data**: We excluded any data prior to "2016-05-10 03:00:00" since no sensors were installed before this date, ensuring our analysis focused on relevant data.

- **Fixing Column Names**: The original dataset contained inconsistently named columns due to sensor replacements and renaming. We implemented a mapping process to unify sensor names, allowing us to aggregate readings under single names. For example, 'Bucina PYRO IN' and 'Bucina_Multi IN' were combined into 'Bucina MERGED IN'.

- **Correcting and Imputing Timestamps**: We adjusted timestamps to account for daylight saving time changes, ensuring the integrity of our time series data. Missing values were filled in from subsequent rows to maintain continuity.

- **Handling Non-Replaced Sensors**: Columns representing non-replaced sensors were set to NaN for values recorded before their replacement dates, as they no longer provided valid data.

- **Correcting Overlapping Sensor Data**: In cases where both old and new sensors reported data during overlapping periods, we set values to NaN for old sensors after their replacement dates to avoid skewing our analysis.

- **Merging Columns**: We merged columns based on predefined mappings to create simplified combined columns, such as 'Bucina MERGED IN'. This step eliminated redundancy and ensured a focus on relevant data.

- **Outlier Handling**: Any visitor count exceeding 800 was transformed to NaN, as these values were deemed outliers and not representative of typical sensor readings.

- **Calculating Traffic Metrics**: We derived key traffic metrics, including:
    - `traffic_abs`: Total counts (in + out) from all sensors.
    - `sum_IN_abs` and `sum_OUT_abs`: Sums of incoming and outgoing counts.
    - `occupancy_abs`: A cumulative measure representing occupancy over time, aiding in trend analysis.

#### Weather Data Preprocessing


The weather data was sourced and preprocessed to ensure consistency and reliability for our analysis. The following key steps were taken:

- **Data Sourcing**: 
     - We retrieved hourly weather data from the Meteostat API for the Bavarian Forest region from January 1, 2016, to September 3, 2024. This involved setting geographical coordinates to target the specific area.

- **Cleaning and Formatting**: 

    - Unnecessary columns such as dew point, snow, wind direction, and others were removed to simplify the dataset.
    - The remaining columns were renamed for clarity, transforming them into more descriptive titles like 'Temperature (°C)', 'Precipitation (mm)', and 'Relative Humidity (%)'.
    - The 'Time' column was converted into a proper datetime format for seamless time series analysis.

- **Imputation of Missing Values**: 
    - We implemented a function to fill missing values using linear interpolation, ensuring that gaps in the data were appropriately addressed. If a significant percentage of zero values (over 60%) was detected in any parameter, we opted to fill missing entries with zero.
    - This approach helped maintain the integrity of the dataset while providing a more accurate representation of weather conditions.

- **Data Storage**: 
     - The processed weather data was saved to an AWS S3 bucket, facilitating easy access and retrieval for subsequent analyses.

By carefully processing the weather data, we ensured it was well-prepared for integration with visitor count data and other datasets in our predictive modeling pipeline.


#### Visitor Center Data Preprocessing

*(Placeholder: Add details about the cleaning and preprocessing steps for visitor center data here.)*

#### Parking Data Preprocessing

*(Placeholder: Add details about the cleaning and preprocessing steps for parking data here.)*

### Data Integration

We joined the preprocessed datasets—visitor counts, weather, and visitor center data—based on their timestamps to create a unified dataset for efficient modeling. This integration ensures that all data points align in hourly format, facilitating a comprehensive analysis of visitor traffic patterns.

The resulting joined dataset encompasses all relevant features from each source, providing a robust foundation for our predictive modeling efforts. This approach allows us to leverage the combined insights from different datasets, enhancing the accuracy and effectiveness of our forecasts.

### Data Preprocessing and Feature Engineering

After joining the data, we conducted various tasks, including feature selection and feature engineering. Below are the relevant aspects of this process:

#### Region-wise Mapping

The Bavarian Forest National Park is divided into six regions, and we grouped the sensors accordingly. For each region, we aggregated the IN and OUT values based on the specific sensors that belong to that region:

> **Falkenstein-Schwellhäusl**  
> Sensors: Bayerisch Eisenstein, Brechhäuslau, Deffernik, Ferdinandsthal, Schillerstraße  
>
> **Nationalparkzentrum Falkenstein**  
> Sensors: Falkenstein 1, Falkenstein 2  
>
> **Scheuereck-Schachten-Trinkwassertalsperre**  
> Sensors: Gsenget, Scheuereck, Trinkwassertalsperre  
>
> **Lusen-Mauth-Finsterau**  
> Sensors: Bucina, Felswandergebiet, Fredenbrücke, Schwarzbachbrücke, Waldhausreibe, Wistlberg, Sagwassersäge  
>
> **Rachel-Spiegelau**  
> Sensors: Diensthüttenstraße, Gfäll, Klingenbrunner Wald, Klosterfilz, Racheldiensthütte, Waldspielgelände  
>
> **Nationalparkzentrum Lusen**  
> Sensors: Lusen 1, Lusen 2, Lusen 3  


The readings from these sensors were combined to provide the total IN and OUT values for the region.


#### Feature Engineering

We integrated additional features, including:

- Z-scores for daily maximum temperature, relative humidity, and wind speed.
- Distance to the nearest holidays for both Bayern and Czech Republic.

#### Data Preprocessing

#### Handling Numerical, Cyclic, and Categorical Features

1. **Cyclic Features**: We transformed cyclical features (e.g., hour, day) using sine and cosine transformations to maintain the cyclic nature.

2. **Numerical Features**: Z-score normalization was applied to standardize numerical features, ensuring they have a mean of 0 and a standard deviation of 1.

3. **Categorical Features**: Categorical columns were converted to string types for proper processing and analysis.

#### Additional Steps

- **Datetime Conversion**: The 'Time' column was converted to a datetime format for easier time-based indexing and analysis.
- **Summation of IN and OUT Values**: We summed the IN and OUT values for each region based on the defined mappings.
- **Data Type Changes**: Data types were adjusted according to predefined specifications to ensure consistency and optimize performance.

This systematic approach to preprocessing and feature engineering sets a solid foundation for subsequent modeling and analysis.

### Modeling
We have sliced the data from January 1, 2023, to July 22, 2024, for training purposes. During our experimentation phase, we explored various forecasting models to identify the most effective approach for predicting visitor traffic in the Bavarian Forest National Park. Ultimately, the ExtraTree Regressor and LSTM (Long Short-Term Memory) models demonstrated superior performance compared to other models.

### ExtraTree Regressor

The ExtraTree Regressor (Extremely Randomized Trees) is a powerful ensemble learning algorithm that constructs multiple decision trees during training. Unlike traditional decision trees, where splits are chosen based on the best criteria, Extra Trees randomly select cut points in the features. This approach often reduces variance without significantly increasing bias, making Extra Trees particularly well-suited for datasets with complex patterns and large feature spaces.

#### Why ExtraTree Regressor is Ideal for Our Use Case

- **Robustness to Overfitting**: Due to the random nature of tree splits, ExtraTree Regressor is less likely to overfit the training data, especially in cases where the data has high dimensionality or contains noise.

- **Efficiency**: ExtraTree Regressor requires less computational effort compared to other ensemble methods like Random Forests, making it an efficient choice for large-scale data.

- **Interpretability**: While still complex, the decision-tree-based structure of the ExtraTree Regressor provides a level of interpretability, allowing us to understand which features contribute most significantly to the model’s predictions.

- **Handling of Various Feature Types**: The model can handle both numerical and categorical features, which is crucial for our dataset, containing a mix of these feature types.

#### Model Implementation

**Data Preparation**: The data is split into training (January 1, 2023, to April 30, 2024) and testing (May 1, 2024, to July 22, 2024) sets based on specific date ranges, ensuring the temporal structure of the data is preserved.

**Model Setup**: PyCaret is used for setting up the model, where we define numeric and categorical features, ensure no data shuffling, and use 90% of the data for training with a 5-fold cross-validation.

**Model Training**: The Extra Trees Regressor is trained on the defined training set, and predictions are made on the test set to evaluate performance.

**Model Saving**: The trained models are saved for each target variable, ensuring reproducibility and facilitating later use in inference tasks.

This approach allowed us to capture the complexities in the data and produce reliable forecasts for visitor traffic in the Bavarian Forest National Park.


### LSTM (Long Short-Term Memory)

Long Short-Term Memory (LSTM) networks are a type of recurrent neural network (RNN) specifically designed to model sequential data and capture long-term dependencies. LSTMs are highly effective for time series forecasting due to their ability to retain information over extended periods, which is crucial for predicting visitor traffic based on past patterns.



#### ExtraTree Regressor vs LSTM
- Comparison of models:
    - Model architectures and configurations
    - Performance evaluation on test data
    - Strengths and weaknesses of each approach
    - Decision rationale for choosing LSTM or ExtraTree Regressor
