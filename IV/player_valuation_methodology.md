# Player Valuation Methodology

## Feature Selection

The feature selection process uses a data-driven approach:

1. First, all numeric features from the dataset are considered as potential predictors
2. LightGBM's built-in feature importance metric identifies the most influential variables
3. Top 10 features are selected based on importance scores
4. Key features include: Age, Passes into Final Third, Ball Recoveries, Touches in Attacking Penalty Area, Carries, Pass Completion %, Goals/90, and Take-Ons metrics

This approach reduces dimensionality while maintaining predictive power, as demonstrated by comparable performance between the full and reduced models.

## Model Selection

A LightGBM regression model was selected because:

1. It handles high-dimensional data efficiently
2. Provides built-in feature importance metrics
3. Performs well with numeric features
4. Captures non-linear relationships in the data

Model hyperparameters:
- Objective: Regression
- Estimators: 100
- Learning rate: 0.05
- Max depth: 7
- Leaves: 31

## Evaluation Results

The model demonstrates strong predictive performance:
- R² score of approximately 0.73-0.75 (explaining ~75% of variance in transfer fees)
- Comparable performance between full feature model and top-10 feature model
- Effective for valuing players across different ages and positions

The methodology successfully identifies market value patterns based on performance metrics, allowing for objective player valuations.
