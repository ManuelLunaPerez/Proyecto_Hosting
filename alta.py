# -*- coding: utf-8 -*-
import sys
import os
import string
import commands
import MySQLdb

usuario = sys.argv[1]
dominio = sys.argv[2]

exisdirectorio = commands.getoutput("if [ -d /var/www/"+usuario+" ]; then echo '1'; else echo '0'; fi")
exisdominio = commands.getoutput("if [ -f /etc/apache2/sites-available/"+dominio+" ]; then echo '1'; else echo '0'; fi")

if exisdirectorio == '0' and exisdominio == '0':
	os.system("mkdir /var/www/"+usuario+"")
	os.system("touch /etc/apache2/sites-available/"+dominio+"")
	print "Usuario y dominio creados satisfactoriamente";
	
elif  exisdirectorio == '1' and exisdominio == '0':
	print "El usuario introducido ya existe";
	
elif  exisdirectorio == '0' and exisdominio == '1':
	print "El dominio introducido ya está siendo utilizado";
	
else:
	print "El usuario y el dominio introducido ya están siendo utilizados";
	exit()
	

	
