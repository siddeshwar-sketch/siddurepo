import smtplib

combos = [
    ("sharanprakaspatil70558@gmail.com", "eket qxdq hnbt kuyv"),
    ("sharanprakashpatil70558@gmail.com", "eket qxdq hnbt kuyv"),
    ("sharanprakaspatil70558@gmail.com", "eketqxdqhnbtkuyv"),
    ("sharanprakashpatil70558@gmail.com", "eketqxdqhnbtkuyv"),
]

for user, pwd in combos:
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        print(f"SUCCESS: {user} / {pwd}")
        print("-" * 20)
        server.quit()
    except smtplib.SMTPAuthenticationError as e:
        print(f"FAILED: {user} / {pwd} -> {e}")
