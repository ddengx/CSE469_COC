# Storage for environmental variables
# Not sure if the prof wants us to actually add 
# vars to the OS itself or hardcode it like this
# Will work for now LGTB

import os

# Env vars
# AES fot encryption/decryption and opasswords for "creators"
# Use os.environ.get() to access these
os.environ['AES_KEY'] = 'R0chLi4uLi4uLi4='
os.environ['BCHOC_PASSWORD_POLICE'] = 'P80P'
os.environ['BCHOC_PASSWORD_LAWYER'] = 'L76L'
os.environ['BCHOC_PASSWORD_ANALYST'] = 'A65A'
os.environ['BCHOC_PASSWORD_EXECUTIVE'] = 'E69E'
os.environ['BCHOC_PASSWORD_CREATOR'] = 'C67C'