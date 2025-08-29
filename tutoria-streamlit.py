import streamlit as st
import requests
import pandas as pd
import scipy

#Menú lateral
st.sidebar.image("https://i.imgur.com/HKlOSPA.png")
ejercicio =  st.sidebar.radio('Ejercicio', ["1","2"])

########################
#      EJERCICIO 1     #
# Explorador de países #
########################

if ejercicio == "1":
    st.header("Ejercicio 1 - Explorador de Países")

    # Título
    st.title("Explorador de Países con REST Countries API")

    # Descripción
    st.markdown("""
    Esta aplicación interactiva utiliza la API pública [REST Countries](https://restcountries.com) 
    para mostrar información sobre países. Usa los filtros para explorar los datos.
    """)

    # Obtener datos de la API
    @st.cache_data
    def obten_paises():
        #url = "https://restcountries.com/v3.1/all"
        url = "https://restcountries.com/v3.1/all?fields=name,region,population,capital,languages,area,flags"
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al obtener los datos de la API.")
            return []

    # Transformar datos en un DataFrame para facilitar el análisis
    def procesar_paises(datos):
        countries = []
        for country in datos:
            countries.append({
                "Nombre": country.get("name", {}).get("common", ""),
                "Región": country.get("region", ""),
                "Población": country.get("population", 0),
                "Capital": ", ".join(country.get("capital", [])),
                "Idiomas": ", ".join(country.get("languages", {}).values()) if country.get("languages") else "",
                "Área (km²)": country.get("area", 0),
                "Bandera": country.get("flags", {}).get("png", ""),
            })
        return pd.DataFrame(countries)

    # Obtenemos datos de la API
    datos = obten_paises()
    df = procesar_paises(datos)

    # Filtros interactivos
    st.sidebar.header("Filtros")
    min_population = st.sidebar.slider("Población mínima:", min_value=0, max_value=int(df["Población"].max()-1), value=0)
    max_population = st.sidebar.slider("Población máxima:", min_value=min_population, max_value=int(df["Población"].max()), value=int(df["Población"].max()))
    #region = st.sidebar.selectbox("Selecciona una región:", ["Todas"] + df["Región"].unique().tolist())
    # language = st.sidebar.text_input("Idioma (ej. Spanish, English):").strip().lower()

    # Aplicar filtros
    filtered_df = df.copy()

    # if region != "Todas":
    #     filtered_df = filtered_df[filtered_df["Región"] == region]

    filtered_df = filtered_df[
        (filtered_df["Población"] >= min_population) & 
        (filtered_df["Población"] <= max_population)
    ]

    # if language:
    #     filtered_df = filtered_df[filtered_df["Idiomas"].str.lower().str.contains(language)]

    # Mostrar resultados
    st.subheader("Resultados")
    st.write(f"Mostrando {len(filtered_df)} país(es)")

    # Tabla con imágenes en miniatura
    st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Bandera": st.column_config.ImageColumn("Vista previa")
                    }
                )

    # Mostrar detalles de un país seleccionado
    selected_country = st.selectbox("Selecciona un país para ver más detalles:", [""] + filtered_df["Nombre"].tolist())

    if selected_country:
        country_details = filtered_df[filtered_df["Nombre"] == selected_country].iloc[0]
        st.markdown(f"### Detalles de {selected_country}")
        st.markdown(f"**Región:** {country_details['Región']}")
        st.markdown(f"**Población:** {country_details['Población']}")
        st.markdown(f"**Capital:** {country_details['Capital']}")
        st.markdown(f"**Idiomas:** {country_details['Idiomas']}")
        st.markdown(f"**Área:** {country_details['Área (km²)']} km²")
        st.image(country_details["Bandera"], width=200)

############################
#      EJERCICIO 2         #
# Generador de identidades #
############################

if ejercicio == "2":
    st.header("Ejercicio 2 - Generador de Identidades")

    def random_persona(contador):
        identidades = []
        fotografias = []
        for i in range(0, contador):
            identidades.append(requests.get("https://api.namefake.com").json())
            fotografias.append(requests.get("https://thispersondoesnotexist.com").content)
        return identidades, fotografias

    contador = st.number_input("Número de personas a generar", min_value=1, max_value=50, step=1)


    identidades, fotografias = random_persona(contador)

    for i in range(0, contador):
        col1, col2 = st.columns(2)
        with col1:
            st.image(fotografias[i])
        with col2:
            st.write(f"**Nombre:** {identidades[i]['name']}")
            st.write(f"**Dirección:** {identidades[i]['address']}")
            st.write(f"**Teléfono:** {identidades[i]['phone_h']}")
            st.write(f"**Email:** {identidades[i]['email_u']}")


    personas_data = []
    for i in range(len(identidades)):
        persona = identidades[i].copy() 
        persona['fotografia_bytes'] = fotografias[i]
        personas_data.append(persona)
    
    df = pd.DataFrame(personas_data)


    import sqlite3
    conexion = sqlite3.connect('personas.sqlite')
    df.to_sql('personas', conexion, if_exists='replace', index=False)