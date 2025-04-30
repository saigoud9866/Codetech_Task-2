# Codetech_Task-2
PROJECT ON PYTHON LEARNING

Overview
This project provides a comprehensive solution for analyzing datasets and generating professional PDF reports with visualizations. It automatically processes data files, performs statistical analysis, creates visualizations, and compiles everything into a well-formatted PDF document.

Features
Multi-format Support: Reads CSV, Excel, and other tabular data formats

Automated Analysis: Calculates key statistics, data types, and missing values

Visualizations: Generates histograms, box plots, and bar charts

Professional Reporting: Creates PDF reports with ReportLab

Clean Architecture: Modular design with separate functions for each task

Requirements
Python 3.6+

Required libraries:

bash
pip install pandas matplotlib reportlab openpyxl
Installation
Install dependencies:

bash
pip install -r requirements.txt
Place your data file (CSV/Excel) in the project directory or specify the path

Usage
Modify the file_path variable in the main() function to point to your data file

Run the script:

bash
python data_analysis_report.py
The script will:

Analyze your data

Generate visualizations

Create a PDF report (default: analysis_report_reportlab.pdf)

Clean up temporary files

Customization Options
Data Analysis:

Add additional statistical measures in analyze_data()

Include custom correlation analyses

Visualizations:

Modify plot styles in create_plots()

Add additional chart types (scatter plots, heatmaps, etc.)

Report Formatting:

Adjust PDF styling in generate_reportlab_report()

Add custom sections or headers

Modify table styles and colors

Output Includes
Dataset Overview:

Number of rows and columns

Column data types

Data Quality:

Missing values count per column

Statistical Analysis:

Descriptive statistics (count, mean, std, min, max, etc.)

Visualizations:

Histograms for numeric columns

Box plots for numeric data

Bar charts for categorical data

Example Report Structure
Title page with generation timestamp

Dataset overview

Column data types table

Missing values analysis

Descriptive statistics table

Visualization section with all generated plots
