# MercadoPago-Django
Integración del Checkout Pro de Mercado Pago en Django

# ¿Cómo exactamente funciona la API y esta integración?
Definí en pasos los procesos requeridos para realizar una transacción y cómo están implementados.
* Paso 1: Obtengo de la base de datos (o de donde se envíe) una lista con las cuotas o artículos que quiero que el cliente pague.
* Paso 2: Defino: ¿Quiero que la persona pague cada cuota por separado o todos a la vez? Si debe ser todo en un pago utilizo la función "unaPreferenciaPorVariasCuotas", si cada uno se debe pagar aparte uso "unaPreferenciaPorCadaCuota"
* Paso 3: La función elegida genera una/s preferencias (detalles debajo), que son enviadas a la API de MP mediante el SDK y se recibe como respuesta: el mismo objeto MÁS ciertos datos de mercado pago, incluido el init_point y la ID de las preferencias enviadas en MP.
* Paso 4: Se envía esta ID al front end y se pasa como argumento a una función, que genera un botón con link. Otra alternativa es poner el link "init_point" en el HTML para que lo acceda el usuario, aunque MP no realiza esta implementación. Más detalles en: https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/integrate-checkout-pro (En la sección donde se describe el HTML).
* Paso 5: Una vez que el usuario paga lo que debe en MP, MP notifica a un punto (especificado en las preferencias) que se realizó una transacción. En esta request podemos encontrar si la operación fue exitosa o no en el campo "status". Si queda pendiente, tenemos que enviar la id devuelta a MP para checkear si se acreditó un tiempo después.

* Nota: el campo "status" tiene las siguientes respuestas posibles: "pending", "approved", "authorized", "in_process", "in_mediation", "rejected", "cancelled", "refunded", "charged_back". En teoría podemos programar para considerar todos estos casos, aunque podemos reducir los casos posibles definiendo en las preferencias "binary_mode": True . Más detalles de esta opción en preferencias.


# ¿Cómo implementar esto a tu proyecto?

## Estructura general
* Está programado utilizando el REST Framework de Django, pensado para que el frontend haga un get al framework y se le devuelva un objeto con todos los datos.

## preferencias.py
* Adapte cada campo a sus propias necesidades.

## views.py
* En "enviarRequestAMP" cambie el argumento "ejemploPropio" de "unaPreferenciaPorVariasCuotas" por el propio dato que se desea tratar.
* En "recibirRequestDeMP" , dentro del if añada un sistema que registre en la base de datos cómo fué procesado el pago.
* "frontEndIntegration" y el archivo index.html pueden ser eliminados, ya que se utilizaron para pruebas.

# Preferencias

## ¿Qué es?
* La preferencia es un objeto con múltiples campos que podemos adaptar para nuestro uso específico. El objeto se encuentra en el archivo preferencias.py y ahí podemos ver cada campo con contexto. El campo más relevante es "items", una lista que contiene a su vez los objetos que se van a cobrar al usuario.

## Documentación oficial:
* https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/checkout-customization/preferences

## Preferencias Notables

### items
* El campo "items" es una lista de las diferentes cuotas o artículos que se desean pagar EN UN SOLO PAGO. Puede haber múltiples productos en el campo pero a la hora de pagar se suman los precios y no se pueden separar.

### payment_methods
    "payment_methods": {
        "excluded_payment_methods": lista de diccionarios, ejemplo: "id": "master",
        "excluded_payment_types": lista de diccionarios, ejemplo: "id": "ticket",
        "installments": son las cuotas máximas aceptadas,
        "porpouse": booleano, requeriría que se tenga una cuenta de mercado pago,
    },

### binary_mode
* El modo binario reduce las capacidades de pago de los usuarios, solo da approved o cancelled, no pending o etc.

### expiration_date_from y expiration_date_to 
* Se recomienda en la documentación dar 3 días por los pagos en efectivo, que impactan a las 48hs.
* Esos datos están como ejemplos, cada vez que se crea una preferencia se reemplazan por los actuales.


# Funciones: unaPreferenciaPorCadaCuota y unaPreferenciaPorVariasCuotas

## Entrada y Salida
* Requieren una devuelve UNA preferencia con el campo "items" como una lista de las cuotas.
* unaPreferenciaPorCadaCuota devuelve un objeto de preferencias POR CADA cuota o artículo de la lista que se le dió.
* unaPreferenciaPorVariasCuotas devuelve UN SOLO objeto de preferencias con una lista con los items dentro.

* Las 2 funciones cumplen 2 funciones distintas dado que, si no tenemos manera de separar los productos y los queremos pagar a parte tenemos que enviarlos en requests separadas.

## Notas
* La manera en la que se transforma la entrada debe adapatarse a la lista que se le dé, si no llegan elementos obligatorios como quantity se los puede asignar a 1.
* No sería ideal crear siempre nuevos links, podría ser buena idea anotar en la DB el link asociado al pago y el vencimiento. Si vence en las prox 48hs, se crea uno nuevo en caso de que el usuario pague en efectivo. O se puede excluir al efectivo y se reemplaza al anterior. Igualmente, puede ser una solución más complicada de implementarse que lo que parece por el uso de timedelta() .