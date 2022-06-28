#importando as bibliotecas
import os
import pandas as pd

#criando uma lista com todos os arquivos presentes na pasta atual
#que possuem a extensão CSV
file_list = [f for f in os.listdir() if f.endswith('.csv')]

#criando uma lista para armazenar as informações
csv_list = []

#laço de repetição para percorrer todos os arquivos, armazenar em um dataframe,
#incluir uma coluna de temporada e por fim armazenar em uma lista
for files in file_list:
    df = pd.read_csv(files, index_col=[0])
    df['SEASON'] = files[:4]
    csv_list.append(df)
print('FEITO!')

#coloca lista que possui todos os dados de todos os arquivos para um unico arquivo
csv_merged = pd.concat(csv_list, ignore_index=True)

csv_merged.to_csv('csv_merged.csv', index=False)




