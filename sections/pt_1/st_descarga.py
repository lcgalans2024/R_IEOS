import streamlit as st
import pandas as pd
import io

from funciones import asignar_nivel_lc, asignar_nivel_M, asignar_nivel_CN, asignar_nivel_ingles

def descarga():
    st.header("Descarga de Datos 📥")

    # Verifica si los datos están en session_state
    if "datos_filtrados" not in st.session_state:
        st.warning("No se han cargado datos aún.")
        return
    
    # Cargar los datos
    df = st.session_state["datos"]
    
    Prueba = st.radio("Seleccione la prueba de la cual desea obtener los resultados:", ["Simulacros o ICFES"
                                                                                        #, "Olimpiadas"
                                                                                        ])

    col1, col2, col3 = st.columns(3)

    if Prueba == "Simulacros o ICFES":
      with col1:
         # Crear un selector de area con st.multiselect
         areas = st.multiselect(
            "Selecciona las áreas",
            ["Puntaje global"
            ,"Matemáticas"
            ,"Lectura crítica"
            ,"Ciencias naturales"
            ,"Sociales y ciudadanas"
            ,"Inglés"],
            default=["Puntaje global"],
            )
    
      with col2:
         # Crear un selector de pruebas con st.multiselect
         
         pruebas = st.multiselect(
            "Selecciona las pruebas",
            st.session_state["datos_filtrados"].SIMULACRO.unique().tolist(),
            default=["S1"],
        )
    
      with col3:
          G_unicos = df["Grupo"].unique()
          # Crear un selector de grupo con st.selectbox
          Eleccion = st.selectbox("Seleccione el grupo:", G_unicos)

      
      # Seleccionamos grupo
      datos_grupo_seleccionado = df[(df.SIMULACRO.isin(pruebas)) &
                                       (df.Grupo == Eleccion) &
                                       (df['AÑO'] == st.session_state["año_seleccionado"])
                                       ] 
      df_resultados_grupo = datos_grupo_seleccionado.groupby(["DOCUMENTO","Nombre alumno"])[
                                                                                      areas
                                                                                ].mean().round(2).reset_index()
      
      if "Lectura crítica" in areas:
          indice_lc = df_resultados_grupo.columns.get_loc("Lectura crítica")
          df_resultados_grupo.insert(indice_lc + 1, "ND_LC", None)
          df_resultados_grupo['ND_LC'] = df_resultados_grupo['Lectura crítica'].apply(asignar_nivel_lc)
      if "Matemáticas" in areas:
        indice_m = df_resultados_grupo.columns.get_loc("Matemáticas")
        df_resultados_grupo.insert(indice_m + 1, "ND_M", None)
        df_resultados_grupo['ND_M'] = df_resultados_grupo['Matemáticas'].apply(asignar_nivel_M)
      if "Ciencias naturales" in areas:
        indice_cn = df_resultados_grupo.columns.get_loc("Ciencias naturales")
        df_resultados_grupo.insert(indice_cn + 1, "ND_CN", None)
        df_resultados_grupo['ND_CN'] = df_resultados_grupo['Ciencias naturales'].apply(asignar_nivel_CN)
      if "Sociales y ciudadanas" in areas:
        indice_sc = df_resultados_grupo.columns.get_loc("Sociales y ciudadanas")
        df_resultados_grupo.insert(indice_sc + 1, "ND_SC", None)
        df_resultados_grupo['ND_SC'] = df_resultados_grupo['Sociales y ciudadanas'].apply(asignar_nivel_CN)
      if "Inglés" in areas:
        indice_ig = df_resultados_grupo.columns.get_loc("Inglés")
        df_resultados_grupo.insert(indice_ig + 1, "ND_IG", None)
        df_resultados_grupo['ND_IG'] = df_resultados_grupo['Inglés'].apply(asignar_nivel_ingles)
      
      
      #############################################
      st.dataframe(df_resultados_grupo.reset_index(drop=True), use_container_width=True, hide_index=True)
  
      # Crear archivo Excel en memoria
      output = io.BytesIO()
      # Botón para descargar el DataFrame como CSV
      with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_resultados_grupo.to_excel(writer, sheet_name=f"Resultados_{Eleccion}", index=False)
        writer.close()
  
      output.seek(0)
  
      # Botón de descarga
  
      st.download_button(
        label="📥 Descargar resultados en Excel",
        data=output,
        file_name=f"Resultados_Grupo_{Eleccion}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Descargar los datos filtrados como archivo Excel."
      )
    
    ## Botón para descargar el DataFrame como Excel
#
    #excel = df.to_excel(index=False).encode('utf-8')
    #st.download_button(
    #    label="Descargar Excel",
    #    data=excel,
    #    file_name='datos.xlsx',
    #    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    #    help="Descargar los datos filtrados como archivo Excel."
    #)