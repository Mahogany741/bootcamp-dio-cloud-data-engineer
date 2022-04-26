# ANOTAÇÕES 

# IMPORTANDO A BIBLIOTECA PANDAS e APELIDANDO DE PD 

import pandas as pd


# GERANDO UM DATAFRAME A PARTIR DO CSV

    #parse_dates=['ocorrencia_dia']  - Serve para convertes os dados da coluna, para o tipo data.

df = pd.read_csv("ocorrencia.csv", sep=";", parse_dates=['ocorrencia_dia'])
df

# VERIFICANDO O TIPO DE DADO NAS COLUNAS

df.dtypes

# ACESSANDO UMA COLUNA ESPECÍFICA 

df.ocorrencia_dia

# TRAZENDO APENAS O MES DA DATA

df.ocorrencia_dia.dt.month

# ETAPA DE VALIDAÇÃO 

# IMPRIMINDO APENAS OS 10 PRIMEIROS RESULTADOS 

df = pd.read_csv("ocorrencia.csv", sep=";", parse_dates=['ocorrencia_dia'], dayfirst=True)
df.head(10) #pega os 10 primeiros resultados 
df.tail(10) #pega os 10 últimos resultados

#Campos vazios, no formato data, retornam NaT
#Campos vazios, no formato texto, retornam  NaN


# COMO EVITAR DATAS INCOERENTES (03/50/2010) 
#obs: Mesmo aplicando o parse_dates, se houver uma data incoerente como no exemplo, ele não realizará a conversão.

import pandera as pa

# CRIANDO UM ESQUEMA 

schema = pa.DataFrameSchema(
    columns = {
        'codigo_ocorrencia':pa.Column(pa.Int),
        'codigo_ocorrencia2':pa.Column(pa.Int),
        'ocorrencia_classificacao':pa.Column(pa.String),
        'ocorrencia_uf':pa.Column(pa.String, pa.Check.str_length(2,2)),
        'ocorrencia_cidade':pa.Column(pa.String),
        'ocorrencia_aerodromo':pa.Column(pa.String),
        'ocorrencia_dia':pa.Column(pa.DateTime),
        'ocorrencia_hora':pa.Column(pa.String, pa.Check.str_matches(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])(:[0-5][0-9])?$'), nullable=True), #Declarando que podem existir campos nulos.
        'total_recomendacoes':pa.Column(pa.Int)
    }
)
#validando o schema
schema.validate(df)

# VALIDANDO A COLUNA HORA (Evitando horas incoerentes)
pa.Check.str_matches(r'^([0-1]?[0-9]| [2][0-3]):([0-5][0-9])(:[0-5][0-9])?$')


# VALIDANDO O TAMANHO DO DADO (UF)

pa.Check.str_length(2,2)

# ETAPA DE LIMPEZA

# Filtrando. Os paramentros solicitados são[linha, nome_da_coluna]

df.loc[1, 'ocorrencia_cidade']

#trazendo todos os dados de uma linha

df.loc[3]

#intervalo de resultados 

df.loc[1:3]

#buscando a linha 10 e 40. É necessário criar uma lista, para o python entender que você está omitindo a coluna

df.loc[[10, 40]]

#trazendo todos os dados de uma coluna

df.loc[:, 'ocorrencia_cidade']


#ALTERANDO O INDICE 

#verificando se uma coluna é única(dados distintos)

df.codigo_ocorrencia.is_unique

#alterando o indice

df.set_index('codigo_ocorrencia', inplace=True)

df.head()

#removendo indice alterado

df.reset_index(drop=True, inplace=True)

#ALTERANDO OS DADOS 
#obs: o df.loc, conta a partir do 0.

df.loc[2, 'ocorrencia_aerodromo'] = ''
df.loc[2]

#alterando os dados de todas as colunas de uma linha 
df.loc[1] = 20

#alterando todos os dados de uma coluna
df.loc[:,'total_recomendacoes'] = '10'

df.head(10)
df.tail(10)

#fazendo bkp de uma coluna

df['ocrrencia_uf_bkp'] = df.ocorrencia_uf

#Filtro: Alterando todos os incidentes para GRAVE onde UF = 'sp'
df.loc[df.ocorrencia_uf == 'SP', ['ocorrencia_classificacao']] = 'GRAVE'

#verificando 
df.loc[df.ocorrencia_uf == 'SP']

#PROCESSO DE LIMPEZA

#COLUNA: ocorrencia_uf
# **

#COLUNA: ocorrencia_aerodromo 
# ###!
# ####
# ****
# *****

#COLUNA: ocorrencia_hora
# NULL

#Fazendo replace, dos valores indesejados, para o padrão do PANDAS 'NA'
df.loc[df.ocorrencia_aerodromo == '****', ['ocorrencia_aerodromo']] = pd.NA

#Fazendo o replace em massa 
df.replace(['**', '###!', '####', '****', '*****', 'NULL'], pd.NA, inplace=True)

#Agora que padronizamos os valores NULOS, vamos verificar quantos existem
df.isna().sum #ou df.isnull().sum()

#Preenchendo os campos nulos com algum valor 

df.fillna(10, inplace=True)

#Preenchendo apenas alguns campos nulos
df.fillna(value={'total_recomendacoes':10})


#Criando uma coluna bkp
df['total_recomendacoes_bkp'] = df.total_recomendacoes

#Excluindo coluna bkp
# obs: necessário identificar o eixo, pois o padrão é o eixo da linha
df.drop(['total_recomendacoes_bkp'], axis=1, inplace=True)

#Excluindo as linhas com valores nulos
df.dropna()

#Filtrando por coluna, antes de excluir a linha com valores nulos 
df.dropna(subset=['ocorrencia_uf'])

#Excluindo registros duplicados
df.drop_duplicates()

#ETAPA DE TRANSFORMAÇÃO

