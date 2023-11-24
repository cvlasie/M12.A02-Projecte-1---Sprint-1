import smtplib, ssl
from email.message import EmailMessage
from email.utils import formataddr
import secrets

class MailManager:

    def init_app(self, app):
        # agafo els paràmetres de configuració
        self.sender_name = app.config.get('MAIL_SENDER_NAME')
        self.sender_addr = app.config.get('MAIL_SENDER_ADDR')
        self.sender_password = app.config.get('MAIL_SENDER_PASSWORD')
        self.smtp_server = app.config.get('MAIL_SMTP_SERVER')
        self.smtp_port = app.config.get('MAIL_SMTP_PORT')
 
        # els missatges de contacte s'envien a aquesta adreça
        self.contact_addr = app.config.get('CONTACT_ADDR')

        # URL del servidor web
        self.external_url = app.config.get('EXTERNAL_URL')

    # https://realpython.com/python-send-email/#option-2-using-starttls
    def send_welcome_msg(self, email, name):
        token = secrets.token_urlsafe(20)
        verification_url = f"{self.external_url}/verify/{name}/{token}"

        subject = "Benvingut/da a l'aplicació"
        content = f"""Benvingut/da, {name}!

Gràcies per registrar-te a l'aplicació. Per verificar la teva adreça de correu, si us plau, segueix aquest enllaç:

{verification_url}

Si no has sol·licitat aquest registre, si us plau, ignora aquest correu.

Salutacions,
{self.sender_name}
        """

        self.__send_mail(
            dst_name=name,
            dst_addr=email,
            subject=subject,
            content=content
        )

    def send_verification_msg(self, name, email, token):
        verification_url = f"{self.external_url}/verify/{name}/{token}"

        subject = "Verificació de l'adreça de correu"
        content = f"""Hola, {name}!

Per verificar la teva adreça de correu, si us plau, segueix aquest enllaç:

{verification_url}

Salutacions,
{self.sender_name}
        """

        self.__send_mail(
            dst_name=name,
            dst_addr=email,
            subject=subject,
            content=content
        )

    # https://realpython.com/python-send-email/#option-2-using-starttls
    def send_contact_msg(self, msg):
        subject = "Missatge de contacte"
        content = f"""Missatge de contacte rebut:

{msg}

Enviat des de {self.external_url}        
        """

        self.__send_mail(
            dst_name="Receptor/a de contacte",
            dst_addr=self.contact_addr,
            subject=subject,
            content=content
        )

    # https://realpython.com/python-send-email/#option-2-using-starttls
    def __send_mail(self, dst_name, dst_addr, subject, content):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.sender_addr, self.sender_password)

            msg = EmailMessage()
            msg['From'] = formataddr((self.sender_name, self.sender_addr))
            msg['To'] = formataddr((dst_name, dst_addr))
            msg['Subject'] = subject
            msg.set_content(content)

            server.send_message(msg, from_addr=self.sender_addr, to_addrs=dst_addr)
