import os
import sys
import threading
import time
from tkinter import messagebox
import keyboard
import webbrowser
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from botcity.core import DesktopBot
from botcor import botcor

link_file = "link.txt"
config_file = "config.txt"
contagem = [str(i) for i in range(1, 10001, 1)]  # Lista de 1 a 10000

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

link_salvo = load_link()
config = load_config()

def restart_program():
    print("Reiniciando o programa...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def release_keys():
    if keyboard.is_pressed('ctrl'):
        keyboard.release('ctrl')
    if keyboard.is_pressed('shift'):
        keyboard.release('shift')

def interromper():
    print("Pressione 'E' para interromper o bot.")
    while True:
        if keyboard.is_pressed('e'):
            release_keys()
            print("Bot interrompido pelo usuário.")
            os._exit(0)
        time.sleep(0.1)

#def monitorar_reinicio():
#    while True:
#        if keyboard.is_pressed('r'):
#            release_keys()
#            print("Tecla 'R' pressionada. Reiniciando o programa...")
#            restart_program()
#        time.sleep(0.1)

def encerrar_programa(janela):
    print("Encerrando o programa...")
    release_keys()
    janela.destroy()
    os._exit(0)

class Bot(DesktopBot):
    def action(self, execution=None):
        global link_salvo, config

        #threading.Thread(target=monitorar_reinicio, daemon=True).start()

        def abrir_configuracoes():
            # Verificar se a janela de configurações já está aberta
            if hasattr(abrir_configuracoes, "janela_config") and abrir_configuracoes.janela_config.winfo_exists():
                abrir_configuracoes.janela_config.lift()  # Traz a janela existente para frente
                return

            # Criar a janela de configurações
            abrir_configuracoes.janela_config = ttk.Toplevel()
            janela_config = abrir_configuracoes.janela_config
            janela_config.title("Configurações")

            # Obter a posição da janela principal
            x_principal = janela.winfo_x()
            y_principal = janela.winfo_y()

            # Definir a posição e o tamanho da janela de configurações
            largura = 400
            altura = 400  # Aumentar a altura para 400 pixels
            x_config = x_principal + 50  # 50 pixels à direita da janela principal
            y_config = y_principal + 50  # 50 pixels abaixo da janela principal
            janela_config.geometry(f"{largura}x{altura}+{x_config}+{y_config}")

            # Variáveis para armazenar os valores padrão
            tempo_espera_inicial_var = tk.StringVar(value=str(config["tempo_espera_inicial"]))
            tempo_espera_var = tk.StringVar(value=str(config["tempo_espera"]))
            tempo_pagedown_var = tk.StringVar(value=str(config["tempo_espera_pagedown"]))
            tempo_ctrl_a_var = tk.StringVar(value=str(config["tempo_espera_ctrl_a"]))
            tempo_ctrl_c_var = tk.StringVar(value=str(config["tempo_espera_ctrl_c"]))

            # Valores predefinidos para os Combobox
            valores_tempo = [str(i) for i in range(0, 61)]  # Valores de 0 a 60 segundos

            # Configurar layout com grid
            janela_config.grid_rowconfigure(0, weight=1)
            janela_config.grid_rowconfigure(6, weight=1)
            janela_config.grid_columnconfigure(0, weight=1)
            janela_config.grid_columnconfigure(2, weight=1)

            ttk.Label(janela_config, text="Configurações", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

            ttk.Label(janela_config, text="Tempo de espera inicial:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=tempo_espera_inicial_var, values=valores_tempo).grid(row=1, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Tempo de espera entre consultas:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=tempo_espera_var, values=valores_tempo).grid(row=2, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Tempo de espera após pagedown:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=tempo_pagedown_var, values=valores_tempo).grid(row=3, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Tempo de espera após Ctrl+A:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=tempo_ctrl_a_var, values=valores_tempo).grid(row=4, column=1, sticky="w", padx=10, pady=5)

            ttk.Label(janela_config, text="Tempo de espera após Ctrl+C:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
            ttk.Combobox(janela_config, textvariable=tempo_ctrl_c_var, values=valores_tempo).grid(row=5, column=1, sticky="w", padx=10, pady=5)

            # Função para salvar as configurações
            def salvar_config():
                try:
                    config["tempo_espera_inicial"] = int(tempo_espera_inicial_var.get())
                    config["tempo_espera"] = int(tempo_espera_var.get())
                    config["tempo_espera_pagedown"] = int(tempo_pagedown_var.get())
                    config["tempo_espera_ctrl_a"] = int(tempo_ctrl_a_var.get())
                    config["tempo_espera_ctrl_c"] = int(tempo_ctrl_c_var.get())
                    save_config(config)
                    messagebox.showinfo("Configurações", "Configurações salvas com sucesso!", parent=janela_config)
                    janela_config.destroy()
                except ValueError:
                    messagebox.showerror("Erro", "Por favor, insira valores válidos.", parent=janela_config)

            # Botões "Salvar" e "Cancelar"
            ttk.Button(
                janela_config,
                text="Salvar",
                bootstyle=SUCCESS,
                command=salvar_config
            ).grid(row=6, column=0, pady=20, padx=10, sticky="e")

            ttk.Button(
                janela_config,
                text="Cancelar",
                bootstyle=DANGER,
                command=janela_config.destroy
            ).grid(row=6, column=1, pady=20, padx=10, sticky="w")

        janela = ttk.Window(themename="cosmo")
        janela.title("CONSULTAR PLACA * COR")
        janela.geometry("500x400")

        menu_bar = ttk.Menu(janela)
        menu_inicio = ttk.Menu(menu_bar, tearoff=0)
        menu_inicio.add_command(label="Sair", command=lambda: encerrar_programa(janela))
        menu_bar.add_cascade(label="Início", menu=menu_inicio)

        menu_config = ttk.Menu(menu_bar, tearoff=0)
        menu_config.add_command(label="Configurações", command=abrir_configuracoes)
        menu_bar.add_cascade(label="Configurações", menu=menu_config)

        janela.config(menu=menu_bar)

        # Layout principal com grid
        janela.grid_rowconfigure(0, weight=1)
        janela.grid_rowconfigure(6, weight=1)
        janela.grid_columnconfigure(0, weight=1)
        janela.grid_columnconfigure(3, weight=1)

        # Variável para armazenar a quantidade de consultas selecionada
        quantidade_consultas_var = tk.StringVar(value=contagem[0])

        ttk.Label(janela, text="Link:", font=("Helvetica", 12)).grid(row=1, column=1, sticky="e", padx=10, pady=5)
        
        # Variável para armazenar o link
        link_var = tk.StringVar(value=link_salvo)  # Carrega o link salvo automaticamente

        # Campo de entrada para o link
        ttk.Entry(janela, textvariable=link_var, width=40).grid(row=1, column=2, sticky="w", padx=10, pady=5)

        ttk.Label(janela, text="Quantidade de consultas:", font=("Helvetica", 12)).grid(row=2, column=1, sticky="e", padx=10, pady=5)
        ttk.Combobox(janela, textvariable=quantidade_consultas_var, values=contagem).grid(row=2, column=2, sticky="w", padx=10, pady=5)

        ttk.Button(
            janela,
            text="Consultar",
            bootstyle=SUCCESS,
            command=lambda: self.start_consulta(link_var.get(), quantidade_consultas_var.get())
        ).grid(row=5, column=1, columnspan=2, pady=20)

        # Mensagem abaixo do botão "Consultar"
        ttk.Label(
            janela,
            text="Para interromper o bot, pressione letra e",
            font=("Helvetica", 10),
            foreground="red"
        ).grid(row=6, column=1, columnspan=2, pady=10)

        janela.mainloop()

    def start_consulta(self, link, contagem):
        global link_salvo, config
        try:
            link_salvo = link
            save_link(link_salvo)
            cont = int(contagem)
            threading.Thread(target=interromper, daemon=True).start()
            webbrowser.open(link)
            botcor(0, cont, bot=self, self=self, config=config)
        except Exception as e:
            print(f"Erro durante a consulta: {e}")

if __name__ == '__main__':
    Bot.main()