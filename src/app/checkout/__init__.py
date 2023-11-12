import mercadopago
from settings import Config


config = Config()

sdk = mercadopago.SDK(config.MERCADO_PAGO_ACCESS_TOKEN)


        # Cria um item na preferência
preference_data = {
        "items": [
        {
            "id": "item-ID-1234",
            "title": "Meu produto",
            "currency_id": "BRL",
            "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
            "description": "Descrição do Item",
            "category_id": "art",
            "quantity": 1,
            "unit_price": 75.76
        }
    ],
    "payer": {
        "name": "João",
        "surname": "Silva",
        "email": "user@email.com",
        "phone": {
            "area_code": "11",
            "number": "4444-4444"
        },
        "identification": {
            "type": "CPF",
            "number": "19119119100"
        },
        "address": {
            "street_name": "Street",
            "street_number": 123,
            "zip_code": "06233200"
        }
    },
    "back_urls": {
        "success": "https://www.success.com",
        "failure": "http://www.failure.com",
        "pending": "http://www.pending.com"
    },
    "auto_return": "approved",
    "payment_methods": {
        'excluded_payment_methods': [],
        'excluded_payment_types': [],
        'installments': 5
},
    "notification_url": "https://www.your-site.com/ipn",
    "statement_descriptor": "MEUNEGOCIO",
    "external_reference": "Reference_1234",
    "expires": True,
    "expiration_date_from": "2016-02-01T12:00:00.000-04:00",
    "expiration_date_to": "2016-02-28T12:00:00.000-04:00"
    }

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]
    