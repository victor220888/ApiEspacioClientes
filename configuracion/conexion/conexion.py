#!C:\Python37\python.exe
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import sys
from datetime import datetime

import cx_Oracle

def archivo_log(e):
    print ("No se establecio la conexion", "Detalles\nNo se pudo conectar con el servidor de la base de datos\n%s"%e)


def conectar(usuario, login, host_name, service_name, servidor):
    if servidor == 'Oracle':
        # ~ try:
            # ~ print (""+str(usuario)+"/"+"@"+str(host_name)+"/"+str(service_name)+"")
            conex =  cx_Oracle.connect(""+str(usuario)+"/"+str(login)+"@"+str(host_name)+"/"+str(service_name)+"")
            return conex
        # ~ except OSError as err:
            # ~ print("OS error: {0}".format(err))
            # ~ print(""+str(usuario)+"/"+str(login)+"@"+str(host_name)+"/"+str(service_name)+"")
            # ~ return

