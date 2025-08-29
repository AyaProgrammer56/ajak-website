# app.py
from flask import Flask, render_template, request, jsonify
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv # <-- زدنا هادي

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# --- الإعدادات الأساسية ---
app = Flask(__name__, template_folder='templates', static_folder='static')

# --- إعدادات SendGrid ---
# دابا الكود كيقرا الأسرار من متغيرات البيئة
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')


# --- المسارات (Routes) ---
@app.route('/')
def index():
    return render_template('index.html')

# دالة مساعدة لإرسال الإيميل
def send_email(subject, recipient, body):
    # كنتأكدو أن الأسرار موجودة قبل منسيفطو
    if not SENDGRID_API_KEY or not SENDER_EMAIL:
        print("ERROR: SENDGRID_API_KEY or SENDER_EMAIL is not set.")
        return False

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=recipient,
        subject=subject,
        html_content=f'<div dir="rtl">{body.replace(os.linesep, "<br>")}</div>'
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# مسار لاستقبال رسائل التواصل
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    subject = f"رسالة تواصل جديدة من {data['fullname']}"
    recipient = SENDER_EMAIL
    
    body = f"""
    <h3>لقد توصلت برسالة جديدة من استمارة التواصل.</h3>
    <p><strong>الاسم الكامل:</strong> {data['fullname']}</p>
    <p><strong>البريد الإلكتروني:</strong> {data['email']}</p>
    <hr>
    <p><strong>الرسالة:</strong></p>
    <p>{data['message']}</p>
    """
    
    if send_email(subject, recipient, body):
        return jsonify({'status': 'success', 'message': 'تم إرسال الرسالة بنجاح!'})
    else:
        return jsonify({'status': 'error', 'message': 'حدث خطأ أثناء الإرسال.'}), 500

# مسار لاستقبال طلبات الدعم
@app.route('/submit_support', methods=['POST'])
def submit_support():
    data = request.get_json()
    subject = "طلب دعم نفسي جديد"
    recipient = SENDER_EMAIL
    
    body = f"""
    <h3>لقد توصلت بطلب دعم نفسي جديد.</h3>
    <p><strong>الاسم:</strong> {data.get('name', 'لم يتم تحديده')}</p>
    <p><strong>معلومات التواصل:</strong> {data['contact']}</p>
    <hr>
    <p><strong>الطلب:</strong></p>
    <p>{data['message']}</p>
    """
    
    if send_email(subject, recipient, body):
        return jsonify({'status': 'success', 'message': 'تم إرسال طلب الدعم بنجاح!'})
    else:
        return jsonify({'status': 'error', 'message': 'حدث خطأ أثناء الإرسال.'}), 500

# مسار لاستقبال الشكايات
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    data = request.get_json()
    subject = f"شكاية جديدة من {data['name']}"
    recipient = SENDER_EMAIL
    
    body = f"""
    <h3>لقد توصلت بشكاية جديدة.</h3>
    <p><strong>الاسم الكامل:</strong> {data['name']}</p>
    <p><strong>معلومات التواصل:</strong> {data['contact']}</p>
    <p><strong>موضوع الشكاية:</strong> {data['subject']}</p>
    <hr>
    <p><strong>التفاصيل:</strong></p>
    <p>{data['message']}</p>
    """
    
    if send_email(subject, recipient, body):
        return jsonify({'status': 'success', 'message': 'تم إرسال الشكاية بنجاح!'})
    else:
        return jsonify({'status': 'error', 'message': 'حدث خطأ أثناء الإرسال.'}), 500


# --- تشغيل التطبيق ---
if __name__ == '__main__':
    app.run(debug=False)
