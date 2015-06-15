# -*- coding: utf-8 -*-
import sys
import os
import string
import commands
import MySQLdb

usuario = sys.argv[1]
dominio = sys.argv[2]

exisusuario= commands.getoutput("if [ -d /var/www/"+usuario+" ]; then echo '1'; else echo '0'; fi")
exisdominio = commands.getoutput("if [ -f /etc/apache2/sites-available/"+dominio+" ]; then echo '1'; else echo '0'; fi")

if exisusuario == '1' and exisdominio == '1':
	os.system("rm -r /var/www/"+usuario+"")
	print "Usuario y dominio borrados satisfactoriamente";
	
elif  exisusuario == '0' and exisdominio == '1':
	print "El usuario introducido no existe";
	exit()
	
elif  exisusuario == '1' and exisdominio == '0':
	print "El dominio introducido no existe";
	exit()
	
else:
	print "El usuario y el dominio introducidos no existen";
	exit()

os.system("a2dissite " +dominio+">/dev/null")
os.system("rm /etc/apache2/sites-available/"+dominio+"")
