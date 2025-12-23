"""
Email service using Resend API for transactional emails.
"""

from typing import Optional
import os
import httpx


class EmailService:
    """Email service for sending transactional emails via Resend."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize email service.

        Args:
            api_key: Resend API key (defaults to RESEND_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("RESEND_API_KEY")
        self.from_email = os.getenv("RESEND_FROM_EMAIL", "noreply@yourdomain.com")
        self.api_url = "https://api.resend.com/emails"

    async def send_verification_email(
        self,
        to_email: str,
        username: str,
        verification_url: str
    ) -> bool:
        """
        Send email verification email.

        Args:
            to_email: Recipient email address
            username: User's display name
            verification_url: Verification URL

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.api_key:
            print("Email API key not configured, skipping email send")
            return False

        subject = "Verify your email address"
        html_content = f"""
        <h2>Welcome to the AI-Native Textbook Platform!</h2>
        <p>Hi {username},</p>
        <p>Thank you for signing up. Please verify your email address by clicking the link below:</p>
        <p><a href="{verification_url}">Verify Email Address</a></p>
        <p>This link will expire in 24 hours.</p>
        <p>If you didn't create an account, you can safely ignore this email.</p>
        """

        return await self._send_email(to_email, subject, html_content)

    async def send_password_reset_email(
        self,
        to_email: str,
        username: str,
        reset_url: str
    ) -> bool:
        """
        Send password reset email.

        Args:
            to_email: Recipient email address
            username: User's display name
            reset_url: Password reset URL

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.api_key:
            print("Email API key not configured, skipping email send")
            return False

        subject = "Reset your password"
        html_content = f"""
        <h2>Password Reset Request</h2>
        <p>Hi {username},</p>
        <p>We received a request to reset your password. Click the link below to reset it:</p>
        <p><a href="{reset_url}">Reset Password</a></p>
        <p>This link will expire in 1 hour.</p>
        <p>If you didn't request a password reset, you can safely ignore this email.</p>
        """

        return await self._send_email(to_email, subject, html_content)

    async def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ) -> bool:
        """
        Send email via Resend API.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: Email HTML content

        Returns:
            True if successful, False otherwise
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "from": f"AI Textbook Platform <{self.from_email}>",
            "to": [to_email],
            "subject": subject,
            "html": html_content
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )

                if response.status_code == 200:
                    print(f"Email sent successfully to {to_email}")
                    return True
                else:
                    print(f"Failed to send email: {response.status_code} {response.text}")
                    return False

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    async def health_check(self) -> bool:
        """Check if email service is accessible."""
        return self.api_key is not None


# Global email service instance
email_service = EmailService()
