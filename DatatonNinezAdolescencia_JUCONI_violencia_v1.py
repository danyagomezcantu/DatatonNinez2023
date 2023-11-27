# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18

@author: Danya
"""

import pandas as pd

# Leemos la base de datos como un DataFrame (reportes de 2011 a 2022)
reportes=pd.read_csv("C://Users//Danya//Downloads//JUCONI_Violencia.csv")

# "Traducimos" las fechas de los reportes a un tipo de datos que Pandas reconozca como fecha
reportes['FechaReporte'] = pd.to_datetime(reportes['FechaReporte'])

# Reordenamos nuestra base de datos según la fecha
reportes.set_index('FechaReporte', inplace=True)

# Creamos un DataFrame independiente para cada tipo de violencia
# Vamos a guardar sólo el primer y el último reporte para cada familia,
# para observar su mejoría tras el proceso terapéutico

# Violencia Física Pasiva ("VFPPuntaje")
vfp_df = pd.DataFrame().assign(ClaveFamilia=reportes['ClaveFamilia'], SubPrograma=reportes["SubPrograma"], Puntaje=reportes["VFPPuntaje"])
vfp_df = vfp_df.reset_index()
agrupar = vfp_df.groupby('ClaveFamilia')
primer_rep = agrupar.first().reset_index()
ultimo_rep = agrupar.last().reset_index()
vfp_df = pd.concat([primer_rep, ultimo_rep])

# Violencia Física Activa ("VFAPuntaje")
vfa_df = pd.DataFrame().assign(ClaveFamilia=reportes['ClaveFamilia'], SubPrograma=reportes["SubPrograma"], Puntaje=reportes["VFAPuntaje"])
vfa_df = vfa_df.reset_index()
agrupar = vfa_df.groupby('ClaveFamilia')
primer_rep = agrupar.first().reset_index()
ultimo_rep = agrupar.last().reset_index()
vfa_df = pd.concat([primer_rep, ultimo_rep])

# Violencia Emocional ("VEPuntaje")
ve_df = pd.DataFrame().assign(ClaveFamilia=reportes['ClaveFamilia'], SubPrograma=reportes["SubPrograma"], Puntaje=reportes["VEPuntaje"])
ve_df = ve_df.reset_index()
agrupar = ve_df.groupby('ClaveFamilia')
primer_rep = agrupar.first().reset_index()
ultimo_rep = agrupar.last().reset_index()
ve_df = pd.concat([primer_rep, ultimo_rep])

# Violencia Sexual ("VSPuntaje")
vs_df = pd.DataFrame().assign(ClaveFamilia=reportes['ClaveFamilia'], SubPrograma=reportes["SubPrograma"], Puntaje=reportes["VSPuntaje"])
vs_df = vs_df.reset_index()
agrupar = vs_df.groupby('ClaveFamilia')
primer_rep = agrupar.first().reset_index()
ultimo_rep = agrupar.last().reset_index()
vs_df = pd.concat([primer_rep, ultimo_rep])

# Violencia Patrimonial ("VPaPuntaje")
vpa_df = pd.DataFrame().assign(ClaveFamilia=reportes['ClaveFamilia'], SubPrograma=reportes["SubPrograma"], Puntaje=reportes["VPaPuntaje"])
vpa_df = vpa_df.reset_index()
agrupar = vpa_df.groupby('ClaveFamilia')
primer_rep = agrupar.first().reset_index()
ultimo_rep = agrupar.last().reset_index()
vpa_df = pd.concat([primer_rep, ultimo_rep])

# Elimino las variables que ya no estaré usando

del agrupar, primer_rep, ultimo_rep

#

# Para cada tipo de violencia, identificamos el puntaje promedio inicial que las familias tenían,
# y el puntaje promedio final que tuvieron al graduarse, así como el tiempo que les tomó

data=[vfp_df, vfa_df, ve_df, vs_df, vpa_df]

for i in data:
    avg_initial_score = i.groupby('ClaveFamilia')['Puntaje'].first().mean()
    avg_final_score = i.groupby('ClaveFamilia')['Puntaje'].last().mean()  
    avg_time_diff = (i.groupby('ClaveFamilia')['FechaReporte'].apply(lambda x: (x.max()-x.min()).days).mean())/365
    overall_decrease = ((avg_initial_score - avg_final_score)/avg_initial_score)*100
    annual_decrease_rate = overall_decrease/avg_time_diff
    
    print(f"La tasa de anual promedio de disminución de violencia es {annual_decrease_rate:.2f}%")