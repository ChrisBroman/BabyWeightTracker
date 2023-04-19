import pandas as pd
import openpyxl
import scipy.stats as stats

def get_percentile(weight, month):
    df = pd.read_excel('../percentile.xlsx')
    L = df.iloc[month]['L']
    M = df.iloc[month]['M']
    S = df.iloc[month]['S']
    z_score = ((weight / M) ** L - 1) / (L * S)
    percentile = stats.norm.cdf(z_score) * 100
    return percentile
    
        
