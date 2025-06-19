import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from fastapi import HTTPException
import logging

load_dotenv()

logger = logging.getLogger(__name__)

async def SendRecoveryEmail(email_to: str, token: str):
    # Sends a password recovery email with reset link to the specified email address
    
    # Load environment variables for email configuration
    mail_from = os.getenv("MAIL_FROM")
    mail_server = os.getenv("MAIL_SERVER")
    mail_port = os.getenv("MAIL_PORT")
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")

    # Validate all required environment variables are set
    missing_vars = [
        var for var in ["MAIL_FROM", "MAIL_SERVER", "MAIL_PORT", "MAIL_USERNAME", "MAIL_PASSWORD"]
        if not os.getenv(var)
    ]
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        raise HTTPException(
            status_code=500,
            detail=f"Missing environment variables: {', '.join(missing_vars)}"
        )

    # Construct the email message with reset link
    message = EmailMessage()
    message["From"] = mail_from
    message["To"] = email_to
    message["Subject"] = "Password Reset Request"

    # Create reset link with token
    reset_link = f"http://localhost:5173/reset-password?token={token}"
    message.set_content(f"""
    Hello,

    You requested a password reset. Please click the link below to reset your password:

    {reset_link}

    This link will expire in 15 minutes.

    If you didn't request this, please ignore this email.

    Best regards,
    Auth System
    """)

    # Attempt to send the email using SMTP
    try:
        await aiosmtplib.send(
            message,
            hostname=mail_server,
            port=int(mail_port),
            username=mail_username,
            password=mail_password,
            start_tls=True,
        )
    except aiosmtplib.SMTPException as e:
        logger.error(f"SMTP error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"SMTP error: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
