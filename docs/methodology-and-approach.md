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

### Modeling
#### Explanation of the Feature Engineering Process
- Feature selection:
    - Important features used in the model
    - Methods for feature engineering
    - Handling temporal features
- Creation of input sequences for modeling:
    - Techniques used for different models

#### ExtraTree Regressor vs LSTM
- Comparison of models:
    - Model architectures and configurations
    - Performance evaluation on test data
    - Strengths and weaknesses of each approach
    - Decision rationale for choosing LSTM or ExtraTree Regressor
