import requests
import json
import pandas as pd
import streamlit as st


def getAssunto():
    assunto = st.text_input('Digite o assunto do processo:')
    return assunto


def fetch_data(assunto):
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
    API_KEY = 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=='
    payload = json.dumps({
                "query": {
                    "match": {"assuntos.nome": assunto}}
                }
                )
               
    headers = {
                'Authorization':f'ApiKey {API_KEY}',
                'Content-Type': 'application/json'
}
    response = requests.request("POST", url, headers=headers, data=payload)
    response.encoding = "utf-8"
    return response.json()



def create_dataFrame(data):    
    dataFrame = []
    for item in data["hits"]["hits"]:
        processos = item["_source"]
        assuntos = processos['assuntos'][0]['nome']
        numeroProcesso = processos['numeroProcesso']
        grau = processos['grau']
        data = processos['dataAjuizamento']
        orgao = processos['orgaoJulgador']['nome']
        tribunal = processos['tribunal']
        classe = processos['classe']['nome']
        dataFrame.append({
            "Número": numeroProcesso,
            "Grau": grau,
            "Data Ajuizamento": data,
            "Órgão Julgador": orgao,
            "Assuntos": assuntos,
            "Tribunal":tribunal,
            "Classe": classe
        })
    return dataFrame


def main():    
    st.set_page_config(layout= "wide")
    st.header('Site de pesquisa de Jurisprudencia')
    assunto = getAssunto()
    if not assunto:
        st.stop()    
    data = fetch_data(assunto)        
    dataFrame = pd.DataFrame(create_dataFrame(data)).applymap(
    lambda x: x.encode("cp1252", errors="ignore").decode("utf-8", errors="ignore")
    if isinstance(x, str) else x)    
    filter = st.selectbox('Orgao Julgador',dataFrame[ "Órgão Julgador"].unique())
    if filter:
        dffiltered = dataFrame[dataFrame["Órgão Julgador"] == filter]
        dffiltered = st.dataframe(dffiltered, hide_index=True)
    else:
        df = st.dataframe(dataFrame, hide_index=True)

 


if __name__ == "__main__":
    main()

    
    

    
    


