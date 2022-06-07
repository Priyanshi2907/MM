import smtplib,ssl
def SendMail(receiver_email,message):
    smtp_server="smtp.gmail.com"
    port=587
    sender_email="priyanshiprajapati29@gmail.com"
    password="neelu@1234"

    #creat a secure SSl context
    context=ssl.create_default_context()

    #try to log into the server and send email
    try:
        server=smtplib.SMTP(smtp_server,port)

        server.starttls(context=context)  #secure the connection

        server.login(sender_email,password)

        #TODO:send email here
        server.sendmail(sender_email,receiver_email,message)
    except Exception as e:
        #print any errie masg to stdout
       print(e)
    finally:
        server.quit()
