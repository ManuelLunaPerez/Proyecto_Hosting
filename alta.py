# -*- coding: utf-8 -*-
import sys
import os
import string
import commands
import random
import MySQLdb

usuario = sys.argv[1]
dominio = sys.argv[2]


exisusuario = commands.getoutput("if [ -d /var/www/"+usuario+" ]; then echo '1'; else echo '0'; fi")
exisdominio = commands.getoutput("if [ -f /etc/apache2/sites-available/"+dominio+" ]; then echo '1'; else echo '0'; fi")

if exisusuario == '0' and exisdominio == '0':
	os.system("mkdir /var/www/"+usuario+"")
	os.system("touch /etc/apache2/sites-available/"+dominio+"")
	
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

#Creación del fichero de la zona y configuración

os.system("touch /var/cache/bind/db."+dominio+"")
plantillazonadb = open("plantillas/zonas")
contenidozonas = plantillazonadb.read()
plantillazonadb.close()
ficherozona = open("/var/cache/bind/db."+dominio+"","w")
contenidozonas = contenidozonas.replace('..dom..',dominio)
ficherozona.write(contenidozonas)
ficherozona.close()
os.system("chown bind:bind /var/cache/bind/db."+dominio+"")
os.system("chmod 660 /var/cache/bind/db."+dominio+"")

#Reiniciamos el servicio bind9
os.system("service bind9 restart>/dev/null")

#Creamos  el fichero de configuración del virtualhost de phpmyadmin

os.system("touch /etc/apache2/sites-available/mysql-"+dominio+"")
plantillavhmysql = open("plantillas/vhmysql","r")
contenido3 = plantillavhmysql.read()
plantillavhmysql.close()
vhmysql = open("/etc/apache2/sites-available/mysql-"+dominio+"","w")	
contenido3 = contenido3.replace('..dom..',dominio)
vhmysql.write(contenido3)
vhmysql.close()

os.system ("cd /etc/apache2/sites-available/")
os.system("a2ensite mysql-"+dominio+">/dev/null")
os.system("service apache2 restart>/dev/null")

#ftp
conexion = MySQLdb.connect(host="localhost", user="administrador", passwd="admin", db="ftp")
cursor=conexion.cursor()
sql="select max(uid) from usuarios"
cursor.execute(sql)
resultado=cursor.fetchall() 
for i in resultado:
	maxuid=i[0]
 
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))

passwordftp =id_generator()

if maxuid == None:
	uidnuevo=str("4001")
	nuevousuario = "insert into usuarios values('"+usuario+"','"+passwordftp+"','"+uidnuevo+"','"+uidnuevo+"','/var/www/"+usuario+"','/bin/false1','1','"+dominio+"');"	
	cursor.execute(nuevousuario)
	conexion.commit()
	os.system("chown -R "+uidnuevo+":"+uidnuevo+" /var/www/"+usuario+"")
	conexion.close()

else:
	uidnuevo=int(maxuid)+1
	uidnuevo=str(uidnuevo)
	nuevousuario = "insert into usuario values('"+usuario+"','"+passwordftp+"','"+uidnuevo+"','"+uidnuevo+"','/var/www/"+usuario+"','/bin/false1','1','"+dominio+"');"
	cursor.execute(nuevousuario)
	conexion.commit()
	os.system("chown -R "+uidnuevo+":"+uidnuevo+" /var/www/"+usuario+"")
	conexion.close()



passwordmysql=id_generator()


os.system("mysqladmin -u root -proot create my"+usuario+"")
os.system("mysql -u root -proot -e \"grant all on my"+usuario+".* to \'my"+usuario+"\'@\'localhost\' identified by \'"+passwordmysql+"\';\"")

print "Usuario y dominio creados correctamente"
print "---------------------------------------"
print "Datos de acceso para FTP"
print "Usuario: "+usuario+""
print "Contraseña: "+passwordftp+""
print "---------------------------------------"
print "Datos de acceso para MySQL"
print "Usuario: my"+usuario+""
print "Contraseña: "+passwordmysql+""
