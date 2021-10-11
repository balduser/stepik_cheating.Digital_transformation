import time
from selenium import webdriver
from selenium.webdriver.common.by import By

email = "your_email"
password = "your_password"


# Для начала залогинимся
browser = webdriver.Chrome()
browser.get('https://stepik.org/catalog?auth=login')
time.sleep(2)
browser.find_element_by_css_selector('input#id_login_email').send_keys(email)
browser.find_element_by_css_selector('input#id_login_password').send_keys(password)
browser.find_element_by_css_selector('button.sign-form__btn').click()
time.sleep(3)


def is_not_passed(link):
    """Проверяет, пройдено ли задание. Если пройдено, возвращает False"""

    try:
        browser.find_element_by_css_selector(f'[data-is-passed] > a[href="{link}"]')
        print('Задание уже пройдено')
        return False
    except:
        return True


def is_failed(link):
    """Проверяет, было ли провалено текущее задание (нужно ли нажимать "Попробовать снова"). Если так, возвращает True"""

    try:
        browser.find_element_by_css_selector(f'[data-is-attempted] a[href="{link}"]')
        browser.find_element_by_css_selector('span.attempt-message_wrong')
        return True
    except:
        return False


def selecting(args):
    """Отмечает галочками правильные ответы"""

    for a in args:
        browser.find_element(By.XPATH, (f'//div[@data-type="choice-quiz"]//span[contains(text(), "{a}")]')).click()


def radio_right(args):
    """Отмечает ответы в таблицах, где справа горизонтальные radio buttons"""

    for pair in args:
        buttons = browser.find_elements_by_xpath(f'//tr[./td[contains(text(), "{pair}")]]//span[@class="s-radio__border"]')
        buttons[args[pair]].click()


def matching(args):
    """В тестах, где нужно расположить блоки ответов в правильном порядке, перемещает блоки до получения правильного порядка"""
    
    leftside_blocks = browser.find_elements_by_css_selector('div.matching-quiz__left .matching-quiz__item-content span span')
    leftside_texts = [(n, block.text) for n, block in enumerate(leftside_blocks)]
    # Поочерёдно сверху вниз проходит левые блоки 
    for left_n, left_text in leftside_texts:
        # Для блока нужно выбрать правильный ответ
        for pair in args:
            if pair in left_text:
                # Поднятие правого блока может занять несколько итераций
                while True:
                    rightside_blocks = browser.find_elements_by_css_selector('div.matching-quiz__right .matching-quiz__item-content span span')
                    # Если блок ответа уже расположен в нужном месте, эту пару блоков можно пропустить
                    if args[pair] in rightside_blocks[left_n].text:
                        break
                    # Нужно найти и переместить соответствующий блок ответа
                    else:
                        # Определим позицию, на которой расположен правильный ответ для рассматриваемого блока слева
                        position = [i for i, block in enumerate(rightside_blocks) if args[pair] in block.text][0]
                        browser.find_elements_by_css_selector('button span.up-arrow_icon')[position].click()
    return True


def sorting(args):
    """Выстраивает варианты ответов в правильном порядке сверху вниз"""

    # Поочередно сверху вниз проверяем, соответствует ли текущий блок необходимому
    for n, word in enumerate(args):
        while True:
            blocks = browser.find_elements_by_css_selector('div.sorting-quiz__drag-and-drop span span')
            if word not in blocks[n].text:
                # Если не соответствует - поднимаем
                position = [i for i, block in enumerate(blocks) if word in block.text][0]
                browser.find_elements_by_css_selector('button span.up-arrow_icon')[position].click()
            else:
                break


'''tasks = (  # number, link, function, arguments. Для тестов, где ответ один, аргументы должны быть в кортеже (,)!
    ('2.3.1', '/lesson/500465/step/1?unit=492021', matching, (
        {'Автоматизированные системы': 'Робототехника',
         'Устройства в быту': 'Интернет вещей',
         'Надежный способ': 'Системы распределенного реестра (блокчейн)',
         'Компьютерные алгоритмы': 'Искусственный интеллект'})),
    ('2.3.2', '/lesson/500465/step/2?unit=492021', selecting, ('глобализация', 'международное', 'переход')),
    ('2.5.1', '/lesson/500467/step/1?unit=492023', selecting, ('Снижение трансакционных', 'Рост', 'Снижение цены',)),
    ('2.5.2', '/lesson/500467/step/2?unit=492023', selecting, ('Сетевого эффекта',)),
    ('2.7.1', '/lesson/500512/step/1?unit=492068', selecting, ('Клиентоориентированность', 'Автоматизация', 'Отсутствие',)),
    ('2.7.2', '/lesson/500512/step/2?unit=492068', selecting, ('Принцип проактивности',)),
    ('2.7.3', '/lesson/500512/step/3?unit=492068', matching, (
        {'Моносервис': 'Электронный сервис позволяет подать',
         'Суперсервис': 'Электронный сервис позволяет подобрать'})),
    ('2.12.1', '/lesson/501372/step/1?unit=493057', selecting, ('функциональные колодцы',)),
    ('2.12.2', '/lesson/501372/step/2?unit=493057', selecting, ('компьютеры',)),
    ('2.12.3', '/lesson/501372/step/3?unit=493057', selecting, ('консервативная культура',)),
    ('2.12.4', '/lesson/501372/step/4?unit=493057', selecting, ('Продукция, подстроенная',)),
    ('3.3.1', '/lesson/500558/step/1?unit=492113', selecting, ('Решении сложных задач',)),
    ('3.3.2', '/lesson/500558/step/2?unit=492113', selecting, ('Искусственная',)),
    ('3.3.3', '/lesson/500558/step/3?unit=492113', selecting, ('Искусственный интеллект',)),
    ('3.11.1', '/lesson/500566/step/1?unit=492121', selecting, ('дополненной реальности',)),
    ('3.11.2', '/lesson/500566/step/2?unit=492121', selecting, ('распознавания',)),
    ('3.11.3', '/lesson/500566/step/3?unit=492121', selecting, ('интернета вещей',)),
    ('3.11.4', '/lesson/500566/step/4?unit=492121', selecting, ('интернета вещей',)),
    ('3.11.5', '/lesson/500566/step/5?unit=492121', selecting, ('На рисунке А схематично изображена децентрализованная сеть',)),
    ('3.11.6', '/lesson/500566/step/6?unit=492121', selecting, ('умное сельское хозяйство',)),
    ('4.4.1', '/lesson/501375/step/1?unit=493060', radio_right, (
        {'частота колебаний звуковых волн': 0,
         '+7(495)123-45-67': 0,
         'моя любимая мелодия': 1,
         'сигнал «Движения нет»': 1,
         'телефонный номер друга': 1,
         'красный цвет светофора': 0})),
    ('4.4.2', '/lesson/501375/step/2?unit=493060', selecting, ('нормативно-справочной информации',)),
    ('4.4.3', '/lesson/501375/step/3?unit=493060', selecting, ('реестра данных',)),
    ('4.9.1', '/lesson/501378/step/1?unit=493063', selecting, ('Коммерческие',)),
    ('4.9.2', '/lesson/501378/step/2?unit=493063', sorting, ('Бизнес-анализ', 'Анализ данных', 'Подготовка данных', 'Моделирование', 'Оценка решения', 'Внедрение',)),
    ('5.3.1', '/lesson/500850/step/1?unit=492415', selecting, ('проект',)),
    ('5.3.2', '/lesson/500850/step/2?unit=492415', selecting, ('процесс',)),
    ('5.3.3', '/lesson/500850/step/3?unit=492415', selecting, ('проект',)),
    ('5.3.4', '/lesson/500850/step/4?unit=492415', selecting, ('процесс',)),
    ('5.3.5', '/lesson/500850/step/5?unit=492415', sorting, ('Выявление проблемы', 'Проведение анализа', 'Разработка решения', 'Тестирование', 'Контроль соблюдения', )),
    ('5.3.6', '/lesson/500850/step/6?unit=492415', selecting, ('Plan-Do-Check-Act',)),
    ('5.3.7', '/lesson/500850/step/7?unit=492415', selecting, ('да',)),
    ('5.3.8', '/lesson/500850/step/8?unit=492415', selecting, ('нет',)),
    ('5.3.9', '/lesson/500850/step/9?unit=492415', selecting, ('Переоценка жизнеспособности', 'Многократное', 'Переоценка будущего', 'Недооценка', )),
    ('5.6.1', '/lesson/500858/step/1?unit=492422', selecting, ('Сильное влияние и поддержка',)),
    ('5.6.2', '/lesson/500858/step/2?unit=492422', selecting, ('Привлечь',)),
    ('5.6.3', '/lesson/500858/step/3?unit=492422', selecting, ('Сроки, стоимость, содержание работ',)),
    ('5.6.4', '/lesson/500858/step/4?unit=492422', selecting, ('Скорее всего команда небрежно отнеслась к предпроектному анализу и плохо изучила целевую аудиторию',)),
    ('5.6.5', '/lesson/500858/step/5?unit=492422', selecting, ('Диаграмма Ганта',)),
    ('5.6.6', '/lesson/500858/step/6?unit=492422', selecting, ('взаимосвязи между работами',)),
    ('5.6.7', '/lesson/500858/step/7?unit=492422', selecting, ('стоимость работ',)),
    ('5.6.8', '/lesson/500858/step/8?unit=492422', selecting, ('неверно',)),
    ('5.8.1', '/lesson/500873/step/1?unit=492437', selecting, ('матричная организационная структура',)),
    ('5.8.2', '/lesson/500873/step/2?unit=492437', selecting, ('проектная организационная структура',)),
    ('5.8.3', '/lesson/500873/step/3?unit=492437', selecting, ('функциональная организационная структура',)),
    ('5.8.4', '/lesson/500873/step/4?unit=492437', selecting, ('функциональная организационная структура',)),
    ('5.8.5', '/lesson/500873/step/5?unit=492437', selecting, ('проектная организационная структура',)),
    ('5.8.6', '/lesson/500873/step/6?unit=492437', selecting, ('проектный комитет',)),
    ('6.4.1', '/lesson/500878/step/1?unit=492442', selecting, ('Тайити Оно',)),
    ('6.4.2', '/lesson/500878/step/2?unit=492442', selecting, ('Высококвалифицированные сотрудники, занимающие ключевые посты',)),
    ('6.4.3', '/lesson/500878/step/3?unit=492442', selecting, ('А - процессный подход, Б - функциональный подход',)),
    ('6.4.4', '/lesson/500878/step/4?unit=492442', sorting, ('S — Supplier (поставщик)', 'I — Input (вход)', 'P — Process (процесс)', 'O — Output (выход)', 'С — Customer (заказчик)')),
    ('6.4.5', '/lesson/500878/step/5?unit=492442', matching, (
        {'S — Supplier (поставщик)': 'Пациент с проблемой',
         'I — Input (вход)': 'Запись пациента к врачу',
         'P — Process (процесс)': 'Прием у врача',
         'O — Output (выход)': 'Рецепт на лекарство',
         'С — Customer (заказчик)': 'Пациент с рецептом'})),
    ('7.7.1', '/lesson/500930/step/1?unit=492493', matching, (
        {'Стадия внедрения на рынок': 'Энтузиасты',
         'Стадия роста': 'Новаторы',
         'Стадия зрелости': 'Массовые потребители',
         'Стадия спада': 'Консерваторы'})),
    ('7.7.2', '/lesson/500930/step/2?unit=492493', sorting, ('Эмпатия', 'Анализ и синтез', 'Генерация идей', 'Прототипирование', 'Тестирование')),
    ('7.7.3', '/lesson/500930/step/3?unit=492493', selecting, ('В',)),
    ('7.7.4', '/lesson/500930/step/4?unit=492493', selecting, ('А - каскадные методы, Б - Agile',)),
    ('7.7.5', '/lesson/500930/step/5?unit=492493', selecting, ('На картинке А - работа без MVP, на картинках Б и В - работа с MVP, причем Б - «допустимый» вариант, В - «идеальный» вариант использования MVP',)),
    ('8.3.1', '/lesson/501010/step/1?unit=492571', selecting, ('Культура правил',)),
    ('8.3.2', '/lesson/501010/step/2?unit=492571', selecting, ('Культура согласия',)),
    ('8.3.3', '/lesson/501010/step/3?unit=492571', selecting, ('Культура успеха',)),
    ('8.3.4', '/lesson/501010/step/4?unit=492571', selecting, ('Культура принадлежности',)),
    ('8.3.5', '/lesson/501010/step/5?unit=492571', selecting, ('Культура силы',)),
    ('8.3.6', '/lesson/501010/step/6?unit=492571', selecting, ('Культура синтеза',)),
    ('8.7.1', '/lesson/501385/step/1?unit=493069', selecting, ('не имеют отлаженных моделей управления', 'хотят упорядочить работу в период становления и нестабильности')),
    ('8.7.2', '/lesson/501385/step/2?unit=493069', selecting, ('делегирование полномочий', 'правила ведения совещаний', 'управленческое планирование', 'принципы эффективной обратной связи')),
    ('8.7.3', '/lesson/501385/step/3?unit=493069', selecting, ('дерево целей',)),
    ('8.9.1', '/lesson/501387/step/1?unit=493071', selecting, ('У тебя есть идеи', 'Ты сегодня появился')),
    ('8.9.2', '/lesson/501387/step/2?unit=493071', selecting, ('Стендап-планерка', 'Митинг-встреча')),
    ('8.11.1', '/lesson/501391/step/1?unit=493075', selecting, ('А - зона испытания, Б - зона ближайшего развития, В - зона компетентности',)),
    ('8.11.2', '/lesson/501391/step/2?unit=493075', matching, (
        {'МВО': 'управление по целям',
         'KPI': 'ключевые показатели эффективности',
         'BSC': 'система сбалансированных показателей',
         'OKR': 'цели и ключевые результаты'})),
    ('9.6.1', '/lesson/501043/step/1?unit=492602', matching, (
        {'Руководитель цифровой трансформации (CDTO)': 'разрабатывает программу цифровой трансформации',
         'Руководитель по работе с данными (CDO)': 'отвечает за обеспечение руководства качественными и полными данными',
         'Руководитель по цифровому проектированию и процессам': 'руководит реинжинирингом процессов',
         'ИТ-архитектор': 'принимает решения по внутреннему устройству'})),
    ('9.6.2', '/lesson/501043/step/2?unit=492602', matching, (
        {'Аналитик данных': 'обрабатывает, структурирует данные',
         'Инженер данных': 'управляет проектированием, созданием, тестированием',
         'Исследователь данных': 'извлекает из массива данных полезную информацию'})),
    ('9.6.3', '/lesson/501043/step/3?unit=492602', matching, (
        {'CX-эксперт': 'организует изучение потребностей пользователей',
         'Scrum-мастер': 'проводит совещания, разрешает противоречия',
         'Специалист по тестированию': 'создает сценарии тестирования',
         'UX/UI-дизайнер': 'разрабатывает наиболее удобный для пользователя интерфейс',
         'Владелец продукта': 'формирует видение продукта'})),
    ('9.6.4', '/lesson/501043/step/4?unit=492602', selecting, ('CBDO (Chief Business Development Officer)',)),
    ('9.6.5', '/lesson/501043/step/5?unit=492602', selecting, ('A - CTO, Б - CDO',)),
    ('10.5.1', '/lesson/583170/step/1?unit=577901', selecting, ('слежка в интернете', 'обработка данных с помощью ИИ', 'видеонаблюдение')),
    ('10.5.2', '/lesson/583170/step/2?unit=577901', selecting, ('это «цифровой разрыв»',)),
    ('10.5.3', '/lesson/583170/step/3?unit=577901', selecting, ('Необновленное программное обеспечение (ПО)',)),
    ('10.5.4', '/lesson/583170/step/4?unit=577901', selecting, ('Максимально правдоподобная имитация голоса, изображения или видео',)),
    
    ('11.1.2', '/lesson/501048/step/2?unit=492641', selecting, ('«Мы сейчас же начнем исследование того, как сейчас обстоят дела на предприятии»',)),
    ('11.1.3', '/lesson/501048/step/3?unit=492641', selecting, ('Нужно уделить особое внимание трансформации оргкультуры',)),'''
tasks = (
    ('11.1.4', '/lesson/501048/step/4?unit=492641', selecting, ('1. Руководитель цифровой трансформации',)),
    ('11.1.5', '/lesson/501048/step/5?unit=492641', selecting, ('В нашем случае стейкхолдеры — это и руководство, и сотрудники, и клиенты.',)),
    ('11.1.6', '/lesson/501048/step/6?unit=492641', selecting, ('Решением может стать внедрение практик регулярного менеджмента.',)),
    ('11.1.7', '/lesson/501048/step/7?unit=492641', selecting, ('Нужно, чтобы они хорошо освоили принципы текущей культуры правил',)),
    ('11.1.8', '/lesson/501048/step/8?unit=492641', selecting, ('Стоит проанализировать причины неудач ИТ-проектов',)),
    ('11.1.9', '/lesson/501048/step/9?unit=492641', selecting, ('С инвентаризации процессов',)),
    ('11.1.10', '/lesson/501048/step/10?unit=492641', selecting, ('Нужно попытаться объяснить людям',)),
    ('11.1.11', '/lesson/501048/step/11?unit=492641', selecting, ('Это идеи бережливого производства',)),
    )


for task in tasks:
    try:
        print(f'Задание {task[0]}')
        browser.get(f'https://stepik.org{task[1]}')
        time.sleep(4)
        if is_not_passed(task[1]):
            if is_failed(task[1]):
                browser.find_element_by_css_selector('button.again-btn').click()
                time.sleep(4)
            task[2](task[3])
            browser.find_element_by_css_selector('button.submit-submission').click()
            time.sleep(4)
    except Exception as e:
        print('Что-то пошло не так: ', e)

print('Вы восхитительны! Не забудьте сохранить сертификат!')

#browser.quit()
