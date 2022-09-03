import requests

#Ejemplo de la request utilizada en "recibirNotificación"
def getData():
    x = requests.get("LINK", 
    headers={"Authorization":"Bearer PRIVATE_TOKEN"})
    print(x.text)

getData()