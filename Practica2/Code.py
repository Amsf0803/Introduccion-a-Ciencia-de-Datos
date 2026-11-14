# Práctica de Ciencia de Datos — Limpieza, Imputación y Outliers
# Coloca este archivo .py y el CSV original en la misma carpeta.

import pandas as pd

# =============================================================================
# SECCIÓN A: Carga e inspección inicial
# =============================================================================
archivo = "Practica2/practica_ciencia_datos_limpieza_1500.csv"
df = pd.read_csv(archivo)
print("CSV cargado correctamente")

print("Primeras cinco filas:")
print(df.head())

print("\nÚltimas cinco filas:")
print(df.tail())

print("\nDimensiones (filas, columnas):", df.shape)
print("\nNombres de las columnas:")
print(df.columns.tolist())

print("\nTipos de datos detectados:")
print(df.dtypes)

print("\nInformación general:")
df.info()

print("Descripción numérica:")
print(df.describe())

print("\nDescripción categórica:")
print(df.describe(include=["object"]))

print("\nDescripción global:")
print(df.describe(include="all"))

print("\nUnidad de observación:")
print("Cada fila representa una venta de un producto realizada por un cliente en una fecha, con datos de la compra y del cliente.")

tipos_ideales = {
    'id_venta': 'string', 'fecha_venta': 'datetime64[ns]', 'id_cliente': 'string', 
    'edad': 'Int64 (entero nulo)', 'ciudad': 'string / category', 'region': 'string / category', 
    'segmento': 'category', 'canal': 'category', 'categoria_producto': 'category', 
    'producto': 'string / category', 'cantidad': 'Int64', 'precio_unitario': 'float64', 
    'descuento_pct': 'Float64 (nulo)', 'total_venta': 'float64', 'metodo_pago': 'category', 
    'ingreso_mensual_cliente': 'Float64 (nulo)', 'satisfaccion': 'Int64 (entero nulo)', 
    'dias_entrega': 'Int64 (entero nulo)', 'devolucion': 'category', 'respuesta_campana': 'category', 
    'campanas_recibidas_6m': 'Int64', 'visitas_web_30d': 'Int64', 'antiguedad_cliente_meses': 'Int64', 
    'codigo_postal': 'string'
}

tabla_tipos = pd.DataFrame({
    "variable": df.columns,
    "tipo_actual": [str(df[col].dtype) for col in df.columns],
    "tipo_ideal": [tipos_ideales[col] for col in df.columns]
})
print(tabla_tipos.to_string(index=False))



# SECCIÓN C: Diagnóstico de calidad (COMPLETA)

print("\n--- SECCIÓN C: Diagnóstico de Calidad ---")

# C.1 Cuantificar nulos por columna y porcentaje de ausencia
nulos_totales = df.isna().sum()
porcentaje_nulos = (nulos_totales / len(df)) * 100
tabla_nulos = pd.DataFrame({
    'Nulos_Totales': nulos_totales, 
    'Porcentaje (%)': porcentaje_nulos
})
print("C.1 - Variables con valores nulos (NaN):")
print(tabla_nulos[tabla_nulos['Nulos_Totales'] > 0].round(2))

# C.2 Buscar valores que funcionen como nulos sin ser NaN (NA, N/A, -, -999, etc.)
print("\nC.2 - Búsqueda de nulos ocultos:")
valores_sospechosos = ['NA', 'N/A', '-', '?', 'null', ' ', '']
for col in df.select_dtypes(include=['object', 'string']).columns:
    conteo_ocultos = df[col].astype(str).str.strip().isin(valores_sospechosos).sum()
    if conteo_ocultos > 0:
        print(f" - '{col}': {conteo_ocultos} valores sospechosos de ser nulos en texto.")

if 'edad' in df.columns:
    edades_sospechosas = (pd.to_numeric(df['edad'], errors='coerce') == -999).sum()
    if edades_sospechosas > 0:
        print(f" - 'edad': {edades_sospechosas} valores con -999.")

# C.3 Detectar duplicados exactos
duplicados = df.duplicated().sum()
print(f"\nC.3 - Duplicados exactos encontrados en todo el DataFrame: {duplicados}")

# C.4 Detectar categorías equivalentes
print("\nC.4 - Revisión de categorías:")
if 'categoria_producto' in df.columns:
    print("Valores únicos en 'categoria_producto':\n", df['categoria_producto'].dropna().unique())
if 'ciudad' in df.columns:
    print("Valores únicos en 'ciudad' (muestra):\n", df['ciudad'].dropna().unique()[:10])

# C.5 Detectar tipos incorrectos
print("\nC.5 - Tipos de datos detectados que suelen ser incorrectos:")
cols_revisar = ['fecha_venta', 'precio_unitario', 'total_venta']
for col in cols_revisar:
    if col in df.columns:
        print(f" - '{col}' es de tipo: {df[col].dtype}")

# C.6 Detectar reglas de dominio incumplidas
print("\nC.6 - Reglas de dominio incumplidas:")
if 'edad' in df.columns:
    edad_num = pd.to_numeric(df['edad'], errors='coerce')
    print(f" - Edades ilógicas (<0 o >120): {((edad_num < 0) | (edad_num > 120)).sum()}")

if 'descuento_pct' in df.columns:
    desc_num = pd.to_numeric(df['descuento_pct'], errors='coerce')
    print(f" - Descuentos negativos: {(desc_num < 0).sum()}")

if 'dias_entrega' in df.columns:
    dias_num = pd.to_numeric(df['dias_entrega'], errors='coerce')
    print(f" - Días de entrega negativos: {(dias_num < 0).sum()}")

# C.7 Buscar inconsistencias entre variables
print("\nC.7 - Inconsistencias matemáticas entre variables:")
if all(c in df.columns for c in ['total_venta', 'cantidad', 'precio_unitario', 'descuento_pct']):
    t_venta = pd.to_numeric(df['total_venta'], errors='coerce')
    cant = pd.to_numeric(df['cantidad'], errors='coerce')
    precio = pd.to_numeric(df['precio_unitario'], errors='coerce')
    desc = pd.to_numeric(df['descuento_pct'], errors='coerce').fillna(0)
    
    venta_teorica = cant * precio * (1 - desc)
    inconsistencias_matematicas = (abs(t_venta - venta_teorica) > 0.1).sum()
    print(f" - Compras donde el 'total_venta' no coincide con la fórmula matemática: {inconsistencias_matematicas}")

# # COMENTARIO J (Justificación C):
# # 1. Problema: Datos faltantes explícitos/ocultos, registros duplicados e inconsistencias lógicas (ej. total_venta != cantidad * precio).
# # 2. Por qué es un problema: Provoca sesgos estadísticos, rompe la integridad referencial y genera cálculos financieros erróneos.
# # 3. Información perdida: Al marcar como nulos o eliminar registros incoherentes, se pierden observaciones reales si el error fue solo de dedo al capturar.


# =============================================================================
# SECCIÓN D: Limpieza y estandarización (SOLO INCISO 2)
# =============================================================================
print("\n--- SECCIÓN D: Limpieza (Solo fechas) ---")

# D.2 Convertir fechas y documentar qué valores no pudieron convertirse
fechas_originales = df['fecha_venta'].copy()
df['fecha_venta_limpia'] = pd.to_datetime(df['fecha_venta'], errors="coerce")

nulos_tras_conversion = df['fecha_venta_limpia'].isna() & fechas_originales.notna()
print("Valores en 'fecha_venta' que no pudieron convertirse a datetime:")
print(fechas_originales[nulos_tras_conversion].unique())

# # COMENTARIO J (Justificación D):
# # 1. Problema: Formatos de fecha heterogéneos o texto corrupto que impiden operaciones temporales.
# # 2. Por qué es un problema: Imposibilita agrupar por mes, detectar estacionalidades o calcular métricas de series de tiempo.
# # 3. Información perdida: Se pierde el texto original inaccesible (ej. fechas mal escritas), transformándolas en NaT (Not a Time).


# =============================================================================
# SECCIÓN E: Estrategia de imputación (SIN INCISO 5)
# =============================================================================
print("\n--- SECCIÓN E: Imputación ---")

# E.1 Clasificar variables con nulos
print("E.1 - Clasificación de variables con valores nulos:")
nulos_por_columna = df.isna().sum()
columnas_con_nulos = nulos_por_columna[nulos_por_columna > 0].index

if len(columnas_con_nulos) > 0:
    for col in columnas_con_nulos:
        tipo_pandas = str(df[col].dtype)
        if 'int' in tipo_pandas or 'float' in tipo_pandas:
            clasificacion = "Numérica"
        elif 'datetime' in tipo_pandas:
            clasificacion = "Temporal"
        elif 'object' in tipo_pandas or 'category' in tipo_pandas:
            clasificacion = "Categórica (o Ordinal)" 
        else:
            clasificacion = "Otro"
        
        print(f" - {col}: {clasificacion} (Tipo: {tipo_pandas} | Nulos: {nulos_por_columna[col]})")

# E.3 y E.4 Comparar dos estrategias en una variable numérica (edad)
edad_nulos = pd.to_numeric(df['edad'], errors='coerce')
edad_media = edad_nulos.fillna(edad_nulos.mean())
edad_mediana = edad_nulos.fillna(edad_nulos.median())

def calcular_estadisticas(serie):
    s = serie.dropna()
    return [s.mean(), s.median(), s.std(), s.quantile(0.75) - s.quantile(0.25)]

stats_imputacion = pd.DataFrame({
    'Edad_Con_Nulos': calcular_estadisticas(edad_nulos),
    'Imp_Media': calcular_estadisticas(edad_media),
    'Imp_Mediana': calcular_estadisticas(edad_mediana)
}, index=['Media', 'Mediana', 'Desv_Std', 'IQR'])

print("\nE.3/E.4 - Comparación de estrategias para 'edad':")
print(stats_imputacion.round(2))

# E.2 Decisión aplicada: Imputación por mediana
df['edad_imputada'] = edad_mediana

# # COMENTARIO J (Justificación E):
# # 1. Problema: La presencia de nulos en 'edad' reduce el tamaño de la muestra utilizable.
# # 2. Por qué es un problema: Reducir la muestra mediante eliminación completa (listwise deletion) sesga el análisis.
# # 3. Información perdida: Al imputar por mediana se conserva el centro de la distribución pero se comprime la varianza original (la desviación estándar disminuye levemente).


# =============================================================================
# SECCIÓN F: Representación y resumen (SOLO INCISO 5)
# =============================================================================
print("\n--- SECCIÓN F: Ordenamiento y Filtros ---")

# F.5 Ordenamientos y filtros para identificar grupos relevantes
if 'total_venta' in df.columns:
    ventas_numericas = pd.to_numeric(df['total_venta'], errors='coerce')
    limite_top10 = ventas_numericas.quantile(0.90)
    compras_top = df[ventas_numericas > limite_top10].sort_values(by='total_venta', ascending=False)
    
    print(f"Filtro aplicado: {len(compras_top)} compras pertenecen al Top 10% de ventas (>$ {limite_top10:.2f})")
    print(compras_top[['id_cliente', 'total_venta', 'categoria_producto']].head())

# # COMENTARIO J (Justificación F):
# # Se aíslan las transacciones del Top 10% para segmentar clientes de alto valor sin alterar el dataset original.


# =============================================================================
# SECCIÓN G: Detección de outliers (COMPLETA, SIN INCISO 2)
# =============================================================================
print("\n--- SECCIÓN G: Detección de Outliers ---")

# G.1 Detectar outliers numéricos con IQR
variables_outliers = ['total_venta', 'edad', 'precio_unitario', 'dias_entrega']
outliers_dict = {}

for col in variables_outliers:
    if col in df.columns:
        serie_num = pd.to_numeric(df[col], errors='coerce')
        Q1 = serie_num.quantile(0.25)
        Q3 = serie_num.quantile(0.75)
        IQR = Q3 - Q1
        limite_inf = Q1 - 1.5 * IQR
        limite_sup = Q3 + 1.5 * IQR
        
        mascaras_outliers = (serie_num < limite_inf) | (serie_num > limite_sup)
        outliers_dict[col] = serie_num[mascaras_outliers]
        print(f"G.1 - Outliers en '{col}': {mascaras_outliers.sum()} registros detectados.")

# G.3 Buscar outliers por grupo
if 'categoria_producto' in df.columns and 'cantidad' in df.columns:
    print("\nG.3 - Outliers por grupo (Cantidad por Categoría):")
    cant_num = pd.to_numeric(df['cantidad'], errors='coerce')
    df_g3 = df.assign(cantidad_num=cant_num).dropna(subset=['cantidad_num', 'categoria_producto'])
    
    def detect_group_outliers(group):
        Q1 = group.quantile(0.25)
        Q3 = group.quantile(0.75)
        IQR = Q3 - Q1
        return group[(group < Q1 - 1.5 * IQR) | (group > Q3 + 1.5 * IQR)]
    
    outliers_grupo = df_g3.groupby('categoria_producto')['cantidad_num'].apply(detect_group_outliers)
    print(f"Se detectaron {len(outliers_grupo)} compras con cantidades atípicas para su categoría.")

# G.4 Outliers temporales usando fecha_venta
if 'fecha_venta_limpia' in df.columns and 'total_venta' in df.columns:
    print("\nG.4 - Outliers temporales (Ventas diarias atípicas):")
    total_venta_num = pd.to_numeric(df['total_venta'], errors='coerce')
    df_temp = df.assign(total_venta_num=total_venta_num).dropna(subset=['fecha_venta_limpia', 'total_venta_num'])
    
    ventas_diarias = df_temp.groupby(df_temp['fecha_venta_limpia'].dt.date)['total_venta_num'].sum()
    
    Q1_t = ventas_diarias.quantile(0.25)
    Q3_t = ventas_diarias.quantile(0.75)
    IQR_t = Q3_t - Q1_t
    limite_sup_temp = Q3_t + 1.5 * IQR_t
    
    outliers_temp = ventas_diarias[ventas_diarias > limite_sup_temp]
    print(f"Días con ventas totales inusualmente altas (> ${limite_sup_temp:.2f}): {len(outliers_temp)} días.")

# G.5 Casos multivariados sospechosos
if 'ingreso_mensual_cliente' in df.columns and 'total_venta' in df.columns:
    print("\nG.5 - Casos multivariados sospechosos:")
    ingreso_num = pd.to_numeric(df['ingreso_mensual_cliente'], errors='coerce')
    venta_num = pd.to_numeric(df['total_venta'], errors='coerce')
    sospechosos = df[(venta_num > (ingreso_num * 0.5)) & (ingreso_num > 0)]
    print(f"Se detectaron {len(sospechosos)} registros donde la compra supera el 50% del ingreso mensual del cliente.")

# # COMENTARIO J (Justificación G.6):
# # Diferenciación de outliers:
# # - Error puro: Precios negativos o días de entrega < 0 (deben corregirse/eliminarse).
# # - Observación extrema válida: Ventas muy elevadas en G.5 (clientes mayoristas o compras corporativas).
# # - Valor contextual: Picos atípicos en G.4 asociados a eventos comerciales (Buen Fin / Navidad).


# =============================================================================
# SECCIÓN H: Tratamiento de outliers (Múltiples estrategias)
# =============================================================================
print("\n--- SECCIÓN H: Tratamiento de Outliers ---")

# H.3 Crear columna bandera
serie_venta = pd.to_numeric(df['total_venta'], errors='coerce')
Q1_v = serie_venta.quantile(0.25)
Q3_v = serie_venta.quantile(0.75)
lim_sup_v = Q3_v + 1.5 * (Q3_v - Q1_v)

df['flag_outlier_venta'] = (serie_venta > lim_sup_v).astype(int)

# H.1 y H.2: Estrategia 1 (Winsorizar total_venta)
df['total_venta_tratada'] = serie_venta.clip(upper=lim_sup_v)

# H.1 y H.2: Estrategia 2 (Eliminar errores de precio_unitario <= 0)
serie_precio = pd.to_numeric(df['precio_unitario'], errors='coerce')
df_limpio_h = df[serie_precio > 0].copy()

# # COMENTARIO J (Justificación H):
# # 1. Problema: Outliers extreman la media y la desviación estándar global.
# # 2. Por qué es un problema: 'total_venta' tiene valores muy altos válidos, pero 'precio_unitario' <= 0 son errores técnicos.
# # 3. Información perdida: En 'total_venta' se winsoriza (se conserva el registro ajustando el tope), evitando perder clientes VIP. En 'precio_unitario' se eliminan las filas corruptas inaccesibles.


# =============================================================================
# SECCIÓN J: Comparación antes vs después (Exportación a Excel)
# =============================================================================
print("\n--- SECCIÓN J: Comparación Antes vs Después ---")

# J.2 y J.3 Tabla comparativa exportada a Excel (Sin correlaciones)
tabla_comparativa = pd.DataFrame({
    'Métrica': ['Media', 'Mediana', 'Desviación Estándar', 'IQR'],
    'Edad_Antes': calcular_estadisticas(edad_nulos),
    'Edad_Despues_Imp': calcular_estadisticas(df['edad_imputada']),
    'Venta_Antes': calcular_estadisticas(serie_venta),
    'Venta_Despues_Winsorizada': calcular_estadisticas(df['total_venta_tratada'])
})

# Exportar las tablas a Excel según las indicaciones del profesor
nombre_excel = "Tablas_Comparativas_SeccionJ.xlsx"
tabla_comparativa.round(2).to_excel(nombre_excel, index=False)
print(f"Tabla comparativa antes/después exportada a '{nombre_excel}'")

# # COMENTARIO J.4 (Discusión general de cambios):
# # - Qué cambió por limpieza: La conversión de fechas a datetime eliminó inconsistencias de formato de texto.
# # - Qué cambió por imputación: La mediana de edad se mantuvo constante, permitiendo usar el 100% de los registros con menor varianza.
# # - Qué cambió por outliers: Al winsorizar 'total_venta', se estabilizó la media y se redujo drásticamente la desviación estándar sin eliminar observaciones.


# =============================================================================
# SECCIÓN K: Cierre y Documentación
# =============================================================================
print("\n--- SECCIÓN K: Cierre y Conclusiones ---")
print("""
HALLAZGOS DE NEGOCIO (K.2):
1. Existe una concentración de ingresos anómala en el top 10% de las ventas.
2. Algunas categorías de productos presentan cantidades de compra atípicas, sugiriendo compras al por mayor.
3. Se detectaron clientes cuyas compras superan el 50% de su ingreso mensual declarado.
4. Existen picos estacionales fuertes (outliers temporales) donde las ventas diarias se disparan fuera del límite superior.
5. Las inconsistencias en fechas y precios negativos indican que el sistema de captura de ventas carece de validaciones de entrada en punto de venta.

DECISIONES PARA MODELOS PREDICTIVOS (K.3):
1. Imputación: En lugar de usar la mediana global para 'edad', usaría KNN-Imputer o un modelo de regresión para mantener la varianza multivariada.
2. Tratamiento de Outliers: No winsorizaría 'total_venta' si el objetivo del modelo fuera predecir qué clientes tienen potencial de hacer compras masivas (VIPs).
3. Variables derivadas: Codificaría las variables categóricas con One-Hot Encoding o Target Encoding para algoritmos de Machine Learning.

PREVENCIÓN DE FUGA DE INFORMACIÓN (K.4):
Cualquier cálculo que dependa de la distribución de los datos (límites IQR, media o mediana) debe calcularse ÚNICAMENTE con los datos de entrenamiento (X_train) y luego aplicarse a los datos de prueba (X_test).
""")


# =============================================================================
# EXPORTAR LA BASE DE DATOS LIMPIA
# =============================================================================
print("\n--- Exportando Base de Datos Limpia ---")

# Exportamos el dataframe final (df_limpio_h) a un archivo de Excel
nombre_archivo_salida = "Base_Datos_Limpia.xlsx"
df_limpio_h.to_excel(nombre_archivo_salida, index=False)

print(f"¡Listo! La base de datos ya procesada se guardó como '{nombre_archivo_salida}' en tu carpeta.")

