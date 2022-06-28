#Declara as bibliotecas que serão utilizadas
import pyodbc
import csv
import time

#Estabele a conexão com o banco
dados_conexao = (
    "Driver={SQL Server};"
    "Server=NOME_DO_SERVIDOR;"
    "Database=shot_dashboard;"
)

conexao = pyodbc.connect(dados_conexao)

print('Conexão bem sucedida')

#Lê o arquivo com os dados de arremesso
with open('csv_merged.csv') as f:
    reader = csv.reader(f)
    data = list(reader)
print(f'\n {data[:4]} \n')

time.sleep(10)

#Elimina a primeira linha do arquivo, o cabeçalho
data.pop(0)
print(f'\n {data[:4]} \n')

cursor = conexao.cursor()

chave_primaria = 1

#Cria um laço de repetição, que passa por cada linha do arquivo e insere as informações em sua
#respectiva coluna na tabela shot_data do nosso banco de dados
for item in data:
    comando = f"""INSERT INTO shot_data(idshot_data, GRID_TYPE,
    GAME_ID, GAME_EVENT_ID, PLAYER_ID, PLAYER_NAME, TEAM_ID
    , TEAM_NAME, PERIO, MINUTES_REMAINING, SECONDS_REMAINING,
    EVENT_TYPE, ACTION_TYPE, SHOT_TYPE, SHOT_ZONE_BASIC
    , SHOT_ZONE_AREA, SHOT_ZONE_RANGE, SHOT_DISTANCE, LOC_X,
    LOC_Y, SHOT_ATTEMPTED_FLAG, SHOT_MADE_FLAG, GAME_DATE, HTM, VTM, SEASON)
VALUES ({chave_primaria}, '{item[0]}', {item[1]}, {item[2]}, {item[3]},
 '{item[4]}', {item[5]}, '{item[6]}', {item[7]}, {item[8]}, {item[9]},
 '{item[10]}', '{item[11]}', '{item[12]}', '{item[13]}', '{item[14]}',
 '{item[15]}', '{item[16]}', {item[17]}, {item[18]}, '{item[19]}', 
 '{item[20]}', '{item[21]}', '{item[22]}', '{item[23]}', {item[24]})"""
    cursor.execute(comando)
    cursor.commit()
    print(f'Entrada número>>>{chave_primaria} --- Dados inseridos na tabela:' 
          f'Jogador {item[4]}, Temporada {item[24]}')
    chave_primaria += 1

    
print('FECHOU!')