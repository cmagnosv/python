import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

dados_conceitos ={
    'Java':{'variaveis':8,'condicionais': 10,'loops':4, 'poo':3, 'funções':4},
    'Python':{'variaveis':9,'condicionais': 10,'loops':8, 'poo':3, 'funções':4},
    'Sql':{'variaveis':7,'condicionais': 10,'loops':8, 'poo':3, 'funções':4},
    'GoLang':{'variaveis':10,'condicionais': 5,'loops':8, 'poo':3, 'funções':4},
    'JavaScript':{'variaveis':8,'condicionais': 7,'loops':4, 'poo':3, 'funções':4}
}

cores_map = dict(
    Java='red',
    Python='green',
    sql='yellow',
    Golang='blue',
    JavaScript='pink'
)

app = dash.Dash(__name__)
app.layout = html.Div([
html.H4('Sebrae Maranhão',style={'textAlign':'center'}),
html.Div(dcc.Dropdown(
    id="dropdown_linguagens",
    options=[{'label':'Java','value':'Java'},
             {'label':'Python','value':'Python'},
             {'label':'SQL','value':'Sql'},
             {'label':'GoLang','value':'GoLang'},
             {'label':'JavaScript','value':'JavaScript'}
    ],
    value=['Java'],
    multi=True,
    style={'width':'50%', 'margin':'0 auto'}
    )), dcc.Graph(id='grafico_linguagem')
], style={'width':'80%','margin':'0 auto'}
)

@app.callback(
    Output('grafico_linguagem','figure'),
    [Input('dropdown_inguagens','value')]
)

def scarter_linguagens(linguagens_selecionadas):
    scarter_trace=[]
    for linguagem in linguagens_selecionadas:
        dados_linguagem = dados_conceitos[linguagem]
        for conceito,conhecimento in dados_linguagem.items():
            scarter_trace.append(
                go.Scatter(
                x =[conceito],
                y= [conhecimento],
                mode='markers',
                name=linguagem.title(),
                marker={'size':15,'color':cores_map[linguagem]},
                showLegend=False
            )

        )

    scarter_layout = go.layout(
        title = "Meus Conhecimentos em Linguagens",
        xaxis=dict(title='conceitos', showgrid=False),
        yaxis=dict(title='Nivel de Conhecimento', showgrid=False)

    )
    return {'data':scarter_trace,'layout':scarter_layout}




if __name__ =='__main__':
    app.run_server(debug=True)
