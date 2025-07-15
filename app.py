from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration SMTP (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USERNAME', 'lahraraya@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD', 'your_fallback_password')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('GMAIL_USERNAME', 'lahraraya@gmail.com')

mail = Mail(app)

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    fullname = data.get('fullname')
    email = data.get('email')
    message = data.get('message')

    msg = Message(
        subject=f"رسالة جديدة من {fullname} ({email})",
        recipients=['lahraraya@gmail.com'],
        body=message,
        reply_to=email
    )
    
    try:
        mail.send(msg)
        return jsonify({"status": "success", "message": "تم إرسال الرسالة بنجاح!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطأ في الإرسال: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)