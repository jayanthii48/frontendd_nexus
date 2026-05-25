import requests
from config import *


def send_main_menu(to):

    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "👋 Welcome to Yupro Training"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "course_enquiry",
                            "title": "Courses"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "webinars",
                            "title": "Webinars"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "company_connect",
                            "title": "Company"
                        }
                    }
                ]
            }
        }
    }

    requests.post(url, headers=headers, json=data)


def send_course_buttons(to):

    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "📚 Choose Your Course"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "data_science",
                            "title": "Data Science"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "power_bi",
                            "title": "Power BI"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "python",
                            "title": "Python"
                        }
                    }
                ]
            }
        }
    }

    requests.post(url, headers=headers, json=data)
