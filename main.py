import requests
import json
import pandas as pd
import streamlit as st


def getAssunto():
    assunto = st.text_input('Digite o assunto do processo:')
    return assunto


def fetch_data(assunto):
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search"
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
    return response.json()



def create_dataFrame(data):    
    dataFrame = []
    for item in data["hits"]["hits"]:
        processos = item["_source"]
        assuntos = processos['assuntos'][0]
        numeroProcesso = processos['numeroProcesso']
        grau = processos['grau']
        data = processos['dataAjuizamento']
        orgao = processos['orgaoJulgador']
        dataFrame.append({
            "Número": numeroProcesso,
            "Grau": grau,
            "Data Ajuizamento": data,
            "Órgão Julgador": orgao,
            "Assuntos": assuntos
        })
    return dataFrame


def main():
    assunto = getAssunto()
    data = fetch_data(assunto)    
    dataFrame = pd.DataFrame(create_dataFrame(data))
    st.dataframe(dataFrame)


if __name__ == "__main__":
    main()

    
    

    
    


