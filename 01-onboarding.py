import streamlit as st
import requests
import pandas as pd
import scipy

st.set_page_config(
    page_title="Ejemplos MBIT School",
    page_icon="chart_with_upwards_trend",
    #layout="wide",
    )

#Textos en cuerpo principal
st.title("Título")
st.header("Cabecera")
st.subheader ("Subcabecera")
st.write("Texto normal")
st.markdown("Texto en formato **markdown**")
st.success (" Mensaje de exito")
st.info ("Mensaje de información")
st.warning("Mensaje de advertencia")
st.error("Mensaje de error")


#Añadir textos en la barra lateral
st.sidebar.title("Título")
st.sidebar.header("Cabecera")
st.sidebar.subheader ("Subcabecera")
st.sidebar.write("Texto normal")
st.sidebar.success (" Mensaje de exito")
st.sidebar.info ("Mensaje de información")
st.sidebar.warning("Mensaje de advertencia")
st.sidebar.error("Mensaje de error")

######### IMÁGENES
st.image("https://static.streamlit.io/examples/cat.jpg")

######### CREACIÓN DE COLUMNAS
import streamlit as st
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Gato")
    st.image("https://static.streamlit.io/examples/cat.jpg")
    # Contenido columna 1
with col2:
    st.header("Perro")
    st.image("https://static.streamlit.io/examples/dog.jpg")
    # Contenido columna 2
with col3:
    st.header("Buho")
    st.image("https://static.streamlit.io/examples/owl.jpg")
    # Contenido columna 3

######### CREACIÓN DE TABULADORES
import streamlit as st

tab1, tab2, tab3 = st.tabs(["Gato", "Perro", "Buho"])

with tab1:
    st.header("Gato")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with tab2:
    st.header("Perro")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with tab3:
    st.header("Buho")
    st.image("https://static.streamlit.io/examples/owl.jpg")


#######  EXPANDER

import streamlit as st

with st.expander("Jugar al dado"):
    st.markdown("""
            Tras lanzar este dado varias veces,
            estos son los resultados del mismo.
            Prueba tu a lanzar el dado y **superalo**
            """)
    st.image("https://static.streamlit.io/examples/dice.jpg")
    st.bar_chart({"data": [1,5,2,6,2,1]})

##################################################
#INTERACCIÓN CON EL USUARIO - ELEMENTOS DE DATOS #
##################################################

#### DATAFRAME
import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(df)


### DATA EDITOR
import streamlit as st
import pandas as pd

df = pd.DataFrame(
    [
        {"pelicula": "Matrix 1", "rating": 5, "visto": True},
        {"pelicula": "Matrix 2", "rating": 3, "visto": True},
        {"pelicula": "Matrix 3", "rating": 4, "visto": False},
    ])

edited_df = st.data_editor(df)
pelicula_favorita = edited_df.loc[edited_df["rating"].idxmax()]["pelicula"]
st.markdown(f"Tu pelicula favorita es **{pelicula_favorita}** 👏")


###  BOTONES 
import streamlit as st

# if st.button("Saluda"):
#     st.write("Hey, ¡hola!")
# else:
#     st.write("¡Adios!")

#Botón con ÑaaS evaluando su estado
st.button("Reset")
if st.button("Saluda"):
    st.write("Hey, ¡hola!")
else:
    st.write("¡Adios!")

#### SELECTORES
import streamlit as st

#Variante con botones de radio
options = st.radio(
    'Cuáles son tus colores favoritos',
    ['Verde', 'Azul', 'Amarillo', 'Rojo']
)
st.write('Has seleccionado:', options)

#Variante con selectbox
options2 = st.selectbox(
    'Cuáles son tus colores favoritos',
    ['Verde', 'Azul', 'Amarillo', 'Rojo']
)
st.write('Has seleccionado:', options2)

#Variante con slider
options3 = st.select_slider(
    'Cuáles son tus colores favoritos',
    ['Verde', 'Azul', 'Amarillo', 'Rojo']
)
st.write('Has seleccionado:', options3)

#Multiselector
options4 = st.multiselect(
    'Cuáles son tus colores favoritos',
    ['Verde', 'Azul', 'Amarillo', 'Rojo'],
    ['Azul','Verde']
)
st.write('Has seleccionado:', options4)


## Añadimos opciones en la barra lateral
#Using selectbox notation
add_selectbox = st.sidebar.selectbox('¿Qué forma de pago desea?', ('Tarjeta','Bizum', 'Transferencia bancaria'))

#Using "with" notation
with st.sidebar:
    add_radio = st.radio('Elige un método de envío', ('Estándar (3-5 días)','Express (1-2 días)'))

### Widgets de entrada
import streamlit as st

number = st.number_input('Introduce un número', step=1)
st.write('El número actual es', number)

title = st.text_input("Título de la pelicula", "Matrix")
st.write("El título de la película es", title)

title_todas = st.text_area("Cuenta todas las películas", "Matrix")
st.write("El título de la película es", title_todas)

### Subida de ficheros
import streamlit as st

ficheros_a_subir = st.file_uploader("Elije uno o varios ficheros CSV", accept_multiple_files=True)

for fichero in ficheros_a_subir:
        st.write(fichero.name)
        st.dataframe(pd.read_csv(fichero))

# Cargar archivo
#uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])
#
#if uploaded_file is not None:
#    # Leer el archivo CSV en un DataFrame de pandas
#    try:
#        df = pd.read_csv(uploaded_file)
#        st.success("Archivo cargado exitosamente!")
#        
#        # Mostrar el DataFrame
#        st.write("Vista previa del archivo:")
#        st.dataframe(df)
#        
#        # Opcional: información adicional del DataFrame
#        st.write("Información del DataFrame:")
#        st.write(df.info())
#       
#        st.write("Descripción estadística:")
#        st.write(df.describe())
#    except Exception as e:
#        st.error(f"Error al leer el archivo: {e}")

### Date input
import datetime
import streamlit as st

dia_bitcoin = st.date_input(
    "¿En qué fecha apareció la primera criptomoneda, el Bitcoin?",
    datetime.date(2000,1,1))
if dia_bitcoin == datetime.date(2008,10,31):
        st.write('¡Es correcto! 👏')
elif dia_bitcoin > datetime.date(2008,10,31):
        st.write("Fue antes! ⏪")
elif dia_bitcoin < datetime.date(2008,10,31):
        st.write("Fue más tarde ⏩")
#else:
#    st.write("¡Incorrecto! ❌")

### Imagenes
import streamlit as st
st.image("https://i.imgur.com/vppXpob.png", use_container_width=True, caption="MBIT Data School")

### Audios
import streamlit as st
import requests
st.audio("https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/25.ogg")
st.audio(requests.get("https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/25.ogg").content)

### Videos
import streamlit as st
import requests
st.video("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", muted=True, start_time=10)


### Spinner
import time
with st.spinner("Cargando datos...",show_time=True):
    time.sleep(2)
    st.success("Done!")
    st.button("Rerun")

######################
#   VISUALIZACIÓN    #
######################
# Diagrama de líneas

import streamlit as st
import pandas as pd
import numpy as np

datos_grafica = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a','b','c'])

st.line_chart(datos_grafica)

#diagrama de barras
import streamlit as st
import pandas as pd
import numpy as np

datos_grafica = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a','b','c'])

st.bar_chart(datos_grafica)

## Mapas
import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(300 , 2) / [-3.8, 42] + [40.4, -3.7], columns=['lat','lon'])
st.map(df)


# Visualización de terceros: Altair
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

datos_grafica = pd.DataFrame(np.random.randn(20, 3), columns=['a','b','c'])
c = alt.Chart(datos_grafica).mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
st.altair_chart(c, use_container_width=True)

# Visualización de terceros: Plotly
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
#Creamos histograma
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2
#Agrupa datos
hist_data = [x1, x2, x3]
group_labels = ["Grupo 1", "Grupo 2", "Grupo 3"]
#Crea distplot con tamaño personalizado
fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, -24, .5])
#Muestra en Streamlit
st.plotly_chart(fig, use_container_width=True)


#Visualización matplotlib - Diagrama de tarta
import matplotlib.pyplot as plt

labels = 'Coche', 'Moto', 'Bicicleta', 'Transporte público'
sizes = [15, 30, 45, 10]

fig, ax = plt.subplots()
tarta = ax.pie(sizes, labels=labels)

st.pyplot(fig)


#Visualización matplotlib - Histograma
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)
st.pyplot(fig)