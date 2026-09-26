# APL Logistics Supply Chain Analytics

## Delivery Performance, Delay Risk, and Logistics Efficiency Analysis in Global Supply Chain Operations

This project analyzes supply chain delivery performance using shipment, delivery, customer, regional, market, and shipping-mode data.

The project focuses on identifying delivery delays, measuring late-delivery risk, comparing shipping modes, analyzing regional patterns, and identifying operational risk hotspots.

## Problem Statement

Delivery delays can lead to SLA violations, increased logistics costs, and reduced customer satisfaction. This project uses data analytics to identify delay patterns and provide insights that can support more proactive logistics management.

## Objectives

- Analyze overall delivery performance.
- Calculate on-time, delayed, and early shipments.
- Measure delivery delay using actual vs scheduled shipping duration.
- Analyze late-delivery risk.
- Compare shipping modes.
- Identify high-delay regions and markets.
- Analyze customer segment patterns.
- Identify regional and shipping-mode risk hotspots.
- Develop an interactive Streamlit dashboard.

## Key Metrics

- On-Time Delivery Rate
- Average Delivery Delay
- Late Delivery Risk Ratio
- Shipping Mode Performance
- Regional Delay Index
- Delay Rate by Market
- Operational Risk Hotspots

## Methodology

### 1. Data Cleaning
- Checked missing values and duplicate records.
- Handled missing customer information.
- Validated shipping-duration values.
- Standardized data for analysis.

### 2. Delay Gap Calculation

The delivery delay was calculated using:

**Delay Gap = Actual Shipping Days − Scheduled Shipping Days**

Based on the delay gap:

- **Delayed:** Delay Gap > 0
- **On-time:** Delay Gap = 0
- **Early:** Delay Gap < 0

Cancelled shipments were excluded from completed-delivery performance calculations.

### 3. Exploratory Analysis

The analysis covers:

- Overall delivery performance
- Late-delivery risk
- Shipping mode comparison
- Regional delay analysis
- Market-level analysis
- Customer segment analysis
- Delivery risk hotspot analysis

## Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Google Colab
- GitHub

## Dashboard Features

The Streamlit dashboard provides:

- Logistics Performance Snapshot
- Delivery Health Analysis
- Shipping Mode Performance
- Regional Risk Analysis
- Market Performance
- Regional Delivery Performance Heatmap
- Delivery Risk Hotspot Explorer
- Interactive filters for:
  - Shipping Mode
  - Order Region
  - Market
  - Customer Segment

## Dataset

The analysis was performed using an APL Logistics supply chain dataset containing shipment, delivery, customer, product, regional, market, and shipping information.

The full dataset was analyzed in Google Colab. A smaller processed dataset is used for the deployed dashboard to improve GitHub and Streamlit compatibility.

## Key Findings

The analysis identified differences in delivery performance across shipping modes, regions, and markets.

The results provide a data-driven view of:

- Delivery delay patterns
- Late-delivery risk
- Regional performance differences
- Shipping-mode performance
- Operational risk combinations

## Recommendations

- Monitor regions with consistently high delay rates.
- Review shipping modes with lower on-time performance.
- Use shipment volume together with delay rate when identifying hotspots.
- Monitor late-delivery risk proactively.
- Use regional and shipping-mode insights to support preventive logistics planning.

## Project Structure

```text
APL-Logistics-Supply-Chain-Analytics/
│
├── app.py
├── APL_Logistics_Processed.csv
└── README.md

## How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/Anjali16161/APL-Logistics-Supply-Chain-Analytics.git

2. Open the project folder:
cd APL-Logistics-Supply-Chain-Analytics

3.Install the project folder:
pip install streamlit pandas numpy matplotlib seaborn

4. Run the dashboard:
streamlit run app.py

5. Open the local address shown in the terminal, usually:
http://localhost:8501

## Technologies Used
Python
Pandas
NumPy
Matplotlib
Seaborn
Streamlit
Google Colab
GitHub

Author
Anjali Basude
B.Sc. Data Science
St. Ann's Degree College for Women, Hyderabad
