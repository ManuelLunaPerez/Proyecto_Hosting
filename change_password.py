# -*- coding: utf-8 -*-
import sys
import os
import string
import commands
import MySQLdb


usuario = sys.argv[1]
opcion = sys.argv[2]
newpass = sys.argv[3]


exisusuario = commands.getoutput("if [ -d /var/www/"+usuario+" ]; then echo '1'; else echo '0'; fi")

if exisusuario == '1':
	if opcion == '-sql':
		conexion = MySQLdb.connect(host="localhost", user="root", passwd="root", db="mysql")
		cursor=conexion.cursor()
		sql="set password for my"+usuario+"@locahost = '"+newpass+"'"
		cursor.execute(sql)
		conexion.commit()
		conexion.close() 
		print "Contraseña de sql actualizada"
		print "Datos de acceso para MySQL"
		print "Usuario: my"+usuario+""
		print "Contraseña: "+newpass+""
	elif opcion == '-ftp':
else:
	print "El usuario introducido no existe, vuelva a intentarlo";
	exit()
	
