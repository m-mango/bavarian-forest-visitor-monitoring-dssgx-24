# Findings and Results


The analysis of visitor traffic in the Bavarian Forest National Park utilized the Extra Trees Regressor, focusing on predictions across six distinct regions. We examined 15 target variables, including total visitor counts and IN/OUT values for each region, as well as overall metrics for the park.

### Model Fit Indices

The performance of the Extra Trees Regressor was evaluated using 5-fold cross-validation for both training and test data. The average results across all folds for the target variables are summarized in the table below:

| Target/Model                                                   | MAE      | MSE       | RMSE     | R²      | RMSLE   | MAPE    |
|---------------------------------------------------------------|----------|-----------|----------|---------|---------|---------|
| Traffic (IN + OUT for entire Park)                            | 46.1162  | 8917.1099 | 92.2189  | 0.8081  | 0.8319  | 1.0861  |
| IN (entire park)                                             | 24.3335  | 2442.0343 | 48.2164  | 0.7974  | 0.7300  | 1.0028  |
| OUT (entire park)                                            | 24.1747  | 2458.5690 | 48.4344  | 0.7931  | 0.8057  | 1.0266  |
| Lusen-Mauth-Finsterau (IN)                                   | 6.7317   | 201.3070  | 14.0569  | 0.5393  | 0.8434  | 1.4217  |
| Lusen-Mauth-Finsterau (OUT)                                  | 8.0701   | 257.9571  | 15.9973  | 0.5997  | 0.9015  | 1.6323  |
| Nationalparkzentrum Lusen (IN)                               | 7.9054   | 287.9660  | 16.6835  | 0.6963  | 0.6837  | 1.1265  |
| Nationalparkzentrum Lusen (OUT)                              | 7.5386   | 260.5668  | 15.9148  | 0.7029  | 0.7600  | 1.1740  |
| Rachel-Spiegelau (IN)                                        | 5.9471   | 147.6946  | 11.5325  | 0.6194  | 0.6604  | 1.0976  |
| Rachel-Spiegelau (OUT)                                       | 5.1613   | 114.6056  | 10.1086  | 0.6211  | 0.6459  | 1.1172  |
| Falkenstein-Schwellhäusl (IN)                                | 6.3214   | 175.2889  | 12.7272  | 0.7207  | 0.6538  | 1.0518  |
| Falkenstein-Schwellhäusl (OUT)                               | 5.9329   | 159.9409  | 12.2524  | 0.7392  | 0.6455  | 1.0008  |
| Scheuereck-Schachten-Trinkwassertalsperre (IN)              | 2.4397   | 57.1253   | 6.9169   | 0.1636  | 0.6783  | 1.0380  |
| Scheuereck-Schachten-Trinkwassertalsperre (OUT)             | 2.1488   | 21.6679   | 4.2865   | 0.3744  | 0.6556  | 1.0186  |
| Nationalparkzentrum Falkenstein (IN)                         | 5.0964   | 116.4658  | 10.7654  | 0.6457  | 0.6387  | 1.0955  |
| Nationalparkzentrum Falkenstein (OUT)                        | 4.7758   | 106.0070  | 10.2023  | 0.6063  | 0.6482  | 1.2331  |

### Key Insights

1. **Overall Visitor Traffic**:

    - The model predicted an average total traffic count (IN + OUT) of **46.12** with a **R² value of 0.8081**, indicating a strong relationship between predicted and actual values. This suggests that the model successfully captures the dynamics of visitor traffic across the entire park.

2. **Regional Performance**:
    - **Lusen-Mauth-Finsterau** showed relatively lower prediction errors, with MAE values of **6.73** (IN) and **8.07** (OUT). These figures suggest a stable visitor count in this region, potentially influenced by its accessibility and visitor amenities.
    - **Nationalparkzentrum Lusen** also performed well, with MAE values of **7.91** (IN) and **7.54** (OUT), indicating a robust model fit for this popular tourist area.
    - In contrast, the **Scheuereck-Schachten-Trinkwassertalsperre** region exhibited the lowest prediction accuracy, with MAE values of **2.44** (IN) and **2.15** (OUT). The low R² value of **0.1636** for IN indicates that this region's visitor traffic may be influenced by more unpredictable factors, warranting further investigation.

3. **Traffic Trends**:
    - The overall IN and OUT values for the park were relatively balanced, with minor variations indicating consistent visitor patterns throughout the year. For example, the predicted IN count of **24.33** for the entire park suggests that visitors are more inclined to enter the park compared to exiting, reflecting a positive visitor experience and prolonged stays.

4. **Regional Disparities**:
    - Some regions, such as **Rachel-Spiegelau** and **Falkenstein-Schwellhäusl**, demonstrated relatively close MAE values (around **5-7** for both IN and OUT),       suggesting similar patterns of visitor behavior. The consistent metrics across these regions may indicate comparable attractions or services that draw visitors in and keep them within these areas.

### Conclusion

The findings illustrate the Extra Trees Regressor's effectiveness in predicting visitor traffic across various regions of the Bavarian Forest National Park. The results indicate strong predictive power, especially for areas with consistent visitor patterns. These insights can aid park management in resource allocation, event planning, and enhancing visitor experience based on anticipated traffic flows.
