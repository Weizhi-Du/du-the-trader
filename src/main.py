# src/main.py

import argparse
import sys

from data_preprocessing import load_and_preprocess_data
from model_training import train_model, save_model
from model_evaluation import evaluate_model, plot_results
from prediction import make_future_predictions, plot_future_predictions

def main(ticker, start_date, end_date, days_ahead):
    print(f"Loading and preprocessing data for {ticker} from {start_date} to {end_date}...")
    X_train, y_train, X_test, y_test, scaler, data = load_and_preprocess_data(ticker, start_date, end_date)

    print("Training the model...")
    model, history = train_model(X_train, y_train, X_test, y_test)

    print("Evaluating the model...")
    predictions, y_test_scaled = evaluate_model(model, X_test, y_test, scaler)

    print("Plotting the results...")
    plot_results(y_test_scaled, predictions, ticker)

    print("Saving the model...")
    save_model(model)

    print(f"Making future predictions for the next {days_ahead} days...")
    future_predictions = make_future_predictions(model, data['Close'].values, scaler, days_ahead=days_ahead)
    print("Predicted future stock prices:")
    for i, price in enumerate(future_predictions, 1):
        print(f"Day {i}: {price:.2f}")

    plot_future_predictions(future_predictions, data, ticker)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stock Price Prediction using LSTM')
    parser.add_argument('--ticker', type=str, required=True, help='Stock ticker symbol (e.g., AAPL)')
    parser.add_argument('--start_date', type=str, required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end_date', type=str, required=True, help='End date in YYYY-MM-DD format')
    parser.add_argument('--days_ahead', type=int, default=30, help='Number of days to predict into the future')

    args = parser.parse_args()

    try:
        main(args.ticker, args.start_date, args.end_date, args.days_ahead)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
