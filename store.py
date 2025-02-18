import plotly.graph_objs as graph_ob
import plotly.express as px
import pandas as pd
import dash 
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.dependencies import Input, Output
from dash import html, dcc, Input, Output

daerk_theme = 'darkly'
vapor_theme = 'vapor'
url_dark_theme = dbc.themes.DARKLY
url_vapor_theme = dbc.themes.VAPOR

df = pd.read_csv('dataset_comp.csv')
df['dt_Venda'] = pd.todatetime(df['dt_Venda'])
df['Mes'] = df['dt_Venda'].dt.strftime('%b').str.upper()

lista_clientes = []
for cliente in df['Cliente'].unique():
    lista_cliente.append({
        'label':cliente,
        'value':cliente
    })

lista_cliente.append({
    'label': 'Todos os Clientes',
    'value': 'todos_clientes'
})

meses_br = dict(
    JAN = 'JAN',
    FEB = 'FEV',
    MAR = 'MAR',
    MAY = 'MAI',
    JUN = 'JUN',
    JUL = 'JUL',
    AUG = 'AGO',
    SEP = 'SET',
    OCT = 'OUT',
    NOV = 'NOV',
    DEC = 'DEZ'
)
lista_meses = []
for mes in df['Mes'].unique():
    mes_pt = meses_br.get(mes,mes)
    lista_meses.append({
        'label': mes_pt,
        'value': mes
    })
lista_meses.append({
    'label': 'Ano Completo',
    'value': 'ano_completo'
})

lista_categorias=[]
for categoria in df['Categorias'].unique():
    lista_categorias.append({
        'label': categoria,
        'value': categoria
    })

lista_categorias.append({
    'label': 'Todas as Categorias',
    'value': 'todas_categorias'
})

app = dash.Dash(__name__)
server = app.server

#-------layout----------#
layout_titulo = html.Div([
    #---ELEMENTO DO SELECT
    html.Div(
            dcc.Dropdown(
                id='dropdown_cliente',
                options=lista_clientes,
                placeholder=lista_clientes[-1]['label'],
                style={
                    'background-color': 'transparent',
                    'border': 'none',
                    'color': 'black'
                }
            ), style = {'width':'25%'}
    ),
    html.Div(
        html.Legend(
            'Sebrae Maranhão',
            style={
                'font-size':'150%',
                'tex-align': 'center'
            }
        ), style={'width':'50%'}
    ),
    html.Div(
        ThemeSwitchAIO(
            aio_id='theme',
            themes=[
                url_dark_theme,
                url_vapor_theme
            ]
        ), style={'with':'25%'}
    )
], style={
    'text-align': 'center',
    'display': 'flex',
    'justify-content': 'space-around',
    'align-items': 'center',
    'font-family': 'Fira Code',
    'margin-top': '20px'
})

layout_linha01 = html.Div([
    html.Div([
        html.H4(id='output_cliente'),
                dcc.Graph(id='visual01')
    ], style={
        'width':'65%',
        'text-align':'center'}
    ),
    html.Div([
        dbc.Checklist(
            id='radio_mes',
            options=lista_meses,
            inLine=True
        ),
        dbc.RadioItems(
            id='radio_categorias',
            options=lista_categorias,
            inLine=True
        )
    ], style={
        'width': '30%',
        'dysplay': 'flex',
        'flex-direction': 'column',
        'justify-content': 'space-evenly'
        }
    )
], style={
    'display': 'flex',
    'justify-content': 'space-around',
    'margin-top': '40px',
    'height': '300px'
})

layout_linha02 = html.Div([
    html.Div([
        html.H4('Vendas por Mês e Loja/Cidade'),
        dcc.Graph(id='visual02')
    ], style={
        'width': '60%',
        'text-algin': 'center'
        }),
    html.Div([
        dcc.Graph(id='visual03')
    ], , style={'width': '30%'}, style={
        'display': 'flex',
        'justify-content': 'space-around',
        'margin-top':'40px',
        'height': '150px'
    })
])

app.layout= html.Div([
    layout_titulo,
    layout_linha01,
    layout_linha02
])

#---funções de apoio-#
def filtro_cliente(cliente_selecionado):
    if cliente_selecionado is None:
        return pd.series(True,index=df.index)
    return df['Cliente'] == cliente_selecionado

def filtro_categoria(categoria_selecionada):
    if categoria_selecionada is None:
        return pd,series(True, index=df.index)
    elif categoria_selecionada == 'todas_categorias':
        return pd,series(True, index=df.index)
    return df['Categorias'] == categoria_selecionada

def filtro_mes(meses_selecionados):
    if not meses_selecionados:
        return pd.Series(True, index=df.index)
    elif 'ano_completo' in meses_selecionados:
        return pd.Series(True, index=df.index)
    else:
        return df['Mes'].isin(meses_selecionados)


#--call backs-#
@app.callback(
    Output('output_cliente','children'),
    [
      Input('dropdown_cliente','value'),
      Input('radio_categorias','value')  
    ]
    
)
def atualizar_texto(cliente_selecionado, categoria_selecionada):
    if cliente_selecionado and categoria_selecionada:
        return f'TOP5 {categoria_selecionada} | Cliente: {cliente_selecionado}'
    elif cliente_selecionado:
        return f'Cliente: {cliente_selecionado}'
    elif categoria_selecionada:
        return f'TOP5 {categoria_selecionada}'
    return f'TOP5 Categorias'

@app.callback(
    Output('visual01','figure'),
    [
        Input('dropdown_cliente','value'),
        Input('radio_mes','value'),
        Input('radio_categorias','value'),
        Input(ThemeSwitchAIO.ids,switch('theme'),'value')
              
    ]
)

if __name__ == '__main__':
    app.run.server(debug=True)