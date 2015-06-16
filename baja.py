# -*- coding: utf-8 -*-
import sys
import os
import string
import commands
import MySQLdb

dominio = sys.argv[1]

exisdominio = commands.getoutput("if [ -f /etc/apache2/sites-available/"+dominio+" ]; then echo '1'; else echo '0'; fi")

if 	exisdominio == '1':
	#Si existe el dominio procedemos a buscar el nombre de usuario del propietario de dicho dominio
	conexion = MySQLdb.connect(host="localhost", user="administrador", passwd="admin", db="ftp")
	cursor=conexion.cursor()
	sql="select username from usuarios where dominio='"+dominio+"'"
	cursor.execute(sql)
	resultado=cursor.fetchall() 
	for i in resultado:
		usuario=i[0]
	conexion.close()

else:
	print "El dominio introducido no existe";
	exit()

os.system("rm -r /var/www/"+usuario+"")

#Desactivamos el sitio
os.system ("cd /etc/apache2/sites-available/")
os.system("a2dissite "+dominio+">/dev/null")
#Borramos el sitio
os.system("rm /etc/apache2/sites-available/"+dominio+"")
os.system("rm /etc/apache2/sites-available/mysql-"+dominio+"")
#Borramos el fichero de zona
os.system("rm /var/cache/bind/db."+dominio+"")

#Borramos la zona del fichero de configuración
busqueda = commands.getoutput("grep -A1 "+dominio+" /etc/bind/named.conf.local")
ficheroconf = open("/etc/bind/named.conf.local",'r')   
contenido = ficheroconf.read()   
contenido = contenido.replace(busqueda,"")   
ficheroconf.close() 
modificado = open("/etc/bind/named.conf.local",'w')   
modificado.write(contenido)
modificado.close()

#Nos conectamos como root a la base de datos
conexion = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ftp")
cursor=conexion.cursor()
#Borramos el usuario ftp
borrarftp="delete from usuarios where username='"+usuario+"'"
cursor.execute(borrarftp)
conexion.commit()
#Borramos la base de datos
os.system("mysqladmin -u root -proot drop my"+usuario+"")
#Borramos el usuario 
borrarusuario="drop user my"+usuario+"@localhost"
cursor.execute(borrarusuario)
conexion.commit()
conexion.close()

os.system("service apache2 restart>/dev/null")
os.system("service bind9 restart>/dev/null")

print "Borrado correctamente"
