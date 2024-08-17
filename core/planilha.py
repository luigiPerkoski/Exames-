import pandas as pd
from openpyxl import load_workbook

def ler_com_pandas(caminho_arquivo, nome_planilha):
    # Carrega o arquivo Excel usando pandas
    df = pd.read_excel(caminho_arquivo, sheet_name=nome_planilha)
    
    # Exibe as primeiras linhas do DataFrame
    print("Dados lidos com pandas:")
    print(df.head())

    # Retorna o DataFrame como uma lista de dicionários
    return df.to_dict(orient='records')

def ler_com_openpyxl(caminho_arquivo, nome_planilha):
    # Carrega o arquivo Excel usando openpyxl
    wb = load_workbook(caminho_arquivo)
    sheet = wb[nome_planilha]

    # Itera sobre as linhas da planilha
    dados = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # min_row=2 pula o cabeçalho
        dados.append(row)
    
    print("Dados lidos com openpyxl:")
    for linha in dados:
        print(linha)

    return dados

def main():
    caminho_arquivo = r"C:\Luigi\Document\Code\Python\Project\Exames\TabelaLab.xlsx"  # Caminho completo para o arquivo Excel
    nome_planilha = 'Planilha1'  # Substitua pelo nome da sua planilha

    # Ler dados usando pandas
    dados_pandas = ler_com_pandas(caminho_arquivo, nome_planilha)

    # Ler dados usando openpyxl
    dados_openpyxl = ler_com_openpyxl(caminho_arquivo, nome_planilha)

    # Exemplo de como acessar os dados lidos com pandas
    print("\nPrimeiro registro lido com pandas:")
    if dados_pandas:
        print(dados_pandas[0])

    # Exemplo de como acessar os dados lidos com openpyxl
    print("\nPrimeiro registro lido com openpyxl:")
    if dados_openpyxl:
        print(dados_openpyxl[0])

if __name__ == "__main__":
    main()
