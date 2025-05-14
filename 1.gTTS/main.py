import os
from gtts import gTTS
import smtplib
from email.message import EmailMessage

def read_text_file():
    file_path = input("Enter path to file: ")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("File doesn't exist.")
        return None

def text_to_speech(text, output_path):
    tts = gTTS(text=text, lang='uk')
    tts.save(output_path)
    print(f"File was crated at: {output_path}")

def send_email(recipient_email, subject, body, attachment_path):
    sender_email = "pavlikvstaras@gmail.com"
    sender_password = "mxrd snxw ybvz cmjo"
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
    msg.add_attachment(file_data, maintype="audio", subtype="mp3", filename=file_name)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Sent.")
    except Exception as e:
        print(f"Can't send: {e}")

def main():
    text = read_text_file()
    if not text:
        return

    output_path = input("Enter path where mp3 will be saved: ")
    text_to_speech(text, output_path)

    send_to_email = input("Send to your email? (yes/no): ").strip().lower()
    if send_to_email == "yes":
        recipient = input("Enter email: ").strip()
        send_email(
            recipient_email=recipient,
            subject="Your mp3 file",
            body="Here is your mp3 file.",
            attachment_path=output_path
        )

if __name__ == "__main__":
    main()