import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import seaborn as sns

st.set_page_config(layout="wide")

df = pd.read_csv('df/tele.csv', delimiter=',', encoding='utf-8')

st.title("📱 Análisis Exploratorio: Dataset de Teléfonos")


with st.expander("📊 Ver Datos"):
    st.write(df)


st.sidebar.header("Filtros")
marca_telefono = st.sidebar.selectbox("Seleccionar una Marca", options=df["marca_telefono"].dropna().unique())
modelos = df[df["marca_telefono"] == marca_telefono]["modelo_telefono"].dropna().unique()
modelo_telefono = st.sidebar.selectbox("Seleccionar un Modelo", options=modelos)


df_filtered = df[(df["marca_telefono"] == marca_telefono) & (df["modelo_telefono"] == modelo_telefono)]


#INSIGTHS
celular_mayor_precio = df.loc[df["precio_usd"].idxmax()]
celular_mayor_bateria = df.loc[df["bateria"].idxmax()]

if not df_filtered.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Celular con el Mayor Precio")
        with st.expander(f"Modelo: {celular_mayor_precio['modelo_telefono']}"):
            st.markdown(f"""
            - **Marca:** {celular_mayor_precio['marca_telefono']}
            - **Modelo:** {celular_mayor_precio['modelo_telefono']}
            - **Precio (USD):** {celular_mayor_precio['precio_usd']}
            - **Batería (mAh):** {celular_mayor_precio['bateria']}
            - **Almacenamiento (GB):** {celular_mayor_precio['almacenamiento']}
            """)

    with col2:
        st.subheader("🔋 Celular con Mayor Batería")
        with st.expander(f"Modelo: {celular_mayor_bateria['modelo_telefono']}"):
            st.markdown(f"""
            - **Marca:** {celular_mayor_bateria['marca_telefono']}
            - **Modelo:** {celular_mayor_bateria['modelo_telefono']}
            - **Batería (mAh):** {celular_mayor_bateria['bateria']}
            - **Precio (USD):** {celular_mayor_bateria['precio_usd']}
            - **Almacenamiento (GB):** {celular_mayor_bateria['almacenamiento']}
            """)
else:
    st.warning("No hay datos disponibles para la combinación seleccionada.")


#PRECIO PROMEDIO
    st.subheader("📊 Precio Promedio por Tienda")
precio_promedio_tienda = df.groupby("tienda")["precio_usd"].mean().reset_index()
fig_tienda = px.bar(
    precio_promedio_tienda,
    x="tienda",
    y="precio_usd",
    title="Precio Promedio por Tienda",
    labels={"precio_usd": "Precio Promedio (USD)", "tienda": "Tienda"},
    template="plotly_white"
)
st.plotly_chart(fig_tienda)


# Eliminar duplicados basados en modelo y precio para garantizar modelos únicos
df_unique = df.drop_duplicates(subset=["modelo_telefono", "precio_usd"])

# Seleccionar los 5 modelos más caros (únicos)
top_5_caros = df_unique.nlargest(5, "precio_usd")[["marca_telefono", "modelo_telefono", "precio_usd", "bateria", "almacenamiento"]]

# Mostrar los resultados en un dataframe interactivo
st.subheader("💎 Top 5 Modelos Más Caros")
st.dataframe(top_5_caros)





#TIENDAS
if not df_filtered.empty:
    st.subheader(f"🏬 Tiendas donde está disponible el {modelo_telefono} de {marca_telefono}")

    tiendas_disponibles = df_filtered.groupby("tienda").size().reset_index(name="cantidad")


    st.write("🏪 Tabla de Tiendas:")
    st.dataframe(tiendas_disponibles)

    fig = px.bar(
        tiendas_disponibles,
        x="tienda",
        y="cantidad",
        title=f"Distribución de Tiendas para {modelo_telefono} ({marca_telefono})",
        labels={"tienda": "Tienda", "cantidad": "Cantidad Disponible"},
        template="plotly_white"
    )
    st.plotly_chart(fig)

else:
    st.warning("No hay datos disponibles para la combinación seleccionada.")





if not df_filtered.empty:
    caracteristicas = df_filtered.iloc[0]  
    with st.expander(f"📋 Características del {modelo_telefono}"):
        st.write("### Especificaciones")
        st.markdown(f"""
        - **Marca**: {caracteristicas['marca_telefono']}
        - **Modelo**: {caracteristicas['modelo_telefono']}
        - **Tienda**: {caracteristicas['tienda']}
        - **Precio (USD)**: {caracteristicas['precio_usd']}
        - **Almacenamiento (GB)**: {caracteristicas['almacenamiento']}
        - **RAM (GB)**: {caracteristicas['ram']}
        - **Fecha de Lanzamiento**: {caracteristicas['fecha_lanzamiento']}
        - **Dimensiones**: {caracteristicas['dimensiones']}
        - **Peso (g)**: {caracteristicas['peso']}
        - **Pantalla**: {caracteristicas['tipo_pantalla']}
        - **Resolución Pantalla**: {caracteristicas['resolucion_pantalla']}
        - **Sistema Operativo**: {caracteristicas['sistema operativo']}
        - **NFC**: {"Sí" if caracteristicas['nfc'] == 1 else "No"}
        - **USB**: {caracteristicas['usb']}
        - **Batería (mAh)**: {caracteristicas['bateria']}
        - **Colores Disponibles**: {caracteristicas['colores']}
        - **Resolución de Video**: {caracteristicas['resolucion_video']}
        - **Chipset**: {caracteristicas['chipset']}
        - **CPU**: {caracteristicas['cpu']}
        - **GPU**: {caracteristicas['gpu']}
        - **Densidad de PPI**: {caracteristicas['densidad ppi']}
        - **Rango de Precio**: {caracteristicas['rango_precio']}
        """)

else:
    st.warning("No hay datos disponibles para la combinación seleccionada.")



#COLORES POR CELULARES
# Verificar si hay datos después del filtro
# Verificar si hay datos después del filtro
if not df_filtered.empty:
    # Separar los colores por comas y expandirlos
    df_filtered['colores'] = df_filtered['colores'].str.split(', ')
    df_exploded = df_filtered.explode('colores')

    # Contar la cantidad de teléfonos por color
    colores_count = df_exploded["colores"].value_counts().reset_index()
    colores_count.columns = ["colores", "cantidad"]

    # Crear gráfico de torta
    st.subheader("🎨 Distribución de Colores de Teléfonos")
    fig = px.pie(
        colores_count,
        names="colores",
        values="cantidad",
        title=f"Distribución de Colores para {modelo_telefono} ({marca_telefono})",
        labels={"colores": "Colores", "cantidad": "Cantidad"},
        template="plotly_white"
    )
    st.plotly_chart(fig)

else:
    st.warning("No hay datos disponibles para la combinación seleccionada.")







if not df_filtered.empty:

    fig = px.scatter(
        df_filtered,
        x="almacenamiento",
        y="precio_usd",
        title=f"Relación entre Almacenamiento y Precio para {modelo_telefono} ({marca_telefono})",
        labels={"almacenamiento": "Almacenamiento (GB)", "precio_usd": "Precio (USD)"},
        size="ram", 
        color="bateria",  
        hover_name="tienda",  
        template="plotly_white"
    )
    st.plotly_chart(fig)

else:
    st.warning("No hay datos disponibles para la combinación seleccionada.")




#Graficos dinamicosss
if not df_filtered.empty:
    st.subheader(f"Gráficos dinámicos para {modelo_telefono} de {marca_telefono}")

   
    st.subheader("Relación entre Precio y RAM")
    fig1 = px.scatter(
        df_filtered,
        x='ram',
        y='precio_usd',
        size='almacenamiento',  
        color='bateria',  
        title='Precio vs. RAM',
        labels={'ram': 'RAM (GB)', 'precio_usd': 'Precio (USD)', 'almacenamiento': 'Almacenamiento (GB)'},
        template='plotly_white'
    )
    st.plotly_chart(fig1)

 

 


# 3a. Gráfico de dispersión


df_filtered_by_marca = df[df["marca_telefono"] == marca_telefono]

st.subheader(f"💵 Gráfico de Dispersión entre Precio, RAM y Almacenamiento de{marca_telefono}")

fig_scatter = px.scatter(
    df_filtered_by_marca,
    x="ram",
    y="precio_usd",
    size="almacenamiento",
    color="modelo_telefono",  
    title=f"Relación entre Precio (USD) y RAM con Almacenamiento para {marca_telefono}",
    labels={"ram": "RAM (GB)", "precio_usd": "Precio (USD)", "almacenamiento": "Almacenamiento (GB)"},
    hover_data=["modelo_telefono"],  
    template="plotly_white"
)

st.plotly_chart(fig_scatter)





st.subheader("📊 Popularidad de Sistemas Operativos y Tipos de Pantalla")

# Sistemas Operativos
so_count = df["sistema operativo"].value_counts().reset_index()
so_count.columns = ["Sistema Operativo", "Cantidad"]

# Gráfico para sistemas operativos
fig_so = px.bar(
    so_count,
    x="Sistema Operativo",
    y="Cantidad",
    color="Sistema Operativo",
    title="Distribución de Sistemas Operativos",
    labels={"Sistema Operativo": "Sistema Operativo", "Cantidad": "Cantidad"},
    template="plotly_white"
)

st.plotly_chart(fig_so)

# Tipos de Pantalla
pantalla_count = df["tipo_pantalla"].value_counts().reset_index()
pantalla_count.columns = ["Tipo de Pantalla", "Cantidad"]

# Gráfico para tipos de pantalla
fig_pantalla = px.bar(
    pantalla_count,
    x="Tipo de Pantalla",
    y="Cantidad",
    color="Tipo de Pantalla",
    title="Distribución de Tipos de Pantalla",
    labels={"Tipo de Pantalla": "Tipo de Pantalla", "Cantidad": "Cantidad"},
    template="plotly_white"
)

st.plotly_chart(fig_pantalla)





st.subheader(f"📊 Popularidad de Sistemas Operativos y Tipos de Pantalla para {marca_telefono}")

# Filtrar el DataFrame por la marca seleccionada
df_filtered_by_marca = df[df["marca_telefono"] == marca_telefono]

# Sistemas Operativos
so_count = df_filtered_by_marca["sistema operativo"].value_counts().reset_index()
so_count.columns = ["Sistema Operativo", "Cantidad"]

# Gráfico para sistemas operativos
fig_so = px.bar(
    so_count,
    x="Sistema Operativo",
    y="Cantidad",
    color="Sistema Operativo",
    title=f"Distribución de Sistemas Operativos para {marca_telefono}",
    labels={"Sistema Operativo": "Sistema Operativo", "Cantidad": "Cantidad"},
    template="plotly_white"
)

st.plotly_chart(fig_so)

# Tipos de Pantalla
pantalla_count = df_filtered_by_marca["tipo_pantalla"].value_counts().reset_index()
pantalla_count.columns = ["Tipo de Pantalla", "Cantidad"]

# Gráfico para tipos de pantalla
fig_pantalla = px.bar(
    pantalla_count,
    x="Tipo de Pantalla",
    y="Cantidad",
    color="Tipo de Pantalla",
    title=f"Distribución de Tipos de Pantalla para {marca_telefono}",
    labels={"Tipo de Pantalla": "Tipo de Pantalla", "Cantidad": "Cantidad"},
    template="plotly_white"
)

st.plotly_chart(fig_pantalla)


# 3c. Heatmap de correlación
st.subheader("🔍 Matriz de Correlación entre Variables Numéricas")
numerical_cols = df.select_dtypes(include=["float64", "int64"]).columns
if len(numerical_cols) > 0:
    correlation_matrix = df[numerical_cols].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax)
    plt.title("Heatmap de Correlación")
    st.pyplot(fig)
else:
    st.warning("No se encontraron columnas numéricas para generar la correlación.")

# 4. Interpretación de Resultados
st.subheader("📌 Interpretación de Resultados")
st.markdown("""
1. **Gráfico de Dispersión:** Permite analizar cómo varía el precio en función de la RAM y el almacenamiento, mostrando las diferencias entre marcas.
2. **Gráficos de Barras:** Identifican las preferencias del mercado para sistemas operativos y tipos de pantalla.
3. **Matriz de Correlación:** Ayuda a identificar relaciones significativas entre las especificaciones numéricas de los teléfonos.
""")


# Agrupar por año y contar lanzamientos
lanzamientos_por_año = df.groupby('año').size().sort_index()

# Generar gráfico
plt.figure(figsize=(10, 6))
plt.plot(lanzamientos_por_año.index, lanzamientos_por_año.values, marker='o', linestyle='-', linewidth=2)
plt.title('Tendencias de Lanzamiento por Año', fontsize=14)
plt.xlabel('Año de Lanzamiento', fontsize=12)
plt.ylabel('Número de Modelos Lanzados', fontsize=12)
plt.grid(visible=True, linestyle='--', alpha=0.7)

# Renderizar en Streamlit
st.pyplot(plt)