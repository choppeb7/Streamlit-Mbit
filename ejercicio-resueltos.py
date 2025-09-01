import streamlit as st
import requests
import pandas as pd

ejercicio=st.sidebar.radio("Ejercicios Streamlit", [1,2,3,4,5,6,7]);

if ejercicio==1:
    st.header("Ejercicio 1")
    st.header("Geoposicionamiento IP")
    url="https://ifconfig.me/"
    r=requests.get(url)
    ip=r.text
    st.write(f"Tu dirección IP es {ip}")
    url_api_address=f"http://ip-api.com/json/{ip}"
    r=requests.get(url_api_address)
    jsn_address=r.json()
    city=jsn_address["city"]
    st.dataframe(jsn_address)
    df_address=pd.json_normalize(jsn_address)
    df_filtered=df_address.loc[:, ["lat", "lon"]]
    df_mapa=df_filtered
    st.header("Mapa")
    st.map(df_mapa)
    st.info(f"Tu ciudad es la siguiente {city}")


    
    
if ejercicio==2:

    ##cachear todos los pokemon
    @st.cache
    def matrix_pokemon():
        max=50
        url=f"https://pokeapi.co/api/v2/pokemon/?limit={max}"
        r=requests.get(url)
        poke_json=r.json()
        results=poke_json["results"]
        poke_dic=[]
        x=1
        for i in results:
            url_poke_ind=f"https://pokeapi.co/api/v2/pokemon/{x}"
            data_jsn=requests.get(url_poke_ind).json()
            image_pokex=data_jsn["sprites"]["front_default"]

            poke_dic.append({"id":[x], "name":i["name"], "image":image_pokex, "check":False})
            x=x+1
        df_pokedex_matrix=pd.json_normalize(poke_dic)
        return df_pokedex_matrix
    
    if "matrix_editor" not in st.session_state:
        st.session_state["matrix_editor"]= matrix_pokemon()

    def actualizar_datos(x):
         st.session_state["matrix_editor"]=x




    st.header("Ejercicio 2");
    pokemon_id=st.sidebar.number_input("seleccionar id de Pokemon",min_value=1, max_value=1302, step=1)
    url=f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    r=requests.get(url)
     ## Extraemos Datos
    json_pokemon=r.json()
    pokemon_name=json_pokemon["name"]
    pokemon_altura=json_pokemon["height"]
    pokemon_peso=json_pokemon["weight"]
    pokemon_experience=json_pokemon["base_experience"]
    ## Extraemos imagen
    poke_image=json_pokemon["sprites"]["front_default"]
    ## Extraemos habilidades
    abilities=json_pokemon["abilities"]
    list_abilities=[]
    for i in abilities:
        x=i["ability"]["name"]
        list_abilities.append(x)
    ## Extraemos audio
    poke_audio=json_pokemon["cries"]["legacy"]
    



    st.header("Pokedex by Choopeb")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/250px-International_Pok%C3%A9mon_logo.svg.png")
    col1, col2, col3=st.columns(3)

    with col1:
        st.title("Datos")
        st.write(f"Nombre: {pokemon_name}")
        st.write(f"altura:{pokemon_altura}")
        st.write(f"weight:{pokemon_peso}")
        st.write(f"experience:{pokemon_experience}")

    with col2:
        st.title("Aspecto")
        st.image(poke_image)
        st.write("")
        st.write("")
        st.write("")
        st.write("")

    with col3:
        st.title("Habilidades")
        for i in list_abilities:
            st.write(i)


    colA, colB, colC=st.columns(3)

    with colA:
        st.write("")

    with colB:
        st.title("Audio")
        st.audio(poke_audio)
        
    with colC:
       st.write("")

    tab1, tab2, tab3 = st.tabs(["📊Todos los pokemon", "📈 Archivos", "⚙️ Configuración"])


    with tab1:
        st.header("Todos los pokemon")
        disabled_cols=[c for c in st.session_state["matrix_editor"] if c!="check"]
        df_editado=st.data_editor(
                    st.session_state["matrix_editor"],
                       column_config={
                            "image": st.column_config.ImageColumn("image", help="Vista previa", width="small"),
                            "check": st.column_config.CheckboxColumn("check")
        },
        disabled=disabled_cols,
        hide_index=True,
        use_container_width=True,
        key="pokedex_editor"
        )
        guardar =st.button("Guardar cambios", key="guardar_pokedex")
        if guardar ==True:
            actualizar_datos(df_editado)
            st.rerun()
        st.write(f"has visto una cantidad de {sum(st.session_state['matrix_editor']['check'])}")

        




    
    with tab2:
        st.header("Cargar archivo Excel")
        upload_file=st.file_uploader("Sube tu archivo csv", type=["csv"])
        if upload_file is not None:
        # Si es CSV
            new_data = pd.read_csv(upload_file)

            if set(new_data.columns) == set(st.session_state["matrix_editor"].columns):
                st.session_state["matrix_editor"] = new_data
                st.success("Datos cargados exitosamente")

            # Recomiendo quitar st.rerun() si quieres mostrarlo aquí
                st.dataframe(st.session_state["matrix_editor"])
                
        else:
            st.error("Las columnas no coinciden con la matriz actual")
    
    with tab3:
        st.header("⚙️ Configuración")

if ejercicio==3:

    st.header("Ejercicio 3")
    min=st.sidebar.number_input("Filtro valor minimo de poblacion",step=10000, min_value=100000, max_value=10000000000)
    max=st.sidebar.number_input("Filtro valor max de poblacion",step=1000000, min_value=1000000, max_value=10000000000)
    
    @st.cache_data
    def seleccion(x): 
        url_selected=f"https://restcountries.com/v3.1/name/{x}"
        data_pais=requests.get(url_selected)
        json_pais=data_pais.json
        df_pais=pd.json_normalize(json_pais)
        return df_pais
    
    @st.cache_data
    def matrix_paises():
        url="https://restcountries.com/v3.1/independent?status=true&fields=languages,capital,region,languages,population,name"
        data=requests.get(url)
        data_json=data.json()
        df=pd.json_normalize(data_json)
        return df

    if "data_df" not in st.session_state:
       st.session_state["data_df"]=matrix_paises()

    df=st.session_state["data_df"]
    df_paises_filtrados=df.loc[(df["population"] >= min)&(df["population"] < max), :]
    
    # def actualizar(df):
    #     st.session_state["data_df"]=df

    st.dataframe(df_paises_filtrados)
    st.info(f"Hay una cantidad igual a {len(df_paises_filtrados)} de paises con una poblacion entre {min} y {max}")
    

    @st.cache_data
    def seleccion(x): 
        url_selected=f"https://restcountries.com/v3.1/name/{x}"
        data_pais=requests.get(url_selected)
        json_pais=data_pais.json()
        df_pais=pd.json_normalize(json_pais)
        return df_pais
    lista_paises=matrix_paises()["name.common"].tolist()
    pais=st.selectbox("Selecciona un pais",lista_paises)
    st.dataframe(seleccion(pais))

   
    

if ejercicio==4:
    st.header("Ejercicio 4");

if ejercicio==5:
    st.header("Ejercicio 5");

if ejercicio==6:
    st.header("Ejercicio 6");

if ejercicio==7:
    st.header("Ejercicio 7");