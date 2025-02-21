import dash
from dash import dcc, html
import requests
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

def consulta_nomes():
    url = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/carlos|vladmir|augusto"
    response = requests.get(url)
    dados = response.json()
    nomes=[]
    for nome_data in dados:
        nome = nome_data['nome']
        for res in nome_data['res']:
            periodo = res['periodo']
            frequencia = res['frequencia']
            nomes.append({'Nome':nome,'Periodo':periodo,'Frequencia': frequencia})
    df= pd.DataFrame(nomes)
    return df
    
def criar_grafico(df):
    fig = px.line(
        df,
        x='Periodo',
        y='Frequencia',
        color='Nome',
        title = 'Frequencia dos nomes ao logno do tempo',
        labels = {'Periodo':'Periodo','Frequencia': 'Frequencia'})
    return fig
    
app.layout = html.Div([
    html.H1("frequencia dos nomes longo dos periodos"),
    dcc.Graph(id='grafico', figure=criar_grafico(consulta_nomes()))])

if __name__ == '__main__':
    app.run_server(debug=True)
