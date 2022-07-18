#Importando as bibliotecas a serem utilizadas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
#Lendo o arquivo
turbina = pd.read_csv('T1.csv')
#Mudando o nome das colunas
turbina.columns = ['Data/Hora', 'Active Power(kW)', 'Velocidade_do_vento (m/s)', 'Curva_teórica(kWh)', 'DirecaoVento(°)']
#delento a coluna que não utilizaremos
del turbina['DirecaoVento(°)']
#Formatando data e hora
turbina['Data/Hora'] = pd.to_datetime(turbina['Data/Hora'])
display(turbina)
#Plotando os dados das turbinas reais em um gráfico
sns.scatterplot(data = turbina, x = 'Velocidade_do_vento (m/s)', y = 'Active Power(kW)' )
#O gráfico nos diz que a uma velocidade do vento x foram gerados y de potência
#Plotando os dados da curva teórica do fabricante
sns.scatterplot(data = turbina, x = 'Velocidade_do_vento (m/s)', y = 'Curva_teórica(kWh)' )
#O gráfico nos mostra a potência ideal gerada a partir da velocidade do vento
#A partir disso, criamos 'Limites aceitáveis', para isso convertemos os valores de Active Power e Curva_teórica em uma lista
pot_real = turbina['Active Power(kW)'].tolist()
pot_teorica = turbina['Curva_teórica(kWh)'].tolist()
pot_max = []
pot_min = []
dentro_limite = []
#Definimos esse limites com 5% acima ou abaixo da Curva teórica, criamos uma lista que aplique esse parâmetro
for potencia in pot_teorica:
  pot_max.append(potencia*1.05)
  pot_min.append(potencia*0.95)
#O que ocorre é que criamos um limite superior e inferior, e estes que estão fora são os considerados ineficientes
#Criaremos também um parâmetro que exclua os itens que, mesmo com velocidade do vento apresentam potência igual a zero pois podem estar desativados ou passando por manutenção
for p, potencia in enumerate(pot_real):
  if potencia >= pot_min[p] and potencia <= pot_max[p]:
    dentro_limite.append('Dentro')
  elif potencia == 0:
    dentro_limite.append('Zero')
  else:
    dentro_limite.append('Fora')
#Vamos verificar a porcetagem das turbinas que estão dentro do limite
print(dentro_limite.count('Dentro')/len(dentro_limite))
#Adionaremos a lista 'dentro_limite' ao dataframe
turbina['DentroLimite'] = dentro_limite
display(turbina)
#Plotando novamente o gráfico com os parâmetros criados
cores = {'Dentro': 'blue', 'Fora':'red', 'Zero':'orange'}
sns.scatterplot(data = turbina, x = 'Velocidade_do_vento (m/s)', y = 'Active Power(kW)', hue = 'DentroLimite', s = 1, palette = cores )

