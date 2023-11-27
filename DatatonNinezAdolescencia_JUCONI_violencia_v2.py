# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18

@author: Danya
"""

import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np

# Leemos la base de datos como un DataFrame (reportes de 2011 a 2022)
reportes=pd.read_csv("C://Users//Danya//Downloads//JUCONI_Violencia.csv")

# "Traducimos" las fechas de los reportes a un tipo de datos que Pandas reconozca como fecha
reportes['FechaReporte'] = pd.to_datetime(reportes['FechaReporte'])

# Reordenamos nuestra base de datos según la fecha
reportes.set_index('FechaReporte', inplace=True)

# Creamos un DataFrame independiente para cada tipo de violencia
# A partir de ahí, creamos un DataFrame final
# con sus puntajes inicial y final promedio, duración del proceso terapéutico promedio
# y tasa anual de disminución de violencia

final=pd.DataFrame() # vacío
columnas = ["Puntaje inicial promedio", "Puntaje final promedio", "Tasa anual promedio de disminución (%)"]

# Primero identificamos las columnas que indican el puntaje para cada tipo de violencia
# y a qué DataFrame lo vamos a mandar

dfs_nombres = [("vfp_df", "VFPPuntaje"),("vfa_df", "VFAPuntaje"),("ve_df", "VEPuntaje"),("vs_df", "VSPuntaje"),("vpa_df", "VPaPuntaje")]

tipos_violencia={"vfp_df":"Violencia Física Pasiva","vfa_df":"Violencia Física Activa","ve_df":"Violencia Emocional","vs_df":"Violencia Sexual","vpa_df":"Violencia Patrimonial"}

for df_nombre, nombre in dfs_nombres:
    df = pd.DataFrame().assign(ClaveFamilia=reportes['ClaveFamilia'], SubPrograma=reportes["SubPrograma"], Puntaje=reportes[nombre])
    df = df.reset_index()
    
    agrupar = df.groupby('ClaveFamilia')
    primer_rep = agrupar.first().reset_index()
    ultimo_rep = agrupar.last().reset_index()
    globals()[df_nombre] = pd.concat([primer_rep, ultimo_rep])
    
    avg_initial_score = df.groupby('ClaveFamilia')['Puntaje'].first().mean()
    avg_final_score = df.groupby('ClaveFamilia')['Puntaje'].last().mean()  
    avg_time_diff = (df.groupby('ClaveFamilia')['FechaReporte'].apply(lambda x: (x.max()-x.min()).days).mean())/365
    overall_decrease = ((avg_initial_score - avg_final_score)/avg_initial_score)*100
    annual_decrease_rate = overall_decrease/avg_time_diff
    
    final.loc[tipos_violencia[df_nombre], columnas] = [avg_initial_score, avg_final_score, annual_decrease_rate]

# Elimino las variables que ya no estaré usando
del tipos_violencia, agrupar, df, df_nombre, dfs_nombres, primer_rep, ultimo_rep, nombre
del columnas, overall_decrease, avg_time_diff, avg_initial_score, avg_final_score, annual_decrease_rate