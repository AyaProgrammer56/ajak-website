from flask import Flask, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuration SMTP (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lahraraya@gmail.com'  # Email d'envoi (Ajak)
app.config['MAIL_PASSWORD'] = '12345'  # Mot de passe Gmail ou "App Password"

mail = Mail(app)

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    fullname = data.get('fullname')
    email = data.get('email')
    message = data.get('message')

    # Envoie l'email
    msg = Message(
        subject=f"رسالة جديدة من {fullname} ({email})",
        sender=email,
        recipients=['lahraraya@gmail.com'],  # Email de réception (Ajak)
        body=message
    )
    
    try:
        mail.send(msg)
        return jsonify({"status": "success", "message": "تم إرسال الرسالة بنجاح!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطأ في الإرسال: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

    