# -*- coding: utf-8 -*-
import sys
import os
import string
import commands
import MySQLdb

usuario = sys.argv[1]
dominio = sys.argv[2]


exisusuario = commands.getoutput("if [ -d /var/www/"+usuario+" ]; then echo '1'; else echo '0'; fi")
exisdominio = commands.getoutput("if [ -f /etc/apache2/sites-available/"+dominio+" ]; then echo '1'; else echo '0'; fi")

if exisusuario == '0' and exisdominio == '0':
	os.system("mkdir /var/www/"+usuario+"")
	os.system("touch /etc/apache2/sites-available/"+dominio+"")
	print "Usuario y dominio creados satisfactoriamente";
	
elif  exisusuario == '1' and exisdominio == '0':
	print "El usuario introducido ya existe";
	exit()
	
elif  exisusuario == '0' and exisdominio == '1':
	print "El dominio introducido ya está siendo utilizado por otro usuario";
	exit()
	
else:
	print "El usuario y el dominio introducido ya están siendo utilizados";
	exit()
	
#Creación del index automático
plantillaindex = open("plantillas/index.html","r")
contenido = plantillaindex.read()
plantillaindex.close()
os.system("touch /var/www/"+usuario+"/index.html")
creacionindex = open("/var/www/"+usuario+"/index.html","w")
contenido = contenido.replace('..dom..',dominio)
creacionindex.write(contenido)
creacionindex.close()

#Creacion del virtual host automático
plantillavh = open("plantillas/virtualhost","r")
contenido2 = plantillavh.read()
plantillavh.close()
ficherovh = open("/etc/apache2/sites-available/"+dominio+"","w")
contenido2 = contenido2.replace('..dom..',dominio)
contenido2 = contenido2.replace('..usuario..',usuario)
ficherovh.write(contenido2)
ficherovh.close()

os.system ("cd /etc/apache2/sites-available/")
os.system("a2ensite "+dominio+">/dev/null")

#Reinicio del servicio apache2
os.system("service apache2 restart>/dev/null")

#Insrección de nuevas zonas
introducir = '\nzone "'+dominio+'"{\ntype master;\nfile "db.'+dominio+'";\n};'
ficheroconf = open("/etc/bind/named.conf.local","a")
ficheroconf.write(introducir)
ficheroconf.close()

	
