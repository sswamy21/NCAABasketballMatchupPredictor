# Regular Season Prediction (Wide & Deep)

This folder contains a notebook that predicts regular-season college basketball game outcomes using a wide & deep neural network with running statistics to avoid data leakage.

## Notebook

- Regular_Season_Prediction_Enhanced.ipynb

## What it does

- Builds running, game-by-game team statistics (no future data leakage).
- Engineers matchup features (differentials, tempo, Elo, form, consistency).
- Trains a wide & deep neural network to predict margin of victory.
- Benchmarks against LightGBM and XGBoost baselines.
- Generates a matchup HTML report with predictions and historical spread context.

## Data sources

- Kaggle competition data: "march-machine-learning-mania-2026"
- sportsdataverse (mbb) for recent matchup imports
- Local historical spread data: historical_spread_data.csv

## Outputs

- regular_season_model_enhanced.pth (model checkpoint and scalers)
- matchup_report.html (matchup comparison report)
- Alltime_Matchups_Converted.csv (converted matchup data)
- Alltime_Matchups_Team_Box_Score.csv (team box scores)

## Quick start

1. Open the notebook and run cells in order.
2. Update the matchup list in the "Make Predictions" section.
3. Run the HTML report cell to generate matchup_report.html.

## Notes

- The historical spread lookup uses the closest spread magnitude from historical_spread_data.csv.
- Win probabilities are derived from the predicted margin using a normal CDF with sigma 11.0.
