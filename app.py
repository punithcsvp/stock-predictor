import os
import random
import base64
import io
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        stock_symbol = request.form['stock_symbol'].upper()

        current_price = round(100 + random.uniform(50, 200), 2)

        np.random.seed(sum(ord(c) for c in stock_symbol))
        historical_prices = list(np.round(current_price + np.cumsum(np.random.uniform(-5, 5, 10)), 2))

        predicted_prices = list(np.round(current_price + np.cumsum(np.random.uniform(-2, 3, 5)), 2))

        days = [f"Day {i+1}" for i in range(30)]
        daily_prices = [round(current_price + random.uniform(-10, 10), 2) for _ in range(30)]

        daily_plot_url = generate_plot(daily_prices, days, 'Daily Stock Price Variation', 'Days', 'Price (₹)', 'purple')

        historical_plot_url = generate_plot(historical_prices, list(range(1, 11)), 'Historical Stock Prices', 'Hours Ago', 'Price (₹)', 'blue')

        predicted_plot_url = generate_plot(predicted_prices, list(range(1, 6)), 'Predicted Stock Prices', 'Hours From Now', 'Price (₹)', 'green')

        hourly_prices = [{'hour': f'{i+1}h', 'price': round(price, 2)} for i, price in enumerate(predicted_prices)]

        price_change_percentage = round(((predicted_prices[-1] - current_price) / current_price) * 100, 2)
        decision = "Buy" if (predicted_prices[-1] - current_price) > 0 else "Sell"

        return jsonify({
            'stock_symbol': stock_symbol,
            'current_price': current_price,
            'predicted_prices': [{'hour': i + 1, 'price': price} for i, price in enumerate(predicted_prices)],
            'historical_prices': [{'hour': -i, 'price': price} for i, price in enumerate(historical_prices[::-1])],
            'final_prediction': predicted_prices[-1],
            'price_change_percentage': price_change_percentage,
            'decision': decision,
            'historical_plot_url': historical_plot_url,
            'predicted_plot_url': predicted_plot_url,
            'daily_plot_url': daily_plot_url,
            'hourly_prices': hourly_prices
        })

    except Exception as e:
        return jsonify({'error': str(e)})

def generate_plot(data, labels, title, xlabel, ylabel, color):
    plt.figure(figsize=(10, 5))
    plt.plot(labels, data, marker='o', label=title, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.xticks(rotation=45)
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()
    return plot_url

if __name__ == '__main__':
    app.run(debug=True)
