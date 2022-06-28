import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc

def season_select():
    cursor = conexao.cursor()
    comando_season = '''SELECT DISTINCT SEASON FROM shot_data'''
    cursor.execute(comando_season)
    resultado_season = cursor.fetchall()

    lista_season = []
    for item in resultado_season:
        for nome in item:
            lista_season.append(nome)

    lista_season.sort()

    return lista_season

def team_name():
    cursor = conexao.cursor()
    comando_team = f'''SELECT DISTINCT TEAM_NAME FROM shot_data WHERE SEASON={season_choice}'''
    cursor.execute(comando_team)
    resultado_teams = cursor.fetchall()

    lista_teams = []
    for item in resultado_teams:
        for nome in item:
            lista_teams.append(nome)

    lista_teams.sort()

    return lista_teams

def player_name():
    cursor = conexao.cursor()
    comando_players = f'''SELECT DISTINCT PLAYER_NAME FROM shot_data WHERE (SEASON={season_choice} AND TEAM_NAME='{team_choice}')'''
    cursor.execute(comando_players)
    resultado_players = cursor.fetchall()

    lista_players = []
    for item in resultado_players:
        for nome in item:
            lista_players.append(nome)

    lista_players.sort()

    return lista_players

def shot_dados(season, team, player):
    cursor = conexao.cursor()
    comando_dados = f'''SELECT LOC_X, LOC_Y, EVENT_TYPE FROM shot_data WHERE (SEASON = {season} AND TEAM_NAME = '{team}' AND PLAYER_NAME = '{player}') '''
    cursor.execute(comando_dados)
    resultado_dados = cursor.fetchall()

    lista_dados = []
    for item in resultado_dados:
        lista_dados.append(item)

    dados = pd.DataFrame.from_records(lista_dados, columns=['LOC_X', 'LOC_Y', 'EVENT_TYPE'])

    return dados

def plot_shot(dados):
    markers = {'Missed Shot': 'X', 'Made Shot': 'o'}
    paleta = {'Missed Shot': '#F0421D', 'Made Shot': '#36AC13'}
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(im, extent=[-251, 250, -50, 860])
    sns.scatterplot(ax=ax, x=dados['LOC_X'], y=dados['LOC_Y'], style=dados['EVENT_TYPE'], hue=dados['EVENT_TYPE'], s=15,
                    palette=paleta, markers=markers)
    lng = ax.legend(loc='upper left', title='Shots:', prop={'size': 6})
    lng._legend_box.align = 'left'
    plt.ylabel('')
    plt.xlabel('')
    plt.setp(ax.get_legend().get_texts(), fontsize='6')
    plt.setp(ax.get_legend().get_title(), fontsize='7')
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    return fig

def count_shot_att(season, team, player):
    cursor = conexao.cursor()
    comando_shot_att = f'''SELECT EVENT_TYPE FROM shot_data WHERE (SEASON = {season} AND TEAM_NAME = '{team}' AND PLAYER_NAME = '{player}') '''
    cursor.execute(comando_shot_att)
    resultado_shot_att = cursor.fetchall()

    lista_shot_att = []
    for item in resultado_shot_att:
        for i in item:
            lista_shot_att.append(i)

    return lista_shot_att

def count_shot_made(season, team, player):
    cursor = conexao.cursor()
    comando_shot_made = f'''SELECT EVENT_TYPE FROM shot_data WHERE (SEASON = {season} AND TEAM_NAME = '{team}' AND PLAYER_NAME = '{player}' AND EVENT_TYPE = 'Made Shot') '''
    cursor.execute(comando_shot_made)
    resultado_shot_made = cursor.fetchall()

    lista_shot_made = []
    for item in resultado_shot_made:
        for i in item:
            lista_shot_made.append(i)

    return lista_shot_made

def shot_made_area(season, team, player):
    cursor = conexao.cursor()
    comando_made_area = f'''SELECT EVENT_TYPE, ACTION_TYPE, SHOT_TYPE, SHOT_ZONE_BASIC FROM shot_data WHERE (SEASON = {season} AND TEAM_NAME = '{team}' AND PLAYER_NAME = '{player}' AND EVENT_TYPE = 'Made Shot') '''
    cursor.execute(comando_made_area)
    resultado_made_area = cursor.fetchall()

    lista_made_area = []
    for item in resultado_made_area:
        lista_made_area.append(item)

    dados_made_area = pd.DataFrame.from_records(lista_made_area, columns=['EVENT_TYPE', 'ACTION_TYPE', 'SHOT_TYPE', 'SHOT_ZONE_BASIC'])

    return dados_made_area

def shot_att_area(season, team, player):
    cursor = conexao.cursor()
    comando_att_area = f'''SELECT EVENT_TYPE, ACTION_TYPE, SHOT_TYPE, SHOT_ZONE_BASIC FROM shot_data WHERE (SEASON = {season} AND TEAM_NAME = '{team}' AND PLAYER_NAME = '{player}') '''
    cursor.execute(comando_att_area)
    resultado_att_area = cursor.fetchall()

    lista_att_area = []
    for item in resultado_att_area:
        lista_att_area.append(item)

    dados_att_area = pd.DataFrame.from_records(lista_att_area, columns=['EVENT_TYPE', 'ACTION_TYPE', 'SHOT_TYPE', 'SHOT_ZONE_BASIC'])

    return dados_att_area

def shot_miss_area(season, team, player):
    cursor = conexao.cursor()
    comando_miss_area = f'''SELECT EVENT_TYPE, ACTION_TYPE, SHOT_TYPE, SHOT_ZONE_BASIC FROM shot_data WHERE (SEASON = {season} AND TEAM_NAME = '{team}' AND PLAYER_NAME = '{player}' AND EVENT_TYPE = 'Missed Shot') '''
    cursor.execute(comando_miss_area)
    resultado_miss_area = cursor.fetchall()

    lista_miss_area = []
    for item in resultado_miss_area:
        lista_miss_area.append(item)

    dados_miss_area = pd.DataFrame.from_records(lista_miss_area, columns=['EVENT_TYPE', 'ACTION_TYPE', 'SHOT_TYPE', 'SHOT_ZONE_BASIC'])

    return dados_miss_area

def time_on_the_clock(season, team, player):
    cursor = conexao.cursor()
    comando_clock = f'''SELECT EVENT_TYPE FROM shot_data WHERE (SEASON = {season} AND TEAM_NAME = '{team}' AND PLAYER_NAME = '{player}' AND EVENT_TYPE = 'Made Shot' AND PERIO = 4 AND MINUTES_REMAINING < 2) '''
    cursor.execute(comando_clock)
    resultado_clock = cursor.fetchall()

    lista_clock= []
    for item in resultado_clock:
        for i in item:
            lista_clock.append(i)

    return lista_clock

#Conectando ao Banco de Dados

dados_conexao = (
    "Driver={SQL Server};"
    "Server=NOME_DO_SERVIDOR;"
    "Database=shot_dashboard;"
)

conexao = pyodbc.connect(dados_conexao)

im = plt.imread("nba_full_court.jpg")
sns.set()
st.set_page_config(layout="wide")

#Adicionado uma barra lateral ao dashboard, para o usuário escolher o que deseja visualizar

st.title('Interactive Dashboard')

st.sidebar.markdown("### Filters")
season_choice = st.sidebar.slider('Season:', min_value=min(season_select()), max_value=max(season_select()), step=1)
team_choice = st.sidebar.selectbox('Team:', team_name())
player_choice = st.sidebar.selectbox('Player:', player_name())

#st.markdown(f"### {player_choice}'s shotmap from the {season_choice} season: ")
st.markdown(f'### **{player_choice}**')
st.markdown(f'{team_choice} - {season_choice}')
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

#Coluna 1, Shotmap

col1.pyplot(plot_shot(shot_dados(season_choice, team_choice, player_choice)))

#Informações que serão mostradas na coluna 2
df_shot_att_area = shot_att_area(season_choice, team_choice, player_choice)

col2.metric(label='Shots Attempted', value=len(count_shot_att(season_choice, team_choice, player_choice)))

col2.metric(label='Shots made', value=len(count_shot_made(season_choice, team_choice, player_choice)))

percentage = len(count_shot_made(season_choice, team_choice, player_choice))/len(count_shot_att(season_choice, team_choice, player_choice))*100
col2.metric(label='Shot Percentage', value= f'{round(percentage, 2)}%')

moda_shot_zone = df_shot_att_area['SHOT_ZONE_BASIC'].mode()
col2.metric(label='Favorite zone', value= moda_shot_zone[0])

best_shot_zone = df_shot_att_area.loc[df_shot_att_area['EVENT_TYPE'] == 'Made Shot']['SHOT_ZONE_BASIC'].mode()
col2.metric(label='Best zone', value= best_shot_zone[0])

clutch_shots = len(time_on_the_clock(season_choice, team_choice, player_choice))
col2.metric(label='Clutch Shots', value=clutch_shots)


#Informações que serão mostradas na coluna 3
df_shot_miss_area = shot_miss_area(season_choice, team_choice, player_choice)
df_shot_made_area = shot_made_area(season_choice, team_choice, player_choice)

#Informações sobre arremessos para 2 pontos
two_point_att = len(df_shot_made_area.loc[df_shot_made_area['SHOT_TYPE']=='2PT Field Goal']) + len(df_shot_miss_area.loc[df_shot_miss_area['SHOT_TYPE']=='2PT Field Goal'])
col3.metric(label='2PT attempted', value=two_point_att)

two_point_made = len(df_shot_made_area.loc[df_shot_made_area['SHOT_TYPE']=='2PT Field Goal'])
col3.metric(label='2PT Made', value=two_point_made)

if two_point_att == 0:
    two_point_percentage = 0
else:
    two_point_percentage = len(df_shot_made_area.loc[df_shot_made_area['SHOT_TYPE']=='2PT Field Goal'])/two_point_att*100
col3.metric(label='2PT Percentage', value=f'{round(two_point_percentage, 2)}%')

#Informações sobre arremessos para 3 pontos
three_point_att = len(df_shot_made_area.loc[df_shot_made_area['SHOT_TYPE']=='3PT Field Goal']) + len(df_shot_miss_area.loc[df_shot_miss_area['SHOT_TYPE']=='3PT Field Goal'])
col3.metric(label='3PT attempted', value=three_point_att)

three_point_made = len(df_shot_made_area.loc[df_shot_made_area['SHOT_TYPE']=='3PT Field Goal'])
col3.metric(label='3PT Made', value=three_point_made)

if three_point_att == 0:
   three_point_percentage = 0
else:
    three_point_percentage = len(df_shot_made_area.loc[df_shot_made_area['SHOT_TYPE']=='3PT Field Goal'])/three_point_att*100
col3.metric(label='3PT Percentage', value=f'{round(three_point_percentage, 2)}%')

#Coluna 5 possui as logos do projeto, grupo e universidade, além do link para o repositório
col5.markdown(
        f'''
        <body style="background-color:Gray;">
        <p align="center">
        <img src="https://github.com/crizmorais/shot_dashboard/blob/main/logo_cftb.jpeg?raw=true" height="120" width="120"><br>
        <img src="https://github.com/crizmorais/shot_dashboard/blob/main/logo_gefd.png?raw=true" height="130" width="130"><br>
        <img src="https://github.com/crizmorais/shot_dashboard/blob/main/logo_ufsc.png?raw=true" height="150" width="125"><br><br>
        Developed by <br> Cristiano Zarbato Morais <br><br>
        <a href="https://github.com/crizmorais/shot_dashboard"> Github Repository </a>
        </p></body>
''', unsafe_allow_html=True)