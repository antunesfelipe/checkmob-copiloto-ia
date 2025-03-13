import base64
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email.utils import make_msgid

from onyx.configs.app_configs import EMAIL_CONFIGURED
from onyx.configs.app_configs import EMAIL_FROM
from onyx.configs.app_configs import SMTP_PASS
from onyx.configs.app_configs import SMTP_PORT
from onyx.configs.app_configs import SMTP_SERVER
from onyx.configs.app_configs import SMTP_USER
from onyx.configs.app_configs import WEB_DOMAIN
from onyx.configs.constants import AuthType
from onyx.configs.constants import ONYX_DEFAULT_APPLICATION_NAME
from onyx.configs.constants import ONYX_SLACK_URL
from onyx.configs.constants import TENANT_ID_COOKIE_NAME
from onyx.db.engine import get_session_with_shared_schema
from onyx.db.models import User
from onyx.file_store.onyx_file_store import OnyxFileStore
from onyx.utils.file import OnyxFile
from onyx.utils.variable_functionality import fetch_versioned_implementation
from shared_configs.configs import MULTI_TENANT

HTML_EMAIL_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width" />
  <title>{title}</title>
  <style>
    body, table, td, a {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      text-size-adjust: 100%;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
      -webkit-text-size-adjust: none;
    }}
    body {{
      background-color: #f7f7f7;
      color: #333;
    }}
    .body-content {{
      color: #333;
    }}
    .email-container {{
      width: 100%;
      max-width: 600px;
      margin: 0 auto;
      background-color: #ffffff;
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid #eaeaea;
    }}
    .header {{
      background-color: #000000;
      padding: 20px;
      text-align: center;
    }}
    .header img {{
      max-width: 140px;
    }}
    .body-content {{
      padding: 20px 30px;
    }}
    .title {{
      font-size: 20px;
      font-weight: bold;
      margin: 0 0 10px;
    }}
    .message {{
      font-size: 16px;
      line-height: 1.5;
      margin: 0 0 20px;
    }}
    .cta-button {{
      display: inline-block;
      padding: 12px 20px;
      background-color: #000000;
      color: #ffffff !important;
      text-decoration: none;
      border-radius: 4px;
      font-weight: 500;
    }}
    .footer {{
      font-size: 13px;
      color: #6A7280;
      text-align: center;
      padding: 20px;
    }}
    .footer a {{
      color: #6b7280;
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <table role="presentation" class="email-container" cellpadding="0" cellspacing="0">
    <tr>
      <td class="header">
        <img
          style="background-color: #ffffff; border-radius: 8px;"
          src="data:{logo_mimetype};base64,{logo_b64}"
          alt="{application_name} Logo"
        >
      </td>
    </tr>
    <tr>
      <td class="body-content">
        <h1 class="title">{heading}</h1>
        <div class="message">
          {message}
        </div>
        {cta_block}
      </td>
    </tr>
    <tr>
      <td class="footer">
        © {year} {application_name}. All rights reserved.
        {slack_fragment}
      </td>
    </tr>
  </table>
</body>
</html>
"""


def build_html_email(
    application_name: str | None,
    heading: str,
    message: str,
    logo: bytes,
    logo_mimetype: str,
    cta_text: str | None = None,
    cta_link: str | None = None,
) -> str:
    slack_fragment = ""
    if application_name != ONYX_DEFAULT_APPLICATION_NAME:
        slack_fragment = f'<br>Have questions? Join our Slack community <a href="{ONYX_SLACK_URL}">here</a>.'

    if cta_text and cta_link:
        cta_block = f'<a class="cta-button" href="{cta_link}">{cta_text}</a>'
    else:
        cta_block = ""
    return HTML_EMAIL_TEMPLATE.format(
        application_name=application_name,
        title=heading,
        heading=heading,
        message=message,
        logo=base64.b64encode(logo),
        logo_mimetype=logo_mimetype,
        cta_block=cta_block,
        slack_fragment=slack_fragment,
        year=datetime.now().year,
    )


def send_email(
    user_email: str,
    subject: str,
    html_body: str,
    text_body: str,
    mail_from: str = EMAIL_FROM,
) -> None:
    if not EMAIL_CONFIGURED:
        raise ValueError("Email is not configured.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["To"] = user_email
    if mail_from:
        msg["From"] = mail_from
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="onyx.app")

    part_text = MIMEText(text_body, "plain")
    part_html = MIMEText(html_body, "html")

    msg.attach(part_text)
    msg.attach(part_html)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
    except Exception as e:
        raise e


def send_subscription_cancellation_email(user_email: str) -> None:
    """This is templated but isn't meaningful for whitelabeling."""

    # Example usage of the reusable HTML
    try:
        load_runtime_settings_fn = fetch_versioned_implementation(
            "onyx.server.enterprise_settings.store", "load_runtime_settings"
        )
        settings = load_runtime_settings_fn()
        application_name = settings.application_name
    except ModuleNotFoundError:
        application_name = ONYX_DEFAULT_APPLICATION_NAME

    with get_session_with_shared_schema() as db_session:
        get_onyx_file_store_fn = fetch_versioned_implementation(
            "onyx.file_store.onyx_file_store", "get_onyx_file_store"
        )
        file_store: OnyxFileStore = get_onyx_file_store_fn(db_session)
        onyx_file = file_store.get_logo()

    subject = f"Your {application_name} Subscription Has Been Canceled"
    heading = "Subscription Canceled"
    message = (
        "<p>We're sorry to see you go.</p>"
        "<p>Your subscription has been canceled and will end on your next billing date.</p>"
        "<p>If you change your mind, you can always come back!</p>"
    )
    cta_text = "Renew Subscription"
    cta_link = "https://www.onyx.app/pricing"
    html_content = build_html_email(
        application_name,
        heading,
        message,
        onyx_file.data,
        onyx_file.mime_type,
        cta_text,
        cta_link,
    )
    text_content = (
        "We're sorry to see you go.\n"
        "Your subscription has been canceled and will end on your next billing date.\n"
        "If you change your mind, visit https://www.onyx.app/pricing"
    )
    send_email(user_email, subject, html_content, text_content)


def send_user_email_invite(
    user_email: str, current_user: User, auth_type: AuthType
) -> None:
    onyx_file: OnyxFile | None = None

    try:
        load_runtime_settings_fn = fetch_versioned_implementation(
            "onyx.server.enterprise_settings.store", "load_runtime_settings"
        )
        settings = load_runtime_settings_fn()
        application_name = settings.application_name
    except ModuleNotFoundError:
        application_name = ONYX_DEFAULT_APPLICATION_NAME

    with get_session_with_shared_schema() as db_session:
        get_onyx_file_store_fn = fetch_versioned_implementation(
            "onyx.file_store.onyx_file_store", "get_onyx_file_store"
        )
        file_store: OnyxFileStore = get_onyx_file_store_fn(db_session)
        onyx_file = file_store.get_logo()

    subject = f"Invitation to Join {application_name} Organization"
    heading = "You've Been Invited!"

    # the exact action taken by the user, and thus the message, depends on the auth type
    message = f"<p>You have been invited by {current_user.email} to join an organization on {application_name} .</p>"
    if auth_type == AuthType.CLOUD:
        message += (
            "<p>To join the organization, please click the button below to set a password "
            "or login with Google and complete your registration.</p>"
        )
    elif auth_type == AuthType.BASIC:
        message += (
            "<p>To join the organization, please click the button below to set a password "
            "and complete your registration.</p>"
        )
    elif auth_type == AuthType.GOOGLE_OAUTH:
        message += (
            "<p>To join the organization, please click the button below to login with Google "
            "and complete your registration.</p>"
        )
    elif auth_type == AuthType.OIDC or auth_type == AuthType.SAML:
        message += (
            "<p>To join the organization, please click the button below to"
            " complete your registration.</p>"
        )
    else:
        raise ValueError(f"Invalid auth type: {auth_type}")

    cta_text = "Join Organization"
    cta_link = f"{WEB_DOMAIN}/auth/signup?email={user_email}"

    html_content = build_html_email(
        application_name,
        heading,
        message,
        onyx_file.data,
        onyx_file.mime_type,
        cta_text,
        cta_link,
    )

    # text content is the fallback for clients that don't support HTML
    # not as critical, so not having special cases for each auth type
    text_content = (
        f"You have been invited by {current_user.email} to join an organization on {application_name}.\n"
        "To join the organization, please visit the following link:\n"
        f"{WEB_DOMAIN}/auth/signup?email={user_email}\n"
    )
    if auth_type == AuthType.CLOUD:
        text_content += "You'll be asked to set a password or login with Google to complete your registration."

    send_email(user_email, subject, html_content, text_content)


def send_forgot_password_email(
    user_email: str,
    token: str,
    tenant_id: str,
    mail_from: str = EMAIL_FROM,
) -> None:
    # Builds a forgot password email with or without fancy HTML
    try:
        load_runtime_settings_fn = fetch_versioned_implementation(
            "onyx.server.enterprise_settings.store", "load_runtime_settings"
        )
        settings = load_runtime_settings_fn()
        application_name = settings.application_name
    except ModuleNotFoundError:
        application_name = ONYX_DEFAULT_APPLICATION_NAME

    with get_session_with_shared_schema() as db_session:
        get_onyx_file_store_fn = fetch_versioned_implementation(
            "onyx.file_store.onyx_file_store", "get_onyx_file_store"
        )
        file_store: OnyxFileStore = get_onyx_file_store_fn(db_session)
        onyx_file = file_store.get_logo()

    subject = f"{application_name} Forgot Password"
    link = f"{WEB_DOMAIN}/auth/reset-password?token={token}"
    if MULTI_TENANT:
        link += f"&{TENANT_ID_COOKIE_NAME}={tenant_id}"
    message = f"<p>Click the following link to reset your password:</p><p>{link}</p>"
    html_content = build_html_email(
        application_name,
        "Reset Your Password",
        message,
        onyx_file.data,
        onyx_file.mime_type,
    )
    text_content = f"Click the following link to reset your password: {link}"
    send_email(user_email, subject, html_content, text_content, mail_from)


def send_user_verification_email(
    user_email: str,
    token: str,
    mail_from: str = EMAIL_FROM,
) -> None:
    # Builds a verification email
    try:
        load_runtime_settings_fn = fetch_versioned_implementation(
            "onyx.server.enterprise_settings.store", "load_runtime_settings"
        )
        settings = load_runtime_settings_fn()
        application_name = settings.application_name
    except ModuleNotFoundError:
        application_name = ONYX_DEFAULT_APPLICATION_NAME

    with get_session_with_shared_schema() as db_session:
        get_onyx_file_store_fn = fetch_versioned_implementation(
            "onyx.file_store.onyx_file_store", "get_onyx_file_store"
        )
        file_store: OnyxFileStore = get_onyx_file_store_fn(db_session)
        onyx_file = file_store.get_logo()

    subject = f"{application_name} Email Verification"
    link = f"{WEB_DOMAIN}/auth/verify-email?token={token}"
    message = (
        f"<p>Click the following link to verify your email address:</p><p>{link}</p>"
    )
    html_content = build_html_email(
        application_name,
        "Verify Your Email",
        message,
        onyx_file.data,
        onyx_file.mime_type,
    )
    text_content = f"Click the following link to verify your email address: {link}"
    send_email(user_email, subject, html_content, text_content, mail_from)
