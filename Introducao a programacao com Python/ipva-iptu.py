import datetime
print('Aqui começa o programa')

# PEGANDO O MES DA CONSULTA E REALIZANDO O CALCULO DE QUANTOS MESES FALTAM ATÉ O PAGAMENTO DO IPVA

current_time = datetime.datetime.now()
mes = current_time.month

if mes == 12:
    mes = mes - 1

def calc_ipva(valor_veiculo, estado_uf):

    if estado_uf == 'sp':
        resultado = str((valor_veiculo * 0.04) / (12 - mes))
        return resultado
    else:
        print('Fim do programa')

a =  int(input('Informe o valor: '))
b = input('Informe o Estado: ')

# print(type(a))
# print(type(b))
resultado = calc_ipva(a,b)
print('Com base no mes atual e valor do seu IPVA, se vc poupar {} mes, você conseguirá pagar seu IPVA a vista'.format(resultado))