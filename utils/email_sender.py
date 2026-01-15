import os
import resend
from datetime import datetime

def send_daily_report(new_questions):
    if not new_questions:
        print("No new questions to email.")
        return

    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        print("Skipping email: Missing RESEND_API_KEY.")
        return

    resend.api_key = api_key
    
    # "onboarding@resend.dev" only works if you verify logic or use their test mode to ONLY your own email.
    # It allows sending to the email registered with Resend account.
    email_from = os.getenv("EMAIL_FROM", "onboarding@resend.dev")
    email_to = os.getenv("EMAIL_TO")
    
    if not email_to:
         print("Skipping email: Missing EMAIL_TO.")
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
    
    params = {
        "from": email_from,
        "to": [email_to],
        "subject": f"【每日精选】Android 面试题更新 ({len(new_questions)}题)",
        "html": html_content
    }

    try:
        email = resend.Emails.send(params)
        print(f"✅ Daily report email sent successfully! ID: {email.get('id')}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
