import requests
import config


def send_webinar_flow(to):

    url = f"https://graph.facebook.com/v23.0/{config.PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {config.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "flow",
            "header": {
                "type": "text",
                "text": "Webinar Registration"
            },
            "body": {
                "text": "Please fill the registration form"
            },
            "footer": {
                "text": "Yupro Training"
            },
            "action": {
                "name": "flow",
                "parameters": {
                    "flow_message_version": "3",
                    "flow_token": "unused",
                    "flow_id": config.FLOW_ID,
                    "flow_cta": "Open Form"
                }
            }
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print(response.status_code)
    print(response.json())