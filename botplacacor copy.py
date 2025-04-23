import os
import sys
import threading
import keyboard
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from botcity.core import DesktopBot
from botcor import botcor

link_file = "link.txt"  # Nome do arquivo para armazenar o link
config_file = "config.txt"  # Nome do arquivo para armazenar as configurações
contagem = [str(i) for i in range(1, 10001, 1)]  # Lista de contagens de 1 a 10000

def save_link(link):
    with open(link_file, "w") as file:
        file.write(link)

def load_link():
    if os.path.exists(link_file):
        with open(link_file, "r") as file:
            return file.read().strip()
    return ""

def save_config(config):
    try:
        with open(config_file, "w") as file:
            for key, value in config.items():
                file.write(f"{key}={value}\n")
        print("Configurações salvas com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")

def load_config():
    config = {
        "tempo_espera_inicial": 1,
        "tempo_espera": 4,
        "tempo_espera_pagedown": 0,
        "tempo_espera_ctrl_a": 0,
        "tempo_espera_ctrl_c": 0
    }
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.strip().split("=")
                        config[key] = int(value)
            print("Configurações carregadas com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    return config

link_salvo = load_link()  # Carregar o link ao iniciar o bot
config = load_config()  # Carregar as configurações ao iniciar o bot

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def release_keys():
    if keyboard.is_pressed('ctrl'):
        keyboard.release('ctrl')
    if keyboard.is_pressed('shift'):
        keyboard.release('shift')

def interromper():
    while True:
        if keyboard.is_pressed('e'):
            release_keys()
            os._exit(0)

def show_config_window():
    global config  # Usar a variável global

    # Função para salvar as configurações
    def salvar_config():
        try:
            config["tempo_espera_inicial"] = int(tempo_espera_inicial_var.get())
            config["tempo_espera"] = int(tempo_espera_var.get())
            config["tempo_espera_pagedown"] = int(tempo_espera_pagedown_var.get())
            config["tempo_espera_ctrl_a"] = int(tempo_espera_ctrl_a_var.get())
            config["tempo_espera_ctrl_c"] = int(tempo_espera_ctrl_c_var.get())
            save_config(config)
            messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
            janela_config.destroy()  # Fecha a janela
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

    # Criar a janela principal
    janela_config = tk.Tk()
    janela_config.title("Configurações")

    # Variáveis para armazenar os valores
    tempo_espera_inicial_var = tk.StringVar(value=str(config["tempo_espera_inicial"]))
    tempo_espera_var = tk.StringVar(value=str(config["tempo_espera"]))
    tempo_espera_pagedown_var = tk.StringVar(value=str(config["tempo_espera_pagedown"]))
    tempo_espera_ctrl_a_var = tk.StringVar(value=str(config["tempo_espera_ctrl_a"]))
    tempo_espera_ctrl_c_var = tk.StringVar(value=str(config["tempo_espera_ctrl_c"]))

    # Layout da janela
    tk.Label(janela_config, text="Tempo de espera (segundos):").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(janela_config, text="Para carregar a página inicial:").grid(row=1, column=0, sticky="e")
    ttk.Combobox(janela_config, textvariable=tempo_espera_inicial_var, values=[str(i) for i in range(0, 61)]).grid(row=1, column=1)

    tk.Label(janela_config, text="Para consultar a placa:").grid(row=2, column=0, sticky="e")
    ttk.Combobox(janela_config, textvariable=tempo_espera_var, values=[str(i) for i in range(0, 61)]).grid(row=2, column=1)

    tk.Label(janela_config, text="Após executar pagedown:").grid(row=3, column=0, sticky="e")
    ttk.Combobox(janela_config, textvariable=tempo_espera_pagedown_var, values=[str(i) for i in range(0, 61)]).grid(row=3, column=1)

    tk.Label(janela_config, text="Após selecionar todo o texto:").grid(row=4, column=0, sticky="e")
    ttk.Combobox(janela_config, textvariable=tempo_espera_ctrl_a_var, values=[str(i) for i in range(0, 61)]).grid(row=4, column=1)

    tk.Label(janela_config, text="Após copiar a cor do veículo:").grid(row=5, column=0, sticky="e")
    ttk.Combobox(janela_config, textvariable=tempo_espera_ctrl_c_var, values=[str(i) for i in range(0, 61)]).grid(row=5, column=1)

    # Botões
    tk.Button(janela_config, text="Salvar", command=salvar_config).grid(row=6, column=0, pady=10)
    tk.Button(janela_config, text="Cancelar", command=janela_config.destroy).grid(row=6, column=1, pady=10)

    # Iniciar o loop da janela
    janela_config.mainloop()

class Bot(DesktopBot):
    def action(self, execution=None):
        global link_salvo, config  # Usar as variáveis globais
        try:
            # Criar a janela principal
            janela = tk.Tk()
            janela.title("CONSULTAR PLACA * COR")

            # Variáveis para os campos
            link_var = tk.StringVar(value=link_salvo)
            contagem_var = tk.StringVar(value=contagem[0])

            # Layout da janela
            tk.Label(janela, text="Link:").grid(row=0, column=0, sticky="e")
            tk.Entry(janela, textvariable=link_var, width=50).grid(row=0, column=1)

            tk.Label(janela, text="Quantidade de consultas:").grid(row=1, column=0, sticky="e")
            ttk.Combobox(janela, textvariable=contagem_var, values=contagem).grid(row=1, column=1)

            tk.Button(janela, text="Configurações", command=show_config_window).grid(row=2, column=0, pady=10)
            tk.Button(janela, text="Consultar", command=lambda: self.start_consulta(link_var.get(), contagem_var.get())).grid(row=2, column=1, pady=10)

            janela.mainloop()
        except Exception as e:
            print(f"Erro: {e}")

    def start_consulta(self, link, contagem):
        global link_salvo, config
        try:
            link_salvo = link
            save_link(link_salvo)
            cont = int(contagem)
            threading.Thread(target=interromper).start()
            webbrowser.open(link)
            botcor(0, cont, bot=self, self=self, config=config)
        except Exception as e:
            print(f"Erro durante a consulta: {e}")

if __name__ == '__main__':
    Bot.main()