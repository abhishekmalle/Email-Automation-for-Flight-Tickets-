import smtplib

smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.ehlo()
smtp_server.starttls()
email = 'flightsaleresponse@gmail.com'
apppwd = 'kxgrfartdbtkdubf'
smtp_server.login(email, apppwd)
toaddr = 'abhishekmalle@gmail.com'
msg = "\r\n".join([
    "From: flightsaleresponse@gmail.com",
    "To: abhishekmalle@gmail.com",
    "Subject: Test123",
    "Test234",
    "Test345"
    ])
smtp_server.sendmail(email, toaddr, msg)