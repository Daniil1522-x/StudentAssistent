from django.shortcuts import render

def sources(request):
    sources_data = {
        "Группа ВК": ["https://vk.com/your_university_group"],
        "Телеграмм": [
            "Общая группа: https://t.me/your_university",
            "Групповая: https://t.me/your_group_chat",
            "Канал новостей: https://t.me/itmo_news"
        ],
        "Личные кабинеты": [
            "Абитуриент: https://entrant.itmo.ru",
            "Студент: https://student.itmo.ru",
            "Преподаватель: https://teacher.itmo.ru"
        ],
        "Корпоративная почта": ["student@itmo.ru"],
        "Номера телефонов": [
            "Приемная комиссия: +7 (812) 232-97-72",
            "Деканат: +7 (812) 232-97-00",
            "Справочная: +7 (812) 232-97-50"
        ],
        "Официальный сайт": ["https://itmo.ru"],
        "Электронная библиотека": ["https://lib.itmo.ru"]
    }

    return render(request, 'sources.html', {'sources': sources_data})