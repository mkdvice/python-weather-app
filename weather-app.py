import os

import requests
from pprint import pprint
import dotenv
import streamlit as st

def fazer_request(url, params=None):
    resposta = requests.get(url, params=params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        resultado = None
    else:
        resultado = resposta.json()
    return resultado

def pegar_tempo_para_local(local):
    dotenv.load_dotenv()
    token = os.environ['CHAVE_API_OPENWEATHER']
    
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'appid': token,
        'q': local,
        'units': 'metric',
        'lang': 'pt_br',
    }
    dados_tempo = fazer_request(url=url, params=params)
    return dados_tempo

def main():
    st.title("Web App Tempo")
    st.write("Dados do OpenWeather")
    local = st.text_input('Busque uma cidadade:')
    if not local:
        st.stop()
        
    dados_tempo = pegar_tempo_para_local(local=local)
    if not dados_tempo:
        st.warning(f"Dados não carregados para cidade {local}")
        st.stop()
    clima_atual = dados_tempo["weather"][0]["description"]
    temperatura = dados_tempo["main"]["temp"]
    sensacao_termica = dados_tempo["main"]["feels_like"]
    umidade = dados_tempo["main"]["humidity"]
    cobertura_nuvens = dados_tempo["clouds"]["all"]
    
    st.metric(label="Tempo atual", value=clima_atual)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Temperatura", value=f'{temperatura} ºC')
        st.metric(label="Sensação Térmica", value=f'{sensacao_termica} ºC')
    with col2:
        st.metric(label="Umidade", value=f'{umidade} %')
        st.metric(label="Cobertura de nuvens", value=f'{cobertura_nuvens} %')
        
if __name__ == '__main__':
    main()