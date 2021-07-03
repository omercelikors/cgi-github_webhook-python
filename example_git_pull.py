#!/usr/bin/python
import os
import hashlib
import hmac
import sys
import paramiko

x_hub_signature_256 = os.environ.get('HTTP_X_HUB_SIGNATURE_256', '')

cont_len = int(os.environ["CONTENT_LENGTH"])
req_body = sys.stdin.read(cont_len)

# call from external file
with open('') as f:
	webhook_key = f.readline().replace('\n','')
	user_pass = f.readline().replace('\n','')

signature = hmac.new(key=webhook_key, msg=req_body, digestmod=hashlib.sha256).hexdigest()

if hmac.compare_digest(signature, x_hub_signature_256.split('sha256=')[-1].strip()):
	hostname = ""
	username = ""

	client = paramiko.SSHClient()

	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		client.connect(hostname=hostname, username=username, password=user_pass)
	except:
		connect_error = "connection error occured"
		print "Content-type:text/html\r\n\r\n"
		print "<html>"
		print "<head>"
		print "<title>CGI Program</title>"
		print "</head>"
		print "<body>"
		print "<h2>Connection Error:%s</h2>" % (connect_error)
		print "</body>"
		print "</html>"
		sys.exit()


	stdin, stdout, stderr = client.exec_command('cd /srv/mini_bzcrawler; git pull')
	s_output = stdout.read().decode()
	s_err = stderr.read().decode()

	print "Content-type:text/html\r\n\r\n"
	print "<html>"
	print "<head>"
	print "<title>CGI Program</title>"
	print "</head>"
	print "<body>"
	print "<h2>Output:%s</h2>" % (s_output)
	print "<h2>Error:%s</h2>" % (s_err)
	print "</body>"
	print "</html>"