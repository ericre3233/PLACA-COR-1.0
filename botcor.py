import pyautogui
import time
import pyperclip
from botcity.core import DesktopBot

def botcor(contador, cont, bot: DesktopBot, self: DesktopBot, executation=None, config=None):
    while contador < cont:
        time.sleep(config["tempo_espera_inicial"])  # Usar o tempo de espera inicial fornecido pelo usuário
        
        bot.type_keys(["ctrl", "tab"])
        bot.type_keys(["ctrl", "c"])        
        bot.type_keys(["right"] * 5)
        bot.type_keys(["ctrl", "tab"])
        bot.type_keys(["tab"] * 6)
        bot.type_keys(["ctrl", "v"])  # Cola a placa para pesquisa

        # Captura o texto do campo antes de pressionar Enter
        pyautogui.hotkey("ctrl", "a")  # Seleciona o texto do campo
        pyautogui.hotkey("ctrl", "c")  # Copia o texto selecionado
        time.sleep(1)  # Aguarda para garantir que o texto foi copiado
        texto_antes = pyperclip.paste()  # Obtém o texto copiado

        bot.type_keys(["enter"])  # Realiza a pesquisa
        self.wait(config["tempo_espera"] * 1000)  # Aguarda o tempo configurado para a página carregar

        # Captura o texto do campo após pressionar Enter
        pyautogui.hotkey("ctrl", "a")  # Seleciona o texto do campo
        pyautogui.hotkey("ctrl", "c")  # Copia o texto selecionado
        time.sleep(1)  # Aguarda para garantir que o texto foi copiado
        texto_depois = pyperclip.paste()  # Obtém o texto copiado

        # Verifica se o texto antes e depois são iguais (indicando que a pesquisa falhou)
        if texto_antes == texto_depois:
            print("A pesquisa não foi realizada. Interrompendo o bot.")
            return  # Interrompe a execução do bot

        # Continua com o fluxo normal se a pesquisa foi realizada
        pyautogui.press('pagedown')
        time.sleep(config["tempo_espera_pagedown"])  # Usar o tempo de espera específico
        pyautogui.hotkey("ctrl", "a")
        time.sleep(config["tempo_espera_ctrl_a"])  # Usar o tempo de espera específico

        # Copia o conteúdo para a área de transferência
        pyautogui.hotkey("ctrl", "c")
        time.sleep(config["tempo_espera_ctrl_c"])  # Usar o tempo de espera específico

        # Obtém o texto copiado
        texto_completo = pyperclip.paste()

        # Inicializa a variável cor
        cor = None

        # Procura pela linha onde aparece "Cor"
        for linha in texto_completo.split("\n"):
            if "Cor" in linha:
                cor = linha.split()[-1]  # Pega a última palavra da linha (a cor)
                bot.type_keys(["tab"] * 2)
                bot.type_keys(["enter"])

        if cor:
            bot.type_keys(["ctrl", "tab"])
            self.paste(cor)
            self.wait(1000)
            bot.type_keys(["down"])
            bot.type_keys(["left"] * 5)
            bot.type_keys(["ctrl", "tab"])

        contador += 1