# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26
@author: Danya
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read in the CSV files as dataframes
reportes = pd.read_csv("C://Users//Danya//Downloads//JUCONI_Violencia.csv", usecols=["ClaveFamilia", "SubPrograma", "FechaReporte", "VFPPuntaje", "VFAPuntaje", "VEPuntaje", "VSPuntaje", "VPaPuntaje"])
funcionamiento = pd.read_csv("C://Users//Danya//Downloads//JUCONI_EFF.csv", usecols=["subprograma", "ClaveFamilia", "FechaReporte", "PTPuntajeGlobal"])

# Drop any missing values from both dataframes
reportes.dropna(inplace=True)
funcionamiento.dropna(inplace=True)

# Perform the desired calculations on the specified columns in `reportes`
reportes["VFPPuntaje"] = (reportes["VFPPuntaje"]/84)*100
reportes["VFAPuntaje"] = (reportes["VFAPuntaje"]/124)*100
reportes["VEPuntaje"] = (reportes["VEPuntaje"]/1840)*100
reportes["VSPuntaje"] = (reportes["VSPuntaje"]/1259)*100
reportes["VPaPuntaje"] = (reportes["VPaPuntaje"]/80)*100

# Drop any rows in `funcionamiento` where PTPuntajeGlobal is over 100
funcionamiento = funcionamiento[funcionamiento["PTPuntajeGlobal"] <= 100]

def impact_of_violence_on_functioning(reportes, funcionamiento):
    # Merge the two data frames on the common columns ClaveFamilia and FechaReporte
    merged_df = pd.merge(reportes, funcionamiento, on=["ClaveFamilia", "FechaReporte"])
    
    # Calculate the correlation between each type of violence and the family functioning score
    corr_df = merged_df[["VFPPuntaje", "VFAPuntaje", "VEPuntaje", "VSPuntaje", "VPaPuntaje", "PTPuntajeGlobal"]].corr()
    
    # Return the correlation matrix
    return corr_df

vis1=impact_of_violence_on_functioning(reportes, funcionamiento)
# Plot the heatmap
plt.figure(figsize=(8, 6))
ax = plt.axes()
cmap = sns.color_palette(["#4682B4","#5E8AA8","#7F92A5","#B0C4DE","#F8D7B5","#FEE9D7","#FED4B6","#FDAE88","#FB8740","#E55C0E"], as_cmap=True)
sns.heatmap(vis1, annot=True, cmap=cmap)
plt.title('Correlation Matrix')
plt.show()

def observe_violence_changes_with_functioning(reportes, funcionamiento):
    # Merge the two data frames on the common columns ClaveFamilia and FechaReporte
    merged_df = pd.merge(reportes, funcionamiento, on=["ClaveFamilia", "FechaReporte"])
    
    # Calculate the mean values of each type of violence and family functioning score for each unique value of PTPuntajeGlobal
    grouped_df = merged_df.groupby("PTPuntajeGlobal")[["VFPPuntaje", "VFAPuntaje", "VEPuntaje", "VSPuntaje", "VPaPuntaje"]].mean()
    
    # Return the grouped data frame
    return grouped_df

vis2=observe_violence_changes_with_functioning(reportes, funcionamiento)

grouped_df=observe_violence_changes_with_functioning(reportes, funcionamiento)

# Set the color palette
palette = sns.color_palette(["#3383BA", "#1F5F8B", "#FF8010", "#FFB407", "#FDD835"])

# Plot the stacked bar chart
grouped_df.plot(kind="bar", stacked=True, color=palette)
plt.xlabel("Family Functioning Score")
plt.ylabel("Count")
plt.title("Violence Types and Family Functioning")
plt.legend(title="Violence Types", bbox_to_anchor=(1.0, 1.0))
plt.show()