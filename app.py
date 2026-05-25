from flask import Flask, jsonify
from flask_cors import CORS

from webhook import webhook
from db import get_connection

app = Flask(__name__)
CORS(app)

# Register WhatsApp webhook blueprint
app.register_blueprint(webhook)


# =====================================================
# USERS API
# =====================================================
@app.route('/users', methods=['GET'])
def users():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            id,
            whatsapp_number,
            whatsapp_name,
            status,
            created_at
        FROM users
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# =====================================================
# COURSE LEADS API
# =====================================================
@app.route('/course-leads', methods=['GET'])
def course_leads():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            id,
            user_id,
            course_name,
            status,
            created_at
        FROM course_enquiries
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# =====================================================
# WEBINAR LEADS (WHATSAPP FLOWS)
# =====================================================
@app.route('/webinar-leads', methods=['GET'])
def webinar_leads():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            id,
            whatsapp_number,
            name,
            email,
            qualification,
            employment_status,
            created_at
        FROM webinar_registrations
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


# =====================================================
# DASHBOARD STATS API
# =====================================================
@app.route('/dashboard', methods=['GET'])
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    # Total users
    cursor.execute("SELECT COUNT(*) as total_users FROM users")
    users_count = cursor.fetchone()

    # Course leads
    cursor.execute("SELECT COUNT(*) as course_leads FROM course_enquiries")
    course_count = cursor.fetchone()

    # Webinar leads
    cursor.execute("SELECT COUNT(*) as webinar_leads FROM webinar_registrations")
    webinar_count = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify({
        "total_users": users_count["total_users"],
        "course_leads": course_count["course_leads"],
        "webinar_leads": webinar_count["webinar_leads"]
    })


# =====================================================
# HEALTH CHECK (VERY IMPORTANT FOR DEPLOYMENT)
# =====================================================
@app.route('/health', methods=['GET'])
def health():

    return jsonify({
        "status": "running",
        "message": "Flask WhatsApp CRM is working fine"
    })


# =====================================================
# RUN SERVER
# =====================================================
if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )