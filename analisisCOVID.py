import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CARGA DE DATOS
df = pd.read_csv("fallecidos_covid.csv",sep=";", encoding="utf-8", dtype= str)
print(df.head(10))
print(df.info())

#LIMPIEZA DE DATOS
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)
print("DESPUES DE LA LIMPIEZA: ")
print(df.columns.to_list())

#CONVERSION DE DATOS
df["fecha_corte"]=pd.to_datetime(df["fecha_corte"],errors="coerce")
df["fecha_fallecimiento"]= pd. to_datetime(df["fecha_fallecimiento"],errors="coerce")
df["edad_declarada"]= pd.to_numeric(df["edad_declarada"],errors="coerce")
print("DESPUES DE LA CONVERSION: ")
print(df.dtypes.head(10))

# VALIDACION DE NULOS
print({
    "fecha_corte_na":df["fecha_corte"].isna().sum(),
    "fecha_fallecimiento_na":df["fecha_fallecimiento"].isna().sum(),
    "edad_declarada_na":df["edad_declarada"].isna().sum()
})

# BUSCA DE LOS KPIS (EDA)
print("KPIS: ")
print("TOTAL DE FALLECIDOS: ", len(df))

print("FALLECIDOS POR SEXO: ")
print(df["sexo"].value_counts())

print("TOP 5 DEPARTAMENTOS MAS AFECTADOS: ")
top5_dep=df["departamento"].value_counts().head(5)
print(top5_dep)

print("PROMEDIO DE EDAD: ",round(df["edad_declarada"].mean(),2))

print("FALLECIDOS POR AÑO: ")
fallecidos_por_anio=df["fecha_fallecimiento"].dt.year.value_counts().sort_index()
print(fallecidos_por_anio)

# VISUALIZACION DE LOS KPIS
sns.set(style="whitegrid")

#FALLECIDOS POR SEXO
plt.figure(figsize=(8,5))
sns.countplot(data=df, x="sexo", palette="coolwarm")
plt.title("FALLECIDOS POR SEXO")
plt.xlabel("SEXO")
plt.ylabel("CANTIDAD")
plt.show()

#DEPARTAMENTOS MAS AFECTADOS (TOP 5)
plt.figure(figsize=(8,5))
sns.barplot(x=top5_dep.index,y=top5_dep.values, palette="Reds_r")
plt.title("TOP 5 DEPARTAMENTOS AFECTADOS")
plt.xlabel("DEPARTAMENTOS")
plt.ylabel("CANTIDAD")
plt.show()

#PROMEDIO DE EDAD
plt.figure(figsize=(8,5))
sns.histplot(df["edad_declarada"], bins=20, kde=True , color="Skyblue")
plt.title("PROMEDIO DE EDADES")
plt.xlabel("EDADES")
plt.ylabel("CANTIDAD")
plt.show()

#CORRELACION
df["anio_fallecimiento"] = df["fecha_fallecimiento"].dt.year
corr=df[["edad_declarada", "anio_fallecimiento"]].corr()
print("MAPA DE CALOR-CORRELACION")
print(corr)

plt.figure(figsize=(8,5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("MAPA DE CALOR-CORRELACION")
plt.show()

#AGRUPACION
promedio_fallecidos_por_sexo=df.groupby("sexo")["edad_declarada"].mean().head(2)
print("PROMEDIO DE FALLECIDOS POR SEXO: ")
print(promedio_fallecidos_por_sexo)

plt.figure(figsize=(8,5))
sns.barplot(x=promedio_fallecidos_por_sexo.index,y=promedio_fallecidos_por_sexo.values, palette="Blues_r")
plt.title("PROMEDIO DE FALLECIDOS POR SEXO")
plt.xlabel("SEXO")
plt.ylabel("PROMEDIO")
plt.show()

# RESULTADOS
fallecidos_por_sexo= df["sexo"].value_counts()

resultados = {
    "TOTAL_FALLECIDOS":[len(df)],
    "M-FALLECIDOS":[fallecidos_por_sexo.get("MASCULINO",0)],
    "F-FALLECIDOS":[fallecidos_por_sexo.get("FEMENINO", 0)],
    "TOP5_DEPARTAMENTOS":[";".join(top5_dep.index)],
    "FALLECIDOS_POR_ANIO":[
    ", ".join([f"{int(a)}: {int(c)}" for a, c in fallecidos_por_anio.items()])    
    ]
}
# EXPORTAR KPIS
kpi_df=pd.DataFrame(resultados)
kpi_df.to_excel("resultados_kpi_covid_completo.xlsx", index=False)
print("RESULTADOS EXPORTADOS CORRECTAMENTE")