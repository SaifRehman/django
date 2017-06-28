from django.http.response import JsonResponse
def hello_world(request):
    return JsonResponse({"message": "hello world!"})