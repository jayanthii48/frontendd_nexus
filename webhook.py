from flask import Blueprint, request
from send_flow import send_webinar_flow
from db import get_connection
from send_message import *
from config import VERIFY_TOKEN
import json

webhook = Blueprint('webhook', __name__)


@webhook.route('/webhook', methods=['GET'])
def verify():

    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge

    return "Verification failed"


@webhook.route('/webhook', methods=['POST'])
def receive_message():

    data = request.json

    try:

        value = data['entry'][0]['changes'][0]['value']

        # ignore non-message events
        if 'messages' not in value:
            return "ok", 200

        message = value['messages'][0]
        number = message['from']

        cursor = get_connection().cursor()

        # -----------------------------
        # USER CREATION / FETCH
        # -----------------------------
        cursor.execute(
            "SELECT * FROM users WHERE whatsapp_number=%s",
            (number,)
        )

        user = cursor.fetchone()

        if not user:
            cursor.execute(
                "INSERT INTO users (whatsapp_number) VALUES (%s)",
                (number,)
            )
            get_connection().commit()

            cursor.execute(
                "SELECT * FROM users WHERE whatsapp_number=%s",
                (number,)
            )

            user = cursor.fetchone()

        user_id = user['id']

        # -----------------------------
        # TEXT MESSAGE FLOW
        # -----------------------------
        if message['type'] == 'text':

            text = message['text']['body']

            cursor.execute(
                "INSERT INTO messages (user_id, sender, message) VALUES (%s,%s,%s)",
                (user_id, 'user', text)
            )
            get_connection().commit()

            # MAIN ENTRY POINT
            if text.lower() in ["hi", "hello", "start"]:

                send_main_menu(number)

            elif text.lower() == "webinar":

                send_webinar_flow(number)   # optional shortcut

        # -----------------------------
        # BUTTON CLICK FLOW
        # -----------------------------
        elif message['type'] == 'interactive':

            interactive = message['interactive']

            # -----------------------------
            # BUTTON REPLY (normal buttons)
            # -----------------------------
            if 'button_reply' in interactive:

                button_id = interactive['button_reply']['id']

                if button_id == 'course_enquiry':
                    send_course_buttons(number)

                elif button_id == 'data_science':

                    cursor.execute(
                        "INSERT INTO course_enquiries (user_id, course_name) VALUES (%s,%s)",
                        (user_id, 'Data Science')
                    )
                    get_connection().commit()

                elif button_id == 'webinars':
                    send_webinar_flow(number)

            # -----------------------------
            # FLOW RESPONSE (VERY IMPORTANT)
            # -----------------------------
            elif 'nfm_reply' in interactive:

                flow_data = json.loads(
                    interactive['nfm_reply']['response_json']
                )

                name = flow_data.get("name")
                email = flow_data.get("email")
                qualification = flow_data.get("qualification")
                employment = flow_data.get("employment_status")

                # store in DB
                cursor.execute(
                    """
                    INSERT INTO webinar_registrations
                    (whatsapp_number, name, email, qualification, employment_status)
                    VALUES (%s,%s,%s,%s,%s)
                    """,
                    (number, name, email, qualification, employment)
                )

                get_connection().commit()
        print("RAW DATA RECEIVED:")
        print(data)

        return "ok", 200

    except Exception as e:
        print("ERROR:", e)
        return "error", 500