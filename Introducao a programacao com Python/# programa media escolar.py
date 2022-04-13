# programa media escolar

nota1 = float(input('Informe a primeira nota: '))
nota2 = float(input('Informe a segunda nota: '))

media = (nota1 + nota2) / 2

if media >= 7:
    print('Sua média foi: {}, voce está: aprovado'.format(media))
if media >= 5 and media < 7:
    print('Sua média foi: {}, voce está: recuperacao'.format(media))
if media < 5:
    print('Sua média foi: {}, voce está: reprovado'.format(media))
    






