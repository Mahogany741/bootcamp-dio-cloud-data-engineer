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

#importando as bibliotecas
import pandas as pd
import pandera as pa

#fazendo a leitura e limpeza parcial simultaneamente
valores_ausentes = ['**', '###!', '####', '****', '*****', 'NULL']
df = pd.read_csv("ocorrencia.csv", sep=";", parse_dates=['ocorrencia_dia'], dayfirst=True, na_values=valores_ausentes)
df.head(10)

#gerando o esquema
schema = pa.DataFrameSchema(
    columns = {
        'codigo_ocorrencia':pa.Column(pa.Int),
        'codigo_ocorrencia2':pa.Column(pa.Int),
        'ocorrencia_classificacao':pa.Column(pa.String),
        'ocorrencia_uf':pa.Column(pa.String, pa.Check.str_length(2,2), nullable=True),
        'ocorrencia_cidade':pa.Column(pa.String),
        'ocorrencia_aerodromo':pa.Column(pa.String, nullable=True),
        'ocorrencia_dia':pa.Column(pa.DateTime),
        'ocorrencia_hora':pa.Column(pa.String, pa.Check.str_matches(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])(:[0-5][0-9])?$'), nullable=True), #Declarando que podem existir campos nulos.
        'total_recomendacoes':pa.Column(pa.Int)
    }
)

#validando o esquema
schema.validate(df)

#verificando o tipo de dados
df.dtypes

#buscando dados da segunda linha
df.loc[1]

#buscando pelo indice 
df.iloc[-1] #(ultima linha)

#buscando uma range com indice
df.iloc[10:15] #esse resultado trará apenas até o 14, diferentemente do df.loc que se baseia no label.

#buscando dados de uma coluna
df.loc[:,'ocorrencia_uf'] 
#or
df['ocorrencia_uf']

#valores nulos
df.isna().sum()
#or
df.isnull().sum()

#buscando linhas com valores nulos
df.ocorrencia_uf.isnull() #metodo booleano: trará todas as linhas da coluna, informando false/true

#trazendo somente, a linha que tem o valor nulo
df.loc[df.ocorrencia_uf.isnull()]

#facilitando o filtro
filtro = df.ocorrencia_uf.isnull()
df.loc[filtro]

#função count
df.count() #não conta valores nulos

#filtros: ocorrencias com mais de 10 recomendacoes
filtro = df.total_recomendacoes > 10
df.loc[filtro]

#filtros: trazendo uma coluna específica, com ocorrencias com mais de 10 recomendacoes
filtro = df.total_recomendacoes > 10
df.loc[filtro, 'ocorrencia_cidade']

#filtros: trazendo mais de uma coluna, com ocorrencias com mais de 10 recomendacoes
filtro = df.total_recomendacoes > 10
df.loc[filtro, ['ocorrencia_cidade', 'total_recomendacoes']]

#filtros: ocorrencia classificada como INCIDENTE GRAVE
filtro = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
df.loc[filtro]

#filtros: classificacao == 'INCIDENTE GRAVE' E UF == 'SP'
filtro1 = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
filtro2 = df.ocorrencia_uf == 'SP'
df.loc[filtro1 & filtro2] #operador logico AND

#filtros: classificacao == 'INCIDENTE GRAVE' OU UF == 'SP'
filtro1 = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
filtro2 = df.ocorrencia_uf == 'SP'
df.loc[filtro1 | filtro2] #operador logico OR

#filtros: classificacao == 'INCIDENTE GRAVE' OU 'INCIDENTE' E UF == 'SP'
filtro1 = (df.ocorrencia_classificacao == 'INCIDENTE GRAVE') | (df.ocorrencia_classificacao == 'INCIDENTE')
filtro2 = df.ocorrencia_uf == 'SP'
df.loc[filtro1 & filtro2]

#filtros: facilitando com o metodo isin() que verifica possibilidades dentro de uma coluna
filtro1 = df.ocorrencia_classificacao.isin(['INCIDENTE GRAVE', 'INCIDENTE'])
filtro2 = df.ocorrencia_uf == 'SP'
df.loc[filtro1 & filtro2]

#filtro parcial: Trazer todas as cidades que comecem com a letra C
# obs: str[0] serve para buscar a primeira letra de uma string (atraves do indice)
filtro = df.ocorrencia_cidade.str[0] == 'C'
df.loc[filtro]

#filtro parcial: Trazer todas as cidades que termine com a letra A
# obs: str[-1] serve para buscar a primeira letra de uma string (atraves do indice)
filtro = df.ocorrencia_cidade.str[-1] == 'A'
df.loc[filtro]

#filtro parcial: Trazer todas as cidades que termine com as letras NA
filtro = df.ocorrencia_cidade.str[-2:] == 'NA'
df.loc[filtro]

#filtro parcial: Trazer todas as cidades que contem as letras MA
filtro = df.ocorrencia_cidade.str.contains('MA')
df.loc[filtro]

#filtro parcial com operador logico OR: Trazer todas as cidades que contem as letras MA OU AL
filtro = df.ocorrencia_cidade.str.contains('MA|AL')
df.loc[filtro]

#filtro parcial: ocorrencia do ano de 2015
filtro = df.ocorrencia_dia.dt.year == 2015
df.loc[filtro]

#filtro parcial: ocorrencia do ano de 2015 e mes 12
#forma 1
filtro1 = df.ocorrencia_dia.dt.year == 2015
filtro2 = df.ocorrencia_dia.dt.month == 12
df.loc[filtro1 & filtro2]

#filtro parcial: ocorrencia do ano de 2015 e mes 12
#forma 2
filtro = (df.ocorrencia_dia.dt.year == 2015) & (df.ocorrencia_dia.dt.month == 12)
df.loc[filtro]

#filtro parcial: ocorrencia do ano de 2015 e mes 12 e dia 8
filtro_ano = df.ocorrencia_dia.dt.year == 2015
filtro_mes = df.ocorrencia_dia.dt.month == 12
filtro_dia = df.ocorrencia_dia.dt.day == 8
df.loc[filtro_ano & filtro_mes & filtro_dia]

#filtro parcial: ocorrencia do ano de 2015 e mes 12 e do dia 3 ao 8
filtro_ano = df.ocorrencia_dia.dt.year == 2015
filtro_mes = df.ocorrencia_dia.dt.month == 12
filtro_dia = (df.ocorrencia_dia.dt.day >=3) & (df.ocorrencia_dia.dt.day <=8)
df.loc[filtro_ano & filtro_mes & filtro_dia]


#filtro parcial: 
# Necessidade: filtrar dia e hora, numa mesma coluna

#passo1: concatenar as colunas ocorrencia_dia e ocorrencia_hora em uma só 
#passo2: como as colunas eram de tipos diferentes, foi necessário realizar a conversão, antes da concatenacao
#passo3: astype(str) foi utilizado para converter em str
#passo4: pd.to_datetime foi utilizado para converter no formato de data e hora
df['ocorrencia_dia_hora'] = pd.to_datetime(df.ocorrencia_dia.astype(str) + ' ' + df.ocorrencia_hora)

#filtro parcial: ocorrencia do ano de 2015 e mes 12 e do dia 3 as 11:00 ao dia 8 13:00
filtro1 = df.ocorrencia_dia_hora >= '2015-12-03 11:00:00'
filtro2 = df.ocorrencia_dia_hora <= '2015-12-08 13:00:00'
df.loc[filtro1 & filtro2]


# AGRUPAMENTO DE DADOS 
#dica: nunca contar, por uma coluna que tem valores nulos

#ocorrencias do ano de 2015 e mes 03
filtro1 = df.ocorrencia_dia.dt.year == 2015
filtro2 = df.ocorrencia_dia.dt.month == 3
df201503 = df.loc[filtro1 & filtro2]
df201503

df201503.count()

df201503.groupby(['ocorrencia_classificacao']).codigo_ocorrencia.count()

df201503.groupby(['ocorrencia_classificacao']).ocorrencia_aerodromo.count()

#size() serve para agrupar e contar os registros
df201503.groupby(['ocorrencia_classificacao']).size()

#ordernando em ordem crescente
df201503.groupby(['ocorrencia_classificacao']).size().sort_values()

#ordernando em ordem decrescente
df201503.groupby(['ocorrencia_classificacao']).size().sort_values(ascending=False)

#agrupando dados da regiao sudeste de 2012
filtro1 = df.ocorrencia_dia.dt.year == 2012
filtro2 = df.ocorrencia_uf.isin(['SP', 'MG', 'ES', 'RJ'])
dfsudeste2012 = df.loc[filtro1 & filtro2]
dfsudeste2012

#agrupando e contando os acidentes
filtro1 = df.ocorrencia_dia.dt.year == 2012
filtro2 = df.ocorrencia_uf.isin(['SP', 'MG', 'ES', 'RJ'])
dfsudeste2012 = df.loc[filtro1 & filtro2]
dfsudeste2012.groupby(['ocorrencia_classificacao']).size()

#agrupando e contando os acidentes, por cada UF
filtro1 = df.ocorrencia_dia.dt.year == 2012
filtro2 = df.ocorrencia_uf.isin(['SP', 'MG', 'ES', 'RJ'])
dfsudeste2012 = df.loc[filtro1 & filtro2]
dfsudeste2012.groupby(['ocorrencia_classificacao', 'ocorrencia_uf']).size()

#agrupando e contando por cidades
dfsudeste2012.groupby(['ocorrencia_cidade']).size().sort_values(ascending=False)

#dados do Rio de Janeiro + total de recomendacoes
filtro = dfsudeste2012.ocorrencia_cidade == 'RIO DE JANEIRO'
dfsudeste2012.loc[filtro].total_recomendacoes.sum()

#dados do Rio de Janeiro + total de recomendacoes
dfsudeste2012.loc[filtro].total_recomendacoes.sum()