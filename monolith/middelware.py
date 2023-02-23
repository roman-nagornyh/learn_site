class FirstMiddelware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Я создал первый мидедвайр данный код работает до отображения view')
        response = self.get_response(request)
        print('Данный код работает после отображения view')
        return response


class SecondMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Работает второй миддевайр для рендеринга страницы')
        response = self.get_response(request)
        print('Все еще работает второй мидделвайр для рендеринга страницы')
        return response

