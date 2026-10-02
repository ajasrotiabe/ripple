# 🌊 Ripple

### AI-Powered Retail Decision Simulator

Ripple is an interactive retail inventory simulation
tool that helps users explore how demand, inventory,
and supplier lead times affect retail performance.

## Features

- 30-day inventory simulation
- Adjustable demand and inventory parameters
- Inventory and sales analytics
- Stockout monitoring
- Rule-based inventory recommendations

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy

## Run Locally

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Start the application:

   streamlit run app.py

## Limitations

The simulator uses a simplified stochastic demand
model. Holding costs, operating expenses, and
supplier capacity are not currently modelled.