from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

def send_email(subject, body, to_email):
    sender_email = "emailk@gmail.com"          # غير هاد للإيميل ديالك
    sender_password = "password_app_specific"  # غير هاد لكلمة السر أو كلمة سر التطبيق

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        body = f"رسالة من: {name} <{email}>\n\n{message}"
        send_email("رسالة من الموقع", body, "recipient@example.com")  # هنا دخل الإيميل اللي بغيت توصله الرسائل

        return "تم إرسال الرسالة بنجاح!"

    form_html = '''
    <h2>نموذج الاتصال</h2>
    <form method="POST">
      الاسم: <input type="text" name="name" required><br><br>
      الإيميل: <input type="email" name="email" required><br><br>
      الرسالة:<br>
      <textarea name="message" required></textarea><br><br>
      <button type="submit">إرسال</button>
    </form>
    '''
    return render_template_string(form_html)

if __name__ == '__main__':
    app.run(debug=True)
