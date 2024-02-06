from decimal import Decimal
import pandas as pd
import os
import tkinter as tk
from tkinter import ttk

# Função para calcular as combinações de odds
def calcular_combinacoes():
    # Função interna para converter os valores dos campos de texto em floats
    def converter_para_float(valor):
        try:
            return float(valor)
        except ValueError:
            return 0.0

    # Obter os valores de entrada dos campos de texto e convertê-los em floats
    odds_values = [[converter_para_float(e.get()) for e in row] for row in odds_entries]

    # Inicializar uma lista vazia para armazenar as combinações
    combinacoes = []

    # Percorrer cada conjunto de odds na lista de entrada
    for i in range(len(odds_values)):
        # Extrair os valores de Time 1, Empate e Time 2
        time1 = odds_values[i][0]
        empate = odds_values[i][1]
        time2 = odds_values[i][2]
        # Percorrer os outros conjuntos de odds na lista de entrada
        for j in range(len(odds_values)):
            # Verificar se o índice é diferente do atual
            if j != i:
                # Extrair os valores de Time 1, Empate e Time 2
                time1_2 = odds_values[j][0]
                empate_2 = odds_values[j][1]
                time2_2 = odds_values[j][2]
                # Percorrer os outros conjuntos de odds na lista de entrada
                for k in range(len(odds_values)):
                    # Verificar se o índice é diferente dos anteriores
                    if k != i and k != j:
                        # Extrair os valores de Time 1, Empate e Time 2
                        time1_3 = odds_values[k][0]
                        empate_3 = odds_values[k][1]
                        time2_3 = odds_values[k][2]
                        # Criar uma lista com uma combinação de odds
                        combinacao = [time1, empate_2, time2_3]
                        # Calcular a odd total da combinação
                        odd_total = round(time1 * empate_2 * time2_3, 2)
                        # Adicionar a odd total à lista da combinação
                        combinacao.append(odd_total)
                        # Adicionar a lista da combinação à lista de combinações
                        combinacoes.append(combinacao)
    # Retornar a lista de combinações
    return combinacoes

# Função para criar a interface gráfica
def criar_interface():
    root = tk.Tk()
    root.title("Gerador de Combinações de Odds")

    # Criar uma lista para armazenar os campos de entrada de odds
    global odds_entries
    odds_entries = []

    # Adicionar campos de entrada para cada conjunto de odds
    for i, odd in enumerate(odds_labels):
        ttk.Label(root, text=odd).grid(row=i, column=0)
        entry_row = []
        for j in range(3):
            entry = ttk.Entry(root)
            entry.grid(row=i, column=j+1)
            entry.insert(tk.END, "0.00")
            entry_row.append(entry)
        odds_entries.append(entry_row)

    # Adicionar um botão para gerar as combinações
    ttk.Button(root, text="Gerar Combinações", command=gerar_combinacoes_e_salvar).grid(row=len(odds_labels), columnspan=4)

    root.mainloop()

# Função para gerar as combinações e salvar em um arquivo
def gerar_combinacoes_e_salvar():
    # Chamar a função que gera as combinações de odds
    combinacoes = calcular_combinacoes()

    # Criar um dataframe pandas com as combinações
    df = pd.DataFrame(combinacoes, columns=["Time 1", "Empate", "Time 2", "Odd Total"])

    # Salvar o dataframe em um arquivo xlsx
    df.to_excel(r'combinações.xlsx', index=False)
    # Mostrar uma mensagem de confirmação
    print("Arquivo de combinações gerado com sucesso!")

# Função para calcular as apostas
def calcular_apostas(valor_total, odd_aposta1, odd_aposta2, odd_aposta3):
    valor_total = Decimal(str(valor_total))
    odd_aposta1 = Decimal(str(odd_aposta1))
    odd_aposta2 = Decimal(str(odd_aposta2))
    odd_aposta3 = Decimal(str(odd_aposta3))

    melhor_retorno = Decimal('0.00')
    melhor_aposta1 = Decimal('0.00')
    melhor_aposta2 = Decimal('0.00')
    melhor_aposta3 = Decimal('0.00')

    for centavos_aposta1 in range(1, int(valor_total * 100)):
        aposta1 = Decimal(centavos_aposta1) / Decimal(100)
        aposta2 = 0
        aposta3 = valor_total - aposta1

        while aposta3 <= 0:
            aposta2 += 0.01
            aposta3 = valor_total - aposta1 - aposta2

        retorno_aposta1 = aposta1 * odd_aposta1
        retorno_aposta2 = aposta2 * odd_aposta2
        retorno_aposta3 = aposta3 * odd_aposta3

        retorno_total = min(retorno_aposta1, retorno_aposta2, retorno_aposta3)
        if retorno_total > melhor_retorno:
            melhor_retorno = retorno_total
            melhor_aposta1 = aposta1
            melhor_aposta2 = aposta2
            melhor_aposta3 = aposta3

    if melhor_retorno > valor_total:
        return melhor_aposta1, melhor_aposta2, melhor_aposta3
    else:
        return None

# Função para processar o arquivo de entrada e salvar o resultado
def processar_excel(entrada_excel, saida_excel):
    try:
        df = pd.read_excel(entrada_excel)
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return

    resultados = []
    for index, row in df.iterrows():
        resultado = calcular_apostas(10.00, row['Time 1'], row['Empate'], row['Time 2'])
        resultados.append(resultado)

    df['Aposta 1'] = [f"Aposta 1: Apostei {res[0]:.2f}" if res else f"Não é possível realizar as apostas para obter um retorno acima de 10.00" for res in resultados]
    df['Aposta 2'] = [f"Aposta 2: Apostei {res[1]:.2f}" if res else None for res in resultados]
    df['Aposta 3'] = [f"Aposta 3: Apostei {res[2]:.2f}" if res else None for res in resultados]

    df.to_excel(saida_excel, index=False)
    print(f"Resultados escritos em {saida_excel}.")

# Lista de labels para os campos de entrada de odds
odds_labels = ["Odds 1", "Odds 2", "Odds 3", "Odds 4"]

# Criar a interface gráfica
criar_interface()

# Caminhos dos arquivos de entrada e saída
caminho_arquivo_entrada = r'combinações.xlsx'
caminho_arquivo_saida = r'Resultado_ODDS.xlsx'

# Processar o arquivo de entrada e salvar o resultado
processar_excel(caminho_arquivo_entrada, caminho_arquivo_saida)
