##Insertar temporalmente 

import sys
import os

## Insertar en la sesión actual
currentDirectory = os.getcwd()

sys.path.insert(0, currentDirectory)

print(sys.path)

##Insertar en las variables de entorno

with open("/home/ale/.bashrc", "a") as f:
    f.write("export PYTHONPATH=$PYTHONPATH:"+currentDirectory+"\n")

## Agregar por shell
## echo "export PYTHONPATH=$PYTHONPATH:/home/ale/workspace/odoo-dev/customaddons/l10n_ec_sa" | tee -a /home/ale/.bashrc
