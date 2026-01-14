import sys
import os
import csv
import matplotlib.pyplot as plt
from simulador import Simulador

def gerar_grafico_automatico():
    caminho_csv = "results/results.csv"
    caminho_imagem = "results/grafico_steps.png"
    
    if not os.path.exists(caminho_csv):
        print("Aviso: Não foi possível gerar gráfico. Ficheiro CSV não encontrado.")
        return

    # Estrutura para guardar dados: { 'nome_agente': {'episodes': [], 'steps': []} }
    dados_agentes = {}

    try:
        with open(caminho_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                agente = row['agent']
                ep = int(row['episode'])
                steps = int(row['steps'])

                if agente not in dados_agentes:
                    dados_agentes[agente] = {'episodes': [], 'steps': []}
                
                dados_agentes[agente]['episodes'].append(ep)
                dados_agentes[agente]['steps'].append(steps)

        # Configurar e desenhar o gráfico
        plt.figure(figsize=(10, 6))
        
        for nome, dados in dados_agentes.items():
            plt.plot(dados['episodes'], dados['steps'], label=nome)

        plt.xlabel("Episódio")
        plt.ylabel("Passos (Steps)")
        plt.title("Performance: Passos por Episódio")
        plt.legend()
        plt.grid(True)
        
        plt.savefig(caminho_imagem)
        plt.close()
        
        print(f"--- Gráfico gerado automaticamente em '{caminho_imagem}' ---")

    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")

def main():
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "config/maze_test.json" # Default para testes

    if not os.path.exists(config_path):
        print(f"Erro: Ficheiro de configuração '{config_path}' não encontrado.")
        return

    print(f"--- Iniciando Simulador com: {config_path} ---")

    try:
        # Instanciação do Motor de Simulação conforme requisito
        sim = Simulador(config_path)

        agentes = sim.listaAgentes()
        print(f"Agentes detetados: {[a.nome for a in agentes]}")

        sim.executa()

        # Guardar políticas após o treino
        for ag in agentes:
            if hasattr(ag, 'modo') and ag.modo == "learn":
                policy_name = f"results/{ag.nome}_qtable.json"
                if not os.path.exists("results"):
                    os.makedirs("results")
                ag.guardar_politica(policy_name)

        gerar_grafico_automatico()
        
        print("--- Simulação terminada com sucesso. Resultados guardados em 'results.csv' ---")

    except Exception as e:
        print(f"Ocorreu um erro durante a simulação: {e}")

if __name__ == "__main__":
    main()