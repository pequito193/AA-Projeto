import sys
import os
from simulador import Simulador

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

        print("--- Simulação terminada com sucesso. Resultados guardados em 'results.csv' ---")

    except Exception as e:
        print(f"Ocorreu um erro durante a simulação: {e}")

if __name__ == "__main__":
    main()