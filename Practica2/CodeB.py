import matplotlib.pyplot as plt
import pandas as pd

# 1. Cargar la base de datos
df = pd.read_csv("Practica2/practica_ciencia_datos_limpieza_1500.csv")

# 2. Definir la función para convertir a números y manejar errores
def a_num(serie):
    return pd.to_numeric(serie, errors='coerce')

# 3. Generación de gráficos
# Figura B.1 - Boxplot de edad
plt.figure(figsize=(6, 6))
plt.boxplot(a_num(df["edad"]).dropna())
plt.title("EDAD")
plt.ylabel("Edad (años)")
plt.tight_layout()
plt.savefig("Fig_B1_boxplot_edad.png", dpi=150)
plt.close()
 
# Figura B.2 - Boxplot de ingreso mensual
plt.figure(figsize=(6, 6))
plt.boxplot(a_num(df["ingreso_mensual_cliente"]).dropna())
plt.title("INGRESO MENSUAL DEL CLIENTE")
plt.ylabel("MXN")
plt.tight_layout()
plt.savefig("Fig_B2_boxplot_ingreso.png", dpi=150)
plt.close()
 
# Figura B.3 (a) - Promedio de total_venta por ciudad (sin normalizar)
prom_ciudad = (df.assign(total_num=a_num(df["total_venta"]))
                 .groupby("ciudad", dropna=False)["total_num"].mean())
prom_ciudad.index = prom_ciudad.index.fillna("(en blanco)")

plt.figure(figsize=(8, 8))
prom_ciudad.sort_index().plot(kind="barh")
plt.title("Promedio de total_venta por ciudad (datos crudos)")
plt.tight_layout()
plt.savefig("Fig_B3a_promedio_por_ciudad.png", dpi=150)
plt.close()
 
# Figura B.3 (b) - Promedio de total_venta por fecha (texto crudo)
prom_fecha = (df.assign(total_num=a_num(df["total_venta"]))
                .groupby("fecha_venta", dropna=False)["total_num"].mean())

prom_fecha.index = prom_fecha.index.fillna("(sin fecha)")
etiquetas_x = [str(x) for x in prom_fecha.index]

plt.figure(figsize=(12, 5))
plt.bar(etiquetas_x, prom_fecha.values)
plt.title("Promedio de total de venta por fecha (datos crudos)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("Fig_B3b_promedio_por_fecha.png", dpi=150)
plt.close()
# Figura B.4 - Visitas web vs ventas
plt.figure(figsize=(7, 5))
plt.scatter(a_num(df["visitas_web_30d"]), a_num(df["total_venta"]))
plt.title("Visita al sitio web vs Ventas")
plt.xlabel("Visitas Web (30 días)")
plt.ylabel("Total Venta")
plt.tight_layout()
plt.savefig("Fig_B4_visitas_vs_ventas.png", dpi=150)
plt.close()
 
# Figura B.5 - Ingreso mensual vs edad
plt.figure(figsize=(7, 5))
plt.scatter(a_num(df["ingreso_mensual_cliente"]), a_num(df["edad"]))
plt.title("Ingreso mensual vs Edad")
plt.xlabel("Ingreso Mensual (MXN)")
plt.ylabel("Edad (años)")
plt.tight_layout()
plt.savefig("Fig_B5_ingreso_vs_edad.png", dpi=150)
plt.close()