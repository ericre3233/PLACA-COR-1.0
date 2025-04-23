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
        bot.type_keys(["ctrl", "v"])
        bot.type_keys(["enter"])
        self.wait(config["tempo_espera"] * 1000)  # Usar o tempo de espera fornecido pelo usuário

        # Verificar se o tempo total de espera é maior ou igual a 2 segundos
        start_time1 = time.time()
        while True:
            if time.time() - start_time1 >= 5:
                self.wait(4000)
            else:
                break


        # Seleciona todo o texto da página
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