from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGridManager:
    def __init__(self):
        self.sg = SendGridAPIClient('your_sendgrid_api_key_here')
        self.from_email = 'noreply@ai-image-model-maker.com'

    def send_email(self, to_email, subject, content):
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content)
        try:
            response = self.sg.send(message)
            print(f"Email sent. Status code: {response.status_code}")
            return response.status_code
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return None

    def send_welcome_email(self, to_email, name):
        subject = "Welcome to AI Image Model Maker"
        content = f"Hello {name},<br><br>Welcome to AI Image Model Maker! We're excited to have you on board. Once it has finished training, you can interact with it at the link provided in the next email."
        return self.send_email(to_email, subject, content)

    def send_model_ready_email(self, user_id):
        subject = "Your AI Model is Ready!"
        content = f"Great news! Your AI model has finished training and is now ready to use. You can start interacting with it at this link: https://ai-image-model-maker.com/chat/{user_id}"
        return self.send_email(f"{user_id}@example.com", subject, content)