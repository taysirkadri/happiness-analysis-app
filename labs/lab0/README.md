# Lab 0 – Dataset Understanding and First Checks
This is my assignment for the data analysis class. We needed a dataset that could support a full eight‑lab workflow—from raw inspection to a final Streamlit dashboard. I chose the **World Happiness Report (2015‑2019)** because: 
1. it is a globally‑recognised, multi‑dimensional measure of well‑being that combines objective economic indicators (GDP per capita) with subjective factors (social support, freedom, trust).
2. Its yearly CSV releases provide a tidy, moderately sized tabular data source, perfect for practising data cleaning, exploratory analysis, and linear‑regression modelling across several years. 
3.Moreover, the dataset’s mix of quantitative and qualitative variables sparks curiosity about what truly drives happiness, making it an engaging story‑driven case study for both learning and presentation.

I tried to not just copy the numbers but actually think about what they mean. Some things I found were surprising.

---

## 1. Context (What)
We are working with the **World Happiness** dataset (2015‑2019).  
Before any analysis, we need a solid picture of **what the data looks like** – its shape, types, and missingness.

## 2. Objective (Why)
A clean mental model of the raw data prevents hidden surprises later (e.g., mismatched columns, silent NaNs).  
So..
Before proceeding with any advanced data processing and analytics, I need to be sure for how the data is structured so i can planify the way I think it is. This lab we'll check basic shape, column types, and missing values.

## 3. Methodology (How did I get it done?)

- Scanned the `data/raw/` folder for the five CSV files.
- Extracted the year from each filename.
- Loaded each file with **pandas**, recorded basic stats (rows, columns, missing %).
- Combined everything into one dataframe and wrote a **column‑overview table** (`lab0_column_overview.csv`).
- Plotted a missing‑value heatmap and a happiness‑score distribution.

**Used Tools & libraries**  
- **pandas** – loading & inspecting CSVs  
- **pathlib / re** – infer the year from the filename  
- **matplotlib / seaborn** – quick visual sanity checks  


## 4. Implementation Summary
- All CSVs read, year‑inferred, and concatenated into a single dataframe.  
- `lab0_column_overview.csv` written to `outputs/tables/`.  
- Two diagnostic PNGs saved under `outputs/plots/`.  

## 5. Results & Interpretation


> **What did I learn?** The six core drivers (GDP, social support, life expectancy, freedom, trust, generosity) are almost fully populated – a relief! The `Region` column is mostly empty, showing how the report changed its schema over time. That will need attention in later cleaning steps.

| Metric | Value |
|-------|-------|
| Total rows (all years) | 856 |
| Columns (raw) | 19 |
| Columns with > 0 % missing | `Region` |

## 6. Outputs
lab0/ ├─ outputs/ │ ├─ plots/ │ │ ├─ lab0_plot_missing_values.png │ │ └─ lab0_plot_happiness_distribution.png │ └─ tables/ │ └─ lab0_column_overview.csv






