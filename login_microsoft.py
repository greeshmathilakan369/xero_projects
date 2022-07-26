#microsoft login and otp retrival  jul25/22

import email
import imaplib

def login():
    server = 'outlook.office365.com'
    username = 'greeshmathilakan@outlook.com'
    password = 'greeshma369@'

    mail = imaplib.IMAP4_SSL(server, '993')
    mail.login(username, password)
    print("sucess")
    mail.select('inbox')
    otp=''
    retcode, messages = mail.search(None, '(UNSEEN)', '(FROM "greeshma7thilakan@gmail.com")')
    print("rectcode",retcode)
    print("messages",messages)
    #.........................................................................monday

    if retcode == 'OK':
        list_of_mails = messages[0].split()
        print("list of mails=",list_of_mails)   #list of mails= [b'55']

        if list_of_mails:
                typ, data = mail.fetch(max(messages[0].split()), '(RFC822)')
                print("typ=",typ) #typ= OK
                print("data=",data) #here you got the data including verification code ...like...data= [(b'55 (RFC822 {8804}', b'Delivered-To: myob706@gmail.com\r\nReceived: by 2002:a05:6a11:690:0:0:0:0 with SMTP id lr16csp5003881pxb;\r\n        Thu, 21 Jul 2022
                print("hai67")
                for response_part in data:
                    if isinstance(response_part, tuple):  #The isinstance() function returns True if the specified object is of the specified type, otherwise False .
                        raw_email = data[0][1]
                        # print("raw email=",raw_email)
                        print(".........................................................................................................................................")
                        raw_email_string = raw_email.decode('utf-8')
                        email_message = email.message_from_string(raw_email_string)
                        print("email message",email_message)     #json format email but readable
                        print("hello100")

                        for part in email_message.walk():
                            print("hai500")
                            print("part=",part)  #got it

                            if (part.get_content_type() == "text/plain"):
                                print("123")
                            else:
                                print("else part exec")
                                body = part.get_payload(decode=True)
                                print("the body part=",body)
                                print(type(body))
                        msg = list(body.decode('UTF-8'))
                        print("msg=",msg)


                        removetable = str.maketrans('', '', "\r\n-<>:*.',/[] =\t#%;|_")
                        out_msg = [s.translate(removetable) for s in msg]
                        out_msg = [i for i in out_msg if i]
                        listToStr = ''.join(map(str, out_msg))
                        print("list to str=",listToStr)


                        index = listToStr.find('divdir')
                        for i in range(index + 25, index + 29):
                          otp = otp + listToStr[i]
                        print("otp=",otp)



login()    