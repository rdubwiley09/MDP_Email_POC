from views.email_password import pwd

def sendMessage(email, text):
	import smtplib, string

	fromaddr = 'ReformMiDems@gmail.com'
	toaddrs  = email
	subj = "Membership Status"

	msg  = "Hello,"
	msg = msg + "\r\n" + text

	body = str.join("\r\n", (
		"From: %s" % fromaddr,
		"To: %s" % toaddrs,
		"Subject: %s" % subj,
		msg,
	       ))


	# Gmail Login

	username = 'reformmidems@gmail.com'
	password = pwd

	# Sending the mail

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, [toaddrs], body)
	server.quit()
