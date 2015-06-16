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
		#Conectamos con la base de datos para realizar una consulta para saber el hash de la contraseña introducida
		conexion = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ftp")
		cursor=conexion.cursor()
		sql="select password('"+newpass+"');"
		cursor.execute(sql)
		resultado=cursor.fetchall() 
		for i in resultado:
			newpass1=i[0]
			
		conexion.commit()
		conexion.close() 
		os.system("mysql -u root -proot -e \"set password for \'my"+usuario+"\'@\'localhost\' =  \'"+newpass1+"\';\"")

		print "Contraseña de sql actualizada"
		print "Datos de acceso para MySQL"
		print "Usuario: my"+usuario+""
		print "Contraseña: "+newpass+""
		exit()
	elif opcion == '-ftp':
		conexion = MySQLdb.connect(host="localhost", user="administrador", passwd="admin", db="ftp")
		cursor=conexion.cursor()
		sql="update usuarios set password ='"+newpass+"' where username='"+usuario+"';"
		cursor.execute(sql)
		conexion.commit()
		conexion.close() 
		print "Contraseña de ftp actualizada"
		print "Datos de acceso para FTP"
		print "Usuario: "+usuario+""
		print "Contraseña: "+newpass+""
		exit()		
else:
	print "El usuario introducido no existe, vuelva a intentarlo";
	exit()
	
