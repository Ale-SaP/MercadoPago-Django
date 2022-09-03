#Django REST
from rest_framework.response import Response
from rest_framework.decorators import api_view

#Django
from django.shortcuts import render

#Env
import environ
env = environ.Env()
environ.Env.read_env()

#Programa
import requests
from datetime import datetime, timedelta
import mercadopago
sdk = mercadopago.SDK(env("TEST_TOKEN"))

#Preferencias
from .preferencias import preferencias

ejemploPropio = [
        {
                    "id": 1,
                    "title": "Deuda 1",
                    "currency_id": "ARS",
                    "description": "7/2022",
                    "quantity": 1,
                    "unit_price": 1
        }, 
        {
                    "id": 2,
                    "title": "Deuda 2",
                    "currency_id": "ARS",
                    "description": "8/2022",
                    "quantity": 2,
                    "unit_price": 5
        }
    ]

def unaPreferenciaPorCadaCuota(lista):
    cantidadDeCuotas = len(lista)
    todasLasRequests = []
    if (cantidadDeCuotas >= 1):

        #Un elemento en la lista con las preferencias incluidas por cada cuota.
        for i in range(0, len(lista) + 1):

            todasLasRequests.append([])
            cuota = lista[i]

            todasLasRequests[i] = {
                "items" : [ {
                    "id": cuota["id"], #Requerido
                    "title": cuota["title"], #Requerido
                    "quantity": 1, #Requerido
                    "unit_price": cuota["unit_price"], #Requerido
                    "description": cuota["description"],
                    "currency_id": "ARS", } ],
            }

            todasLasRequests[i].update(preferencias)

            #Se define el tiempo, el actual es facil pero al futuro hay que cambiarlo bastante, quitarle los MS y cambiar la T 
            now = datetime.now() 
            actual = now.astimezone().strftime("%Y-%m-%dT%H:%M:%S.000-03:00")

            futuro = now + \
                timedelta(days = 3)
            futuro = (str(futuro).split("."))[0] + ".000-03:00"
            futuro = futuro.replace(" ", "T")

            todasLasRequests[i]["expiration_date_from"] = actual
            todasLasRequests[i]["expiration_date_to"] = futuro
        
        return (todasLasRequests)

def unaPreferenciaPorVariasCuotas(lista):
    cantidadDeCuotas = len(lista)
    preferenciasCompletas = preferencias
    preferenciasCompletas["items"] = []

    if (cantidadDeCuotas >= 1):

        #Un elemento en la lista con las preferencias incluidas por cada cuota.
        for cuota in lista:

            preferenciasCompletas["items"].append(
                    {
                    "quantity": 1, #Requerido
                    "id": cuota["id"], #Requerido
                    "title": cuota["title"], #Requerido
                    "unit_price": cuota["unit_price"], #Requerido
                    "description": cuota["description"],
                    "currency_id": "ARS",
                    }
            )

            #Se define el tiempo, el actual es facil pero al futuro hay que cambiarlo bastante, quitarle los MS y cambiar la T 
            now = datetime.now() 
            actual = now.astimezone().strftime("%Y-%m-%dT%H:%M:%S.000-03:00")

            futuro = now + \
                timedelta(days = 3)
            futuro = (str(futuro).split("."))[0] + ".000-03:00"
            futuro = futuro.replace(" ", "T")

            preferenciasCompletas["expiration_date_from"] = actual
            preferenciasCompletas["expiration_date_to"] = futuro
        
        return (preferenciasCompletas)

@api_view(['GET'])
def enviarRequestAMP(request):
    
    listaAEnviar = unaPreferenciaPorVariasCuotas(ejemploPropio)
    listaDeDatosRecibidos = []

    preference_response = sdk.preference().create(listaAEnviar)
    preference = preference_response["response"]
    listaDeDatosRecibidos.append(preference)

    return Response({"loRecibido": listaDeDatosRecibidos})

@api_view(['POST'])
def recibirNotificacion(request):
    datos_recibidos = request.data

    url = datos_recibidos["resource"]

    #Ejemplo de como funciona esta request en el archivo "sendRequest.py"
    recibo = request.get(url, headers={"Authorization": "Bearer " + env("TEST_TOKEN")}) #Reemplazo el test token por el production token
    recibo = recibo.text
    status_details = recibo["status_details"]
    if status_details == "Accredited":
        print(status_details) #Registro en la DB que fué exitoso
    else:
        print(status_details) #Registro en la DB que NO fué exitoso


def frontEndIntegration(request):
    return render(request, "api/index.html")