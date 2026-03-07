from django.shortcuts import render

def university_info(request):

    context = {
        'university': {
            'Название': 'Санкт-Петербургский Политехнический Университет Петра Великого',
            'Адрес': 'Политехническая ул., 29, Санкт-Петербург, 195251',
            'Телефон': '8 (812) 775-05-30',
            'Сайт': 'https://www.spbstu.ru/',
            'Описание': 'Высшее учебное заведение в Санкт-Петербурге'
        }
    }
    return render(request, 'university_info.html', context)