import pandas as pd

# Função para carregar os dados e limpá-los
def carregar_e_limpar_dados(caminho_arquivo):
    dados = pd.read_csv(caminho_arquivo)
    dados = dados.rename(columns={
        "renewable_generation__twh_chart_elec_fossil_nuclear_renewables": "Renovavel_TWh",
        "nuclear_generation__twh_chart_elec_fossil_nuclear_renewables": "Nuclear_TWh",
        "fossil_generation__twh_chart_elec_fossil_nuclear_renewables": "Fossil_TWh",
        "renewable_generation__twh_chart_elec_fossil_nuclear_renewables.1": "Renovavel_TWh_Alt",
        "nuclear_generation__twh_chart_elec_fossil_nuclear_renewables.1": "Nuclear_TWh_Alt",
        "fossil_generation__twh_chart_elec_fossil_nuclear_renewables.1": "Fossil_TWh_Alt"
    })
    dados = dados.drop(columns=["Renovavel_TWh_Alt", "Nuclear_TWh_Alt", "Fossil_TWh_Alt"])
    return dados

# Função para filtrar os dados por ano e tipo de fonte
def filtrar_dados(dados, ano_inicial=None, ano_final=None, tipo_energia=None):
    dados_filtrados = dados.copy()
    if ano_inicial:
        dados_filtrados = dados_filtrados[dados_filtrados['Year'] >= ano_inicial]
    if ano_final:
        dados_filtrados = dados_filtrados[dados_filtrados['Year'] <= ano_final]
    if tipo_energia:
        dados_filtrados = dados_filtrados[['Year', tipo_energia]]
    return dados_filtrados

# Função para calcular crescimento percentual de uma fonte de energia
def calcular_crescimento(dados, tipo_energia):
    dados_filtrados = dados[['Year', tipo_energia]].dropna()
    if len(dados_filtrados) < 2:
        return None  # Não é possível calcular crescimento com menos de dois pontos de dados
    inicial = dados_filtrados[tipo_energia].iloc[0]
    final = dados_filtrados[tipo_energia].iloc[-1]
    crescimento = ((final - inicial) / inicial) * 100
    return crescimento

# Função para calcular crescimento por década, respeitando os dados disponíveis
def calcular_crescimento_por_decada(dados, tipo_energia):
    decadas = range(1990, min(2020, dados['Year'].max() // 10 * 10) + 1, 10)
    crescimento_decadal = {}
    for inicio in decadas:
        fim = min(inicio + 9, dados['Year'].max())  # Garante que não extrapole os dados disponíveis
        dados_decada = filtrar_dados(dados, ano_inicial=inicio, ano_final=fim, tipo_energia=tipo_energia)
        if len(dados_decada) > 1:  # Exige pelo menos 2 anos de dados para calcular crescimento
            crescimento = calcular_crescimento(dados_decada, tipo_energia)
            if crescimento is not None:
                crescimento_decadal[f"{inicio}-{fim}"] = crescimento
    return crescimento_decadal

# Função para exibir os insights no terminal
def exibir_insights(dados):
    fontes = ["Renovavel_TWh", "Fossil_TWh", "Nuclear_TWh"]
    nomes = {"Renovavel_TWh": "Energia Renovável", "Fossil_TWh": "Energia Fóssil", "Nuclear_TWh": "Energia Nuclear"}
    
    print("Crescimento da geração de energia no Brasil (em TWh):")
    
    for fonte in fontes:
        crescimento_total = calcular_crescimento(dados, fonte)
        if crescimento_total is not None:
            print(f"\n- {nomes[fonte]}: {crescimento_total:.2f}% de crescimento total (1990-{dados['Year'].max()}).")
        else:
            print(f"\n- {nomes[fonte]}: Não há dados suficientes para calcular o crescimento total.")
        crescimento_decadal = calcular_crescimento_por_decada(dados, fonte)
        for decada, crescimento in crescimento_decadal.items():
            print(f"  - {decada}: {crescimento:.2f}% de crescimento.")

# Caminho do arquivo
caminho_arquivo = 'uso_energia_no_brasil.csv'

# Fluxo principal
dados_limpos = carregar_e_limpar_dados(caminho_arquivo)
dados_filtrados = filtrar_dados(dados_limpos, ano_inicial=1990, ano_final=2020)
exibir_insights(dados_filtrados)



