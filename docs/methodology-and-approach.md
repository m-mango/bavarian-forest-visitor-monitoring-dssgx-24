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
- Detailed explanation of preprocessing:
    - Handling cyclic and categorical features
    - Scaling and normalization
    - Sequence creation for LSTM models
    - Fixed split for train/test/unseen data

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
