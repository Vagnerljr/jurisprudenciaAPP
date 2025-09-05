import requests
import json
import pandas as pd
import streamlit as st
import dotenv
import os

dotenv.load_dotenv()

def getAssunto():
    assunto = st.text_input('Digite o assunto do processo:')
    return assunto


def fetch_data(assunto):
    API_KEY = os.environ["DATA_JUD_KEY"]   
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"        
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
        data_raw = processos['dataAjuizamento']  # ex.: '2024-03-27T00:00:00Z'
        data_fmt = pd.to_datetime(data_raw, errors="coerce", utc=True).strftime("%d/%m/%Y")
        orgao = processos['orgaoJulgador']['nome']
        tribunal = processos['tribunal']
        classe = processos['classe']['nome']
        dataFrame.append({
            "Número": numeroProcesso,
            "Grau": grau,
            "Data Ajuizamento": data_fmt,
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
    lambda x: x.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
    if isinstance(x, str) else x)    
    filter = st.selectbox('Orgao Julgador',dataFrame[ "Órgão Julgador"].unique())
    if filter:
        dffiltered = dataFrame[dataFrame["Órgão Julgador"] == filter]
        dffiltered = st.dataframe(dffiltered, hide_index=True)
    else:
        df = st.dataframe(dataFrame, hide_index=True)

 


if __name__ == "__main__":
    main()

    
    

    
    


