from easygui import multenterbox
from easygui import msgbox

msg = "Ingresa tu usuario y contraseña del SIU"
title = "Ingreso SIU Guarani"
fieldNames = ["Usuario", "Contraseña"]
fieldValues = multenterbox(msg, title, fieldNames)
while 1:
    errmsg = ""
    for i, name in enumerate(fieldNames):
        if fieldValues[i].strip() == "":
          errmsg += "{} es un campo necesario.\n\n".format(name)
    if errmsg == "":
        break # sin problemas
    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    if fieldValues is None:
        break
print(f"Reply was:{fieldValues}")

msgbox("Se han completado las encuestas")