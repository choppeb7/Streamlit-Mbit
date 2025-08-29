import streamlit as st
import requests
import pandas as pd
import scipy

#Menú lateral
st.sidebar.image("https://i.imgur.com/HKlOSPA.png")
ejercicio =  st.sidebar.radio('Ejercicio', ["1","2","3","4","5","6","11","12"])

######################
#    EJERCICIO 1     #
# GEOLOCALIZACIÓN IP #
######################
if ejercicio == "1":

    st.title("Ejercicio 1")
    st.header("Geoposicionamiento IP", divider=True)
    direccion_ip = requests.get("http://ifconfig.me")
    localizacion = requests.get(f"http://ip-api.com/json/{direccion_ip.text}")

    #Muestra la dirección IP capturada
    st.write(f"**Tu dirección es:** {direccion_ip.text}")    

    #Crea Dataframe con los datos
    st.write("Dataframe con datos")
    df2 = pd.DataFrame([localizacion.json()])
    st.dataframe(df2) 

    #Crea Mapa
    st.subheader("Mapa 🌍")
    df = pd.DataFrame({"lat": [localizacion.json()['lat']], "lon": [localizacion.json()['lon']] })
    st.map(df)
    # Muestra la ciudad que ha identificado
    st.write(f"Tu ciudad es: {localizacion.json()['city']}")
    # Muestra el json
    st.write(localizacion.json())

######################
#    EJERCICIO 2     #
#      POKEDEX       #
######################
if ejercicio == "2":
    max_pokemon=30

    # Función para obtener datos de un Pokémon, cacheada
    @st.cache_data
    def obtener_datos_pokemon(numero_pokemon):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{numero_pokemon}/")
        return response.json()

    def actualizar_datos(df_editado):
        # Solo actualiza si hay cambios
        if not st.session_state["df_data"].equals(df_editado):
            st.session_state["df_data"] = df_editado
            st.success("Datos actualizados correctamente!")

    # Inicializa los datos en `session_state` si no existen
    if "df_data" not in st.session_state:
        df_data=[]
        for i in range(1, max_pokemon+1):
            data = obtener_datos_pokemon(i)
            df_data.append({"id": data["id"], "nombre": data["name"], "imagen": data["sprites"]["front_default"], "visto": False })
        st.session_state["df_data"] = pd.DataFrame(df_data)

    # Interfaz principal
    st.header("Ejercicio 2")
    st.title("Pokédex")
    st.sidebar.subheader("Pokémon")

    #Ñaas Centrar Imagen
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/1024px-International_Pok%C3%A9mon_logo.svg.png",caption="Pokémon",width=200)
    numero_pokemon = st.sidebar.number_input(f"Introduce el número del Pokémon (Número máximo configurado {max_pokemon})", min_value=1, max_value=max_pokemon, step=1)

    # Obtener datos de un Pokémon específico
    pokemon = obtener_datos_pokemon(numero_pokemon)

    if pokemon:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Datos")
            st.write(f"**Nombre:** {pokemon['name']}")
            st.write(f"**Altura:** {pokemon['height']}")
            st.write(f"**Peso:** {pokemon['weight'] / 10} kg")
            st.write(f"**Experiencia base:** {pokemon['base_experience']}")

        with col2:
            st.header("Aspecto")
            st.image(pokemon["sprites"]["front_default"], use_container_width=True)
            st.audio(pokemon["cries"]["latest"])

        with col3:
            st.header("Habilidades")
            for ability in pokemon["abilities"]:
                st.write(f"_{ability['ability']['name']}_")


        # Interfaz principal con pestañas
        tab1, tab2 = st.tabs(["Todos los Pokemon", "Restaurar copia de seguridad"])

        # Pestaña 1: Carga de archivo CSV
        with tab1:
            st.header("Todos los pokemon")
            # Editor de datos dinámico basado en session_state
            df_editado = st.data_editor(
                st.session_state["df_data"],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "imagen": st.column_config.ImageColumn("Vista previa"),
                    "id": st.column_config.Column(disabled=True),
                    "nombre": st.column_config.Column(disabled=True),
                    "visto": st.column_config.CheckboxColumn("Visto")
                },
                key="pokedex_editor"
            )
            # Botón para guardar cambios, con key único
            guardar = st.button("Guardar cambios en la Pokédex", key="guardar_pokedex")
            if guardar:
                actualizar_datos(df_editado)
                # Mantener el valor seleccionado tras guardar
                st.rerun()
            st.write(f"Has visto un total de **{st.session_state['df_data']['visto'].sum()}** Pokémon")

        # Pestaña 2: Restaurar copia de seguridad
        with tab2:
            st.header("Carga de archivo CSV")
            st.write("Carga un archivo CSV para sobrescribir los datos actuales.")
            uploaded_file = st.file_uploader("Carga un archivo CSV", type=["csv"])
            if uploaded_file:
                try:
                    # Leer el archivo CSV
                    new_data = pd.read_csv(uploaded_file)

                    # Validar columnas
                    if set(new_data.columns) == set(st.session_state["df_data"].columns):
                        st.session_state["df_data"] = new_data #Actualizamos
                        st.success("Datos cargados correctamente y actualizados.")
                        # Forzar actualización de widgets dependientes
                        st.session_state["_rerun_pokedex"] = True
                        st.rerun()  # Refrescar la tabla y la interfaz tras cargar el CSV
                    else:
                        st.error(f"Las columnas del CSV no coinciden. Se esperan: {list(st.session_state['df_data'].columns)}")
                except Exception as e:
                    st.error(f"Error al procesar el archivo CSV: {e}")

    # Forzar actualización de widgets dependientes tras cargar CSV
    if st.session_state.get("_rerun_pokedex", False):
        st.session_state["_rerun_pokedex"] = False

    col1, col2 = st.columns(2)

    with col1:
        st.header("Pokemon vistos")
        st.subheader(st.session_state['df_data']['visto'].sum())
    
    with col2:
        st.header("Pokemon total en pokedex")
        st.subheader(st.session_state["df_data"].shape[0])

#########  GRÁFICA PIE CHART
    import matplotlib.pyplot as plt
    st.header("% de progreso")
    data = {"labels": ["Visto", "No Visto"],"sizes": [st.session_state['df_data']['visto'].sum(),  st.session_state['df_data']['visto'].shape[0] - st.session_state['df_data']['visto'].sum()]}
    
    pie_chart_data = data
    plt.pie(pie_chart_data['sizes'], labels=pie_chart_data['labels'])
    st.pyplot( plt )

########################
#      EJERCICIO 3     #
# Explorador de países #
########################

if ejercicio == "3":
    st.header("Ejercicio 3")

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

    # Aplicar filtros
    filtered_df = df.copy()

    filtered_df = filtered_df[
        (filtered_df["Población"] >= min_population) & 
        (filtered_df["Población"] <= max_population)
    ]

    # Mostrar resultados
    st.subheader("Resultados")
    st.write(f"Mostrando {len(filtered_df)} país(es)")

    # Tabla interactiva
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

######################
#    EJERCICIO 4     #
#      TITANIC       #
######################

if ejercicio == "4":
    st.header("Ejercicio 4")

    ##### 1. Carga y exploración de datos
    st.title("Dataset del Titanic")
    st.subheader("Carga de Datos")

    data_url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(data_url)

    if st.checkbox("Mostrar datos"):
        st.dataframe(df.head())

    st.write("Resumen del dataset:")
    st.write(df.describe())

    ##### 2. Filtrado de datos
    st.sidebar.title("Filtros")
    gender = st.sidebar.selectbox("Selecciona género:", ["Todos", "male", "female"])
    if gender != "Todos":
        df = df[df["Sex"] == gender.lower()]

    class_filter = st.sidebar.multiselect("Selecciona clases:", [1, 2, 3], default=[1, 2, 3])
    df = df[df["Pclass"].isin(class_filter)]

    st.dataframe(df)

    ##### 3. Análisis visual
    import matplotlib.pyplot as plt

    st.subheader("Gráficos Interactivos")

    st.write("Distribución por Clase:")
    class_count = df["Pclass"].value_counts()
    st.bar_chart(class_count)

    st.write("Porcentaje de Supervivencia:")
    survival_rate = df["Survived"].value_counts(normalize=True)
    fig, ax = plt.subplots()
    ax.pie(survival_rate, labels=survival_rate.index, autopct='%1.1f%%')
    st.pyplot(fig)



################
# EJERCICIO 05 #
################

if ejercicio == "5":
    st.header("Ejercicio 5")

    st.subheader("Chatbot con Google AI Studio (Gemini)")
    st.image("https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/e10bea5e-9155-4e5f-6453-6a7495d67f00/full")
    # Campo para la API key de Google
    google_api_key = st.text_input("Introduce tu token", type="password")
    
    # Campo para el mensaje
    user_message = st.text_input("Escribe tu mensaje:")
    
    if st.button("🚀 Enviar") and google_api_key and user_message:
        with st.spinner("Pensando..."):
            try:
                # URL de la API de Google Gemini
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={google_api_key}"
                
                # Payload para la API
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": user_message
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 100
                    }
                }
                
                # Headers
                headers = {
                    "Content-Type": "application/json"
                }
                
                # Hacer la petición
                response = requests.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extraer la respuesta
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            bot_response = candidate["content"]["parts"][0]["text"]
                            
                            st.success("Respuesta generada:")
                            st.write("**Tu mensaje:**")
                            st.write(f"👤 {user_message}")
                            st.write("**Respuesta del bot:**")
                            st.write(f"🤖 {bot_response}")
                        else:
                            st.error("No se pudo extraer la respuesta del resultado")
                    else:
                        st.error("No se recibió una respuesta válida")
                        
                elif response.status_code == 400:
                    error_data = response.json()
                    if "API key not valid" in str(error_data):
                        st.error("API key inválida. Verifica tu clave de Google AI Studio.")
                    else:
                        st.error(f"Error en la solicitud: {error_data}")
                        
                elif response.status_code == 403:
                    st.error("Acceso denegado. Verifica que tu API key tenga los permisos correctos.")
                    
                elif response.status_code == 429:
                    st.error("Has excedido el límite de requests. Espera un momento e intenta de nuevo.")
                    
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Error: {e}")
    
    elif not google_api_key:
        st.warning("Necesitas una API key de Google AI Studio para continuar.")
        
    elif not user_message:
        st.info("Escribe un mensaje para conversar con el bot.")

################
# EJERCICIO 06 #
################

if ejercicio == "6":
    st.header("Ejercicio 6")

    with st.expander("Session State"):
        st.session_state

    st.subheader("Chatbot con Google AI Studio (Gemini) con memoria")
    st.image("https://imagedelivery.net/K11gkZF3xaVyYzFESMdWIQ/e10bea5e-9155-4e5f-6453-6a7495d67f00/full")

#++++++++++++++++++++++++++++++++++++++++++++++
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
#----------------------------------------------

    # Campo para la API key de Google
    google_api_key = st.text_input("Introduce tu token", type="password")
    
    # Campo para el mensaje
    user_message = st.text_input("Escribe tu mensaje:")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Mostrar historial de la conversación
    if st.session_state["chat_history"]:
        st.markdown("---")
        st.markdown("### Historial de la conversación:")
        for i, (role, msg) in enumerate(st.session_state["chat_history"]):
            if role == "user":
                st.write(f"👤 {msg}")
            else:
                st.write(f"🤖 {msg}")
        st.markdown("---")
#-------------------------------------------------------------------------------

    if st.button("🚀 Enviar") and google_api_key and user_message:
        with st.spinner("🤖 Pensando..."):
            try:
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # Construir el historial para el payload con roles correctos
                contents = []
                for role, msg in st.session_state["chat_history"]:
                    if role == "user":
                        contents.append({"role": "user", "parts": [{"text": msg}]})
                    elif role == "bot":
                        contents.append({"role": "model", "parts": [{"text": msg}]})
                # Añadir el mensaje actual del usuario
                contents.append({"role": "user", "parts": [{"text": user_message}]})
#------------------------------------------------------------------------------------
                # URL de la API de Google Gemini
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={google_api_key}"
                
                # Payload para la API
                payload = {
#+SUSTITUCION DE CONTENTS++++++++++++++++++
                    "contents": contents,
#-----------------------------------------
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 100
                    }
                }
                
                # Headers
                headers = {
                    "Content-Type": "application/json"
                }
                
                # Hacer la petición
                response = requests.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extraer la respuesta
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            bot_response = candidate["content"]["parts"][0]["text"]
#++++++++++++++++++++++++++++++++++++++++
                            # Guardar en el historial usando 'user' y 'bot' (para mostrar bonito), pero enviar como 'user' y 'model' a la API
                            st.session_state["chat_history"].append(("user", user_message))
                            st.session_state["chat_history"].append(("bot", bot_response))
#----------------------------------------
                            st.success("Respuesta generada:")
                            st.write("**Tu mensaje:**")
                            st.write(f"👤 {user_message}")
                            st.write("**Respuesta del bot:**")
                            st.write(f"🤖 {bot_response}")
                        else:
                            st.error("No se pudo extraer la respuesta del resultado")
                    else:
                        st.error("No se recibió una respuesta válida")
                        
                elif response.status_code == 400:
                    error_data = response.json()
                    if "API key not valid" in str(error_data):
                        st.error("API key inválida. Verifica tu clave de Google AI Studio.")
                    else:
                        st.error(f"Error en la solicitud: {error_data}")
                        
                elif response.status_code == 403:
                    st.error("Acceso denegado. Verifica que tu API key tenga los permisos correctos.")
                    
                elif response.status_code == 429:
                    st.error("Has excedido el límite de requests. Espera un momento e intenta de nuevo.")
                    
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
#+ PARA HACER REFRESCO
                st.rerun()
#--------------------    
            except Exception as e:
                st.error(f"Error: {e}")
    
    elif not google_api_key:
        st.warning("Necesitas una API key de Google AI Studio para continuar.")
        
    elif not user_message:
        st.info("Escribe un mensaje para conversar con el bot.")


################
# EJERCICIO 07 #
################

if ejercicio == "7":
    st.header("Ejercicio 7")

    st.subheader("Text-to-Speech con Replicate")
    st.image("https://cdn.sanity.io/images/50q6fr1p/production/2542fad4ab944c0f5e1ab7507a3333a2d5f7f464-2626x684.png")
    st.info("Genera un archivo de audio a partir de texto. Modelo 'resemble-ai/chatterbox'.")

    # Campo para el API key de Replicate
    replicate_api_key = st.text_input("Ingresa tu API Key de Replicate:",type="password")

    # Campo para el texto a convertir en audio
    user_message = st.text_area("Escribe el texto que quieres convertir a voz:")

    # Parámetros avanzados del modelo (cfg_weight, temperature, exaggeration)
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     cfg_weight = st.slider(
    #         "CFG Weight",
    #         min_value=0.0,
    #         max_value=1.0,
    #         value=0.5,
    #         step=0.05,
    #         help="Controla la fidelidad al texto (por defecto 0.5)"
    #     )
    # with col2:
    #     temperature = st.slider(
    #         "Temperatura",
    #         min_value=0.0,
    #         max_value=1.0,
    #         value=0.8,
    #         step=0.05,
    #         help="Controla la creatividad de la voz (por defecto 0.8)"
    #     )
    # with col3:
    #     exaggeration = st.slider(
    #         "Exageración",
    #         min_value=0.0,
    #         max_value=1.0,
    #         value=0.5,
    #         step=0.05,
    #         help="Controla la expresividad/emoción (por defecto 0.5)"
    #     )

    if st.button("🚀 Generar Audio") and replicate_api_key and user_message:
        with st.spinner("Generando audio..."):
            try:
                url = "https://api.replicate.com/v1/models/resemble-ai/chatterbox/predictions"
                headers = {
                    "Authorization": f"Token {replicate_api_key}",
                    "Content-Type": "application/json",
                    "Prefer": "wait"
                }
                input_data = {
                    "seed": 0,
                    "prompt": user_message,
                    "cfg_weight": 0.5,
                    "temperature": 0.8,
                    "exaggeration": 0.5
                }
                payload = {
                    "input": input_data
                }
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code in [200, 201]:
                    result = response.json() # El resultado debe tener una URL de audio en 'output' o 'audio'
                    audio_url = result.get("output")
                    if not audio_url and "audio" in result:
                        audio_url = result["audio"]
                    if audio_url:
                        st.success("✅ Audio generado correctamente:")
                        st.audio(audio_url)
                        st.markdown(f"[Descargar audio]({audio_url})")
                    else:
                        st.error("URL no válida")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif not replicate_api_key:
        st.warning("Necesitas una API key de Replicate para continuar.")
    elif not user_message:
        st.info("Escribe un texto para convertir a audio.")


#########################
# EJERCICIO 11 (Casa 1) #
#########################

if ejercicio == "11":
    st.header("Ejercicio 11 - Generador de Identidades")

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


#########################
# EJERCICIO 12 (Casa 2) #
#########################

from bs4 import BeautifulSoup

if ejercicio == "12":
    st.title("Ejercicio 12 (Casa 2)")
    st.header("Buscador de Precios en eBay España con Imágenes")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/EBay_logo.svg/2560px-EBay_logo.svg.png", use_container_width=True)
    # Entrada para buscar productos
    producto = st.text_input("¿Qué producto deseas buscar?", "laptop")

    if producto:
        # Construir la URL de búsqueda en eBay
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        url = f"https://www.ebay.es/sch/i.html?_nkw={producto.replace(' ', '+')}"
        response = requests.get(url, headers=headers)
        st.write(response.text)
        # Verificar que la página se cargue correctamente
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Inicializar listas para almacenar datos
            productos = []
            precios = []
            imagenes = []
            enlaces = []

            # Buscar productos, precios e imágenes en los resultados
            for item in soup.find_all("li", class_="s-item")[2:10]:  # Limitar a 10 productos
                #st.write(item)
                #nombre = item.find("span", role="heading")
                nombre = item.select_one("div.s-item__title")
                precio = item.find("span", class_="s-item__price")
                #precio = item.select_one("span.s-item__price")
                imagen = item.find("img", loading="eager")
                #imagen = item.select_one("img.s-item__image-img")
                enlace = item.select_one("a.s-item__link")

                # if nombre and precio and imagen and enlace:  # Verificar que todos los datos existan
                productos.append(nombre.text)
                precios.append(precio.text)
                imagenes.append(imagen['src'])  # Obtener la URL de la imagen
                enlaces.append(enlace['href'])  # Obtener la URL del enlace
        
            # Mostrar los resultados en Streamlit
            if productos and precios and imagenes:
                st.write("### Resultados:")

                for i in range(len(productos)):
                    st.subheader(productos[i])  # Nombre del producto
                    st.write(f"Precio: {precios[i]}")  # Precio del producto
                    st.image(imagenes[i], width=200)  # Imagen del producto
                    st.markdown(f"[Ver anuncio en eBay]({enlaces[i]})")  # Enlace al producto

            else:
                st.write("No se encontraron resultados para tu búsqueda.")
        else:
            st.write("Error al conectarse a eBay. Por favor, intenta más tarde.")

### Version 2, con cabeceras por mejoras de filtrado de scraping de eBay 
# from bs4 import BeautifulSoup

# if ejercicio == "12":

#     cabeceras = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
#         'Accept-Encoding': 'gzip, deflate',
#         'Connection': 'keep-alive',
#         'Cache-Control': 'max-age=0',
#     }


#     st.title("Ejercicio 12")
#     st.header("Buscador de Precios en eBay España con Imágenes")
#     st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/EBay_logo.svg/2560px-EBay_logo.svg.png", use_container_width=True)
#     # Entrada para buscar productos
#     producto = st.text_input("¿Qué producto deseas buscar?", "laptop")

#     if producto:
#         # Construir la URL de búsqueda en eBay
#         url = f"https://www.ebay.es/sch/i.html?_nkw={producto.replace(' ', '+')}"
        
#         try:
#             response = requests.get(url, headers=cabeceras, timeout=10)
#             st.write(f"Status de la respuesta: {response.status_code}")
            
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, "html.parser")

#                 # Inicializar listas para almacenar datos
#                 productos = []
#                 precios = []
#                 imagenes = []
#                 enlaces = []

#                 items = soup.find_all("li", class_="s-item")
#                 st.write(f"Total de elementos encontrados: {len(items)}")

#                 for i, item in enumerate(items[2:11]): # Procesar solo los items válidos (saltar los primeros 2 que suelen ser headers)

#                     # Buscar elementos con selectores específicos
#                     nombre = item.select_one("h3.s-item__title span")
#                     precio = item.select_one("span.s-item__price")
#                     imagen = item.select_one("div.s-item__image img")
#                     enlace = item.select_one("a.s-item__link")

#                     if nombre and precio and imagen and enlace:  # Verificar que todos los datos existan
#                         productos.append(nombre.get_text(strip=True))
#                         precios.append(precio.get_text(strip=True))
#                         # Obtener la URL de la imagen
#                         img_src = imagen.get('src') or imagen.get('data-src')
#                         if img_src:
#                             imagenes.append(img_src)
#                             enlaces.append(enlace.get('href'))

#                 # Mostrar los resultados en Streamlit
#                 st.write(f"Productos encontrados: {len(productos)}")
#                 if productos and precios and enlaces:
#                     st.write("### Resultados:")

#                     for i in range(len(productos)):
#                         st.subheader(productos[i])  # Nombre del producto
#                         st.write(f"Precio: {precios[i]}")  # Precio del producto
#                         if i < len(imagenes):
#                             st.image(imagenes[i], width=200)  # Imagen del producto
#                         st.markdown(f"[Ver anuncio en eBay]({enlaces[i]})")  # Enlace al producto
#                         st.divider()
#                 else:
#                     st.write("No se encontraron resultados para tu búsqueda.")
#             else:
#                 st.error(f"Error HTTP {response.status_code}: No se pudo acceder a eBay.")
