from django.shortcuts import render

import requests, json
from django.http import HttpResponse

# Vista que consume Api y envía datos a cliente mediante respuesta HTTP
def index(request):
    url = 'https://dn8mlk7hdujby.cloudfront.net/interview/insurance/58'
    try:
        response = requests.get(url)
        insurance = json.loads(response.text)['insurance']
        return HttpResponse(
            "<ul>Insurance:"
                "<li> Nombre: " + insurance['name'] + "</li>"
                "<li> Descripción " + insurance['description'] + "</li>"
                "<li> Precio: " + insurance['price'] + "</li>"
                "<li> Imagen: <img src=" + insurance['image'] + "/> </li>"
            "</ul>"
        )
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse("No fue posible recuperar información")