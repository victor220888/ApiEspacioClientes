#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  constante.py

import sys
import os
import platform
import socket


# ~ import os.path, time
# ~ file = 'C:\\Users\\MiTierra\\Desktop\\Documentos\\captura.png'
# ~ print("Ultima modificacion: %s" % time.ctime(os.path.getmtime(file)))
# ~ print("Fecha Creacion     : %s" % time.ctime(os.path.getctime(file)))

# ~ import os, time
# ~ (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
# ~ print("last modified: %s" % time.ctime(mtime))


# ~ print (os.listdir("H:\\scaneados\\Tarjetas de visita"))

SERVER_NAME = 'Oracle'
USER        = 'adcs'
LOGIN       = 'centu'
# ~ SCHEMA      = 'DESA'
SCHEMA      = 'OMEGA'
HOST        = '192.168.13.64'

SERVER_SMTP ='smtp-mail.outlook.com:587'

SENDER_EMAIL_ADDRESS  = 'informatica@mitierra.com.py'
SENDER_EMAIL_PASSWORD = 'rOSIOBRITES2288'

PATH        = os.getcwd()
COLOR_SYS   = "#FFFFFF"

MAQUINA      = socket.gethostname()
SYSTEMA      = platform.system()
ARQUITECTURA = platform.machine()
VERSION_SO   = platform.version()


if sys.platform != 'win32':
    ip = ''

MESES = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Setiembre',
   10: 'Octubre',
   11: 'Noviembre',
   12: 'Diciembre'
}

MESES_NUMERO = {
    'Enero': '01',
    'Febrero': '02',
    'Marzo': '03',
    'Abril': '04',
    'Mayo': '05',
    'Junio': '06',
    'Julio': '07',
    'Agosto': '08',
    'Setiembre': '09',
    'Octubre': '10',
    'Noviembre': '11',
    'Diciembre': '12'
}

DIAS = {
    1: 'Lunes',
    2: 'Martes',
    3: 'Miercoles',
    4: 'Jueves',
    5: 'Viernes',
    6: 'Sabado',
    7: 'Domingo',
}


