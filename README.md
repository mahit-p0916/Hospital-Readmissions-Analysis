# U.S. Hospital Readmissions Analysis

Analyzing CMS hospital readmission penalty data across all U.S. states to identify high-risk facilities, conditions, and geographic patterns using Python and Tableau.

---

## Overview

The Centers for Medicare & Medicaid Services (CMS) penalizes hospitals with excess readmission rates under the Hospital Readmissions Reduction Program (HRRP). This project analyzes that data to uncover which conditions, states, and hospitals carry the highest readmission risk - insights directly relevant to hospital strategic planning and operations.

---

## Tools & Technologies

- **Python** - data cleaning and analysis
- **Pandas** - data manipulation and aggregation
- **Matplotlib** - chart generation
- **Tableau** - interactive dashboard
- **Data Source** - CMS Hospital Readmissions Reduction Program (2021–2024)

---

## Project Structure

```
Hospital_Readmissions_Project/
│
├── Data/
│   └── readmissions.csv               # Raw CMS dataset
│
├── Script/
│   └── Readmissions_Analysis.py       # Main Python analysis script
│
├── outputs/
│   ├── chart1_err_by_condition.png    # Avg ERR by condition
│   ├── chart2_top_states_penalized.png # Top 20 states by penalty rate
│   ├── chart3_err_distribution.png    # ERR spread by condition
│   ├── chart4_worst_hospitals.png     # Top 15 highest-risk hospitals
│   ├── readmissions_clean_tableau.csv # Cleaned data for Tableau
│   └── Hospital_Readmissions_Dashboard.twb  # Tableau dashboard
│
└── README.md
```

---

## Key Findings

- Nearly half of all hospital-condition pairs nationally exceed CMS readmission benchmarks
- The Northeast and Southeast show the highest state-level penalty rates
- Hip/Knee Replacement carries the highest average Excess Readmission Ratio across all conditions
- Massachusetts has the highest concentration of high-risk hospitals in the top 15

---

## Dashboard

The Tableau dashboard includes three interactive views:

- **National Map** - average ERR by state with color intensity indicating penalty risk
- **ERR by Condition** - condition-level bar chart with a 1.0 benchmark reference line
- **Top 15 Hospitals** - highest-risk facilities ranked by average ERR across conditions

Clicking any state on the map filters both charts dynamically.

---

## How to Run

1. Clone the repository
2. Place `readmissions.csv` in the `Data/` folder
3. Run the analysis script:
```bash
python Script/Readmissions_Analysis.py
```
4. Output charts and cleaned CSV will be saved to the `outputs/` folder
5. Open `Hospital_Readmissions_Dashboard.twb` in Tableau Desktop

---

## Data Source

Centers for Medicare & Medicaid Services (CMS)
Hospital Readmissions Reduction Program (HRRP)
