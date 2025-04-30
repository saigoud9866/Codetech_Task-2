import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os

def read_data(file_path):
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file_path)
        else:
            return pd.read_csv(file_path, delimiter=None, engine='python')
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def analyze_data(df):
    analysis = {
        'shape': df.shape,
        'describe': df.describe(),
        'null_values': df.isnull().sum(),
        'data_types': df.dtypes
    }
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 1:
        analysis['correlation'] = df[numeric_cols].corr()
    return analysis

def create_plots(df, output_dir='temp_plots'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plots = {}
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        plt.figure()
        df[col].hist()
        plt.title(f'Distribution of {col}')
        plot_path = os.path.join(output_dir, f'{col}_hist.png')
        plt.savefig(plot_path)
        plt.close()
        plots[f'{col}_hist'] = plot_path
    if len(numeric_cols) > 0:
        plt.figure()
        df[numeric_cols].boxplot()
        plt.title('Box Plot of Numeric Columns')
        plot_path = os.path.join(output_dir, 'numeric_boxplot.png')
        plt.savefig(plot_path)
        plt.close()
        plots['numeric_boxplot'] = plot_path
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if len(df[col].unique()) <= 20:
            plt.figure()
            df[col].value_counts().head(10).plot(kind='bar')
            plt.title(f'Top 10 Values in {col}')
            plot_path = os.path.join(output_dir, f'{col}_bar.png')
            plt.savefig(plot_path)
            plt.close()
            plots[f'{col}_bar'] = plot_path
    return plots

def generate_reportlab_report(df, analysis, plots, output_file='report_reportlab.pdf'):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Data Analysis Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Dataset Overview", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Number of rows: {analysis['shape'][0]}", styles['Normal']))
    story.append(Paragraph(f"Number of columns: {analysis['shape'][1]}", styles['Normal']))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Column Data Types", styles['Heading2']))
    story.append(Spacer(1, 12))
    data_type_data = [['Column', 'Data Type']]
    for col, dtype in analysis['data_types'].items():
        data_type_data.append([col, str(dtype)])
    data_type_table = Table(data_type_data)
    data_type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(data_type_table)
    story.append(Spacer(1, 24))
    story.append(Paragraph("Missing Values", styles['Heading2']))
    story.append(Spacer(1, 12))
    null_data = [['Column', 'Missing Values']]
    for col, null_count in analysis['null_values'].items():
        null_data.append([col, null_count])
    null_table = Table(null_data)
    null_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(null_table)
    story.append(Spacer(1, 24))
    story.append(Paragraph("Basic Statistics", styles['Heading2']))
    story.append(Spacer(1, 12))
    stats_data = [analysis['describe'].columns.tolist()] + analysis['describe'].values.tolist()
    stats_table = Table(stats_data)
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 24))
    story.append(Paragraph("Visualizations", styles['Heading2']))
    story.append(Spacer(1, 12))
    for plot_name, plot_path in plots.items():
        story.append(Paragraph(plot_name.replace('_', ' ').title(), styles['Heading3']))
        story.append(Spacer(1, 12))
        try:
            img = Image(plot_path, width=400, height=300)
            story.append(img)
            story.append(Spacer(1, 24))
        except:
            story.append(Paragraph(f"Could not load image: {plot_path}", styles['Normal']))
            story.append(Spacer(1, 12))
    doc.build(story)
    print(f"ReportLab report generated: {output_file}")

def main():
    file_path = 'data1.csv'
    df = read_data(file_path)
    if df is None:
        print("Failed to read data. Exiting.")
        return
    analysis = analyze_data(df)
    plots = create_plots(df)
    generate_reportlab_report(df, analysis, plots, 'analysis_report_reportlab.pdf')
    for plot_path in plots.values():
        try:
            os.remove(plot_path)
        except:
            pass
    try:
        os.rmdir('temp_plots')
    except:
        pass

if __name__ == '__main__':
    main()
