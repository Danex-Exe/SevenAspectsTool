import os, time, requests, socket
from datetime import datetime

class Color:
    def __init__(self, esc_type):
        self.esc_type = esc_type
        self.black = f'{self.esc_type}[30m'
        self.red = f'{self.esc_type}[31m'
        self.green = f'{self.esc_type}[32m'
        self.yellow = f'{self.esc_type}[33m'
        self.blue = f'{self.esc_type}[34m'
        self.white = f'{self.esc_type}[97m'
        self.reset = f'{self.esc_type}[0m'
    def rgb_color(self, r, g, b):
        return f'{self.esc_type}[38;2;{r};{g};{b}m'
    def rgb_bgcolor(self, r, g, b):
        return f'{self.esc_type}[48;2;{r};{g};{b}m'
    def color_message(self, message, color):
        return f'{color}{message}{self.reset}'
def clear():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')
def set_title(title: str):
    if os.name == 'nt': os.system(f"title {title}")
    else: pass
def waiting():
    print("\n\n"+color.reset)
    if os.name == 'nt': os.system('pause')
    else: os.system('clear')
def animate_message(message: str, local_color: str = None, speed: float = 0.015):
    for i in message:
        print(color.color_message(i, local_color) if local_color else i , end="", flush=True)
        time.sleep(speed)
def get_time():
    return f'{color.rgb_bgcolor(174, 61, 245)}{color.white} {datetime.now().strftime("%H:%M:%S")} {color.reset}'
def center_text(message: str):
    return '  ' + message + ' '*(27-len(message))
def stop():
    print(color.color_message("\n\nВы успешно завершили работу програмы", color.green))
    waiting()
    clear()
    quit()
def confirm(message: str, speed: float = 0.015):
    try:
        while True:
            clear()
            animate_message(message)
            t = input()
            if type(t) == str: t.lower()
            match t:
                case 'y': return True
                case 'n': return False
                case _: pass
    except KeyboardInterrupt:
        return False
class System:
    def __init__(self):
        self.project_link = "https://github.com/Danex-Exe/SevenAspectsTool.git"
        self.default_setting_link = "https://raw.githubusercontent.com/Danex-Exe/SevenAspectsTool/refs/heads/main/Attack/setting.json"
        self.version_link = "https://api.github.com/repos/Danex-Exe/SevenAspectsTool/tags"
def check_update(setting):
    """
        check_update(setting) - Функция проверки наличия нового обновления
        setting - Подкласс класса DataBaze (DataFile)
    """
    default_setting = requests.get(project.default_setting_link).json() # Получаем в json формате конфигурационный файл програмы
    response = requests.get(project.version_link)
    if response.status_code == 200:
        project_version = max(response.json(), key=lambda x: x['name'])['name']
        if setting.info() == None:
            if confirm(f"\n\nПрограма потеряла конфигурационный файл, требуется переустановка программы.\nДля переустановки, введите {color.color_message('Y', color.green)} если вы согласы и {color.color_message('n', color.red)} если не согласны. Введите (Y/n): "):
                try:
                    os.system(f"git pull {project.project_link}")
                    setting.create()
                    default_setting['current_version'] = project_version
                    setting.write(default_setting)
                    animate_message("\n\n\n\nВы успешно переустановили программу", color.green)
                    quit()
                except:
                    animate_message(f"\n\n\n\nВо время установки обновления произошла ошибка, пожалуйста переустановити програму вручную (Подробнее: {project.project_link})", color.red)
                    quit()
            else:
                animate_message("\n\n\n\nВы отказались устанавливать обновление", color.red)
                quit()
        else:
            setting_data = setting.read()
            if 'current_version' in setting_data:
                if setting_data['current_version'] == project_version:
                    return
                else:
                    if confirm(f"\n\nВышла новая версия программы.\nДля установки, введите {color.color_message('Y', color.green)} если вы согласы и {color.color_message('n', color.red)} если не согласны. Введите (Y/n): "):
                        try:
                            os.system(f"git pull {project.project_link}")
                            default_setting['current_version'] = project_version
                            setting.write(default_setting)
                            animate_message("\n\n\n\nВы успешно устанавили обновление, перезапустите программу", color.green)
                            quit()
                        except:
                            animate_message(f"\n\n\n\nВо время установки обновления произошла ошибка, пожалуйста переустановити програму вручную (Подробнее: {project.project_link})", color.red)
                            quit()
                    else:
                        animate_message("\n\n\n\nВы отказались устанавливать обновление", color.red)
                        quit()
            else:
                if confirm(f"\n\nПрограма потеряла конфигурационный файл, требуется переустановка программы.\nДля переустановки, введите {color.color_message('Y', color.green)} если вы согласы и {color.color_message('n', color.red)} если не согласны. Введите (Y/n): "):
                    try:
                        os.system(f"git pull {project.project_link}")
                        setting.create()
                        default_setting['current_version'] = project_version
                        setting.write(default_setting)
                        animate_message("\n\n\n\nВы успешно переустановили программу", color.green)
                        quit()
                    except:
                        animate_message(f"\n\n\n\nВо время установки обновления произошла ошибка, пожалуйста переустановити програму вручную (Подробнее: {project.project_link})", color.red)
                        quit()
                else:
                    animate_message("\n\n\n\nВы отказались устанавливать обновление", color.red)
                    quit()
    else:
        animate_message("\n\n\n\nПроблема с подключением к интернету", color.red)
        quit()
    

def check_connection(host: str = "8.8.8.8", port: int = 53, timeout: int = 3):
    """
        Проверяет наличие подключения к интернету.

        Аргументы:
            host (str) -- Адрес для проверки (по умолчанию 8.8.8.8 - DNS Google)
            port (int) -- Порт для проверки соединения (по умолчанию 53)
            timeout (int) -- Таймаут соединения в секундах (по умолчанию 3)

        Возвращает:
            bool -- True, если соединение установлено, иначе False.
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        return True
    except socket.error:
        return False

color = Color('\033') # Класс для использования цвета в командной строке
project = System() # Класс с системными значениями