preferencias = {
    "back_urls" : {
        "success": "https://www.success.com", # Si se envía correctamente los datos a mercado libre, redirecciona acá
        "failure": "http://www.failure.com", # Si falla, acá
        "pending": "http://www.pending.com" # Si queda pendiente, acá 
    },

    "auto_return": "approved", # Volver a la página automaticamente

    #"payment_methods" en el readme

    "notification_url": "https://www.your-site.com/ipn", # URL a la cual te gustaría recibir notificaciones de pagos.
    #Alternativa en readme
    
    "binary_mode": False, #En readme

    "statement_descriptor": "MINEGOCIO", # Descripción del negocio.

    "external_reference": "Reference_1234", # Identificador único que envía el vendedor para relacionar la order_id 
                                            # Generada por Mercado Pago, con el id de su sistema de pagos

    "expires": True, # Booleano

    "expiration_date_from": "2016-02-01T12:00:00.000-04:00", #En readme
    "expiration_date_to": "2016-02-28T12:00:00.000-04:00",

    # "porpouse" : "wallet_porpouse", En readme

    # "payer" : En la documentación hay más detalles, no es requerido. 
    # https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/checkout-customization/preferences 
}