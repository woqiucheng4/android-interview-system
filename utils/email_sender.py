import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import json
from datetime import datetime

def send_daily_report(new_questions):
    if not new_questions:
        print("No new questions to email.")
        return

    email_host = os.getenv("EMAIL_HOST", "smtp.qq.com")
    email_port = int(os.getenv("EMAIL_PORT", 465))
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASSWORD")
    email_to = os.getenv("EMAIL_TO")

    if not all([email_user, email_pass, email_to]):
        print("Skipping email: Missing EMAIL_USER, EMAIL_PASSWORD, or EMAIL_TO.")
        return

    # Build HTML Content
    html_content = f"""
    <html>
    <body>
        <h2>📅 Android 面试题库日报 ({datetime.now().strftime('%Y-%m-%d')})</h2>
        <p>今日新增 <b>{len(new_questions)}</b> 道面试题：</p>
        <hr/>
    """

    for idx, q in enumerate(new_questions, 1):
        html_content += f"""
        <div style="margin-bottom: 20px; padding: 15px; background-color: #f9f9f9; border-radius: 8px;">
            <h3 style="color: #333;">{idx}. {q['question']} <span style="font-size: 12px; color: #666; background: #eee; padding: 2px 6px; border-radius: 4px;">{q['level']}</span></h3>
            <p><strong>Category:</strong> {q['category']}</p>
            <div style="background: #fff; padding: 10px; border-left: 4px solid #4caf50;">
                <strong>参考答案:</strong><br/>
                {q['answer'].replace(chr(10), '<br/>')}
            </div>
        </div>
        """

    html_content += """
        <hr/>
        <p style="font-size: 12px; color: #888;">此邮件由 Android Interview System 自动生成。</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Subject'] = Header(f"【每日精选】Android 面试题更新 ({len(new_questions)}题)", 'utf-8')
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        if email_port == 465:
            server = smtplib.SMTP_SSL(email_host, email_port)
        else:
            server = smtplib.SMTP(email_host, email_port)
            server.starttls()
            
        server.login(email_user, email_pass)
        server.sendmail(email_user, [email_to], msg.as_string())
        server.quit()
        print("✅ Daily report email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
