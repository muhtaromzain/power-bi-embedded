# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
import json
import binascii
from Crypto.Cipher import AES
from Crypto import Random
import base64

class Utils:

    def check_config(app):
        '''Returns a message to user for missing configuration

        Args:
            app (Flask): Flask app object

        Returns:
            string: Error info
        '''

        if app.config['AUTHENTICATION_MODE'] == '':
            return 'Please specify one of the two authentication modes'
        if app.config['AUTHENTICATION_MODE'].lower() == 'serviceprincipal' and app.config['TENANT_ID'] == '':
            return 'Tenant ID is not provided in the config.py file'
        elif app.config['REPORT_ID'] == '':
            return 'Report ID is not provided in config.py file'
        elif app.config['WORKSPACE_ID'] == '':
            return 'Workspace ID is not provided in config.py file'
        elif app.config['CLIENT_ID'] == '':
            return 'Client ID is not provided in config.py file'
        elif app.config['AUTHENTICATION_MODE'].lower() == 'masteruser':
            if app.config['POWER_BI_USER'] == '':
                return 'Master account username is not provided in config.py file'
            elif app.config['POWER_BI_PASS'] == '':
                return 'Master account password is not provided in config.py file'
        elif app.config['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
            if app.config['CLIENT_SECRET'] == '':
                return 'Client secret is not provided in config.py file'
        elif app.config['SCOPE_BASE'] == '':
            return 'Scope base is not provided in the config.py file'
        elif app.config['AUTHORITY_URL'] == '':
            return 'Authority URL is not provided in the config.py file'
        
        return None

    def check_configuration(app, workspace_id, report_id, tenant_id, client_id, client_secret):
        '''Returns a message to user for missing configuration

        Args:
            app (Flask): Flask app object

        Returns:
            string: Error info
        '''

        if app.config['AUTHENTICATION_MODE'] == '':
            return 'Please specify one of the two authentication modes'
        if app.config['AUTHENTICATION_MODE'].lower() == 'serviceprincipal' and tenant_id == '':
            return 'Tenant ID is not provided in the config.py file'
        elif report_id == '':
            return 'Report ID is not provided in config.py file'
        elif workspace_id == '':
            return 'Workspace ID is not provided in config.py file'
        elif client_id == '':
            return 'Client ID is not provided in config.py file'
        elif app.config['AUTHENTICATION_MODE'].lower() == 'masteruser':
            if app.config['POWER_BI_USER'] == '':
                return 'Master account username is not provided in config.py file'
            elif app.config['POWER_BI_PASS'] == '':
                return 'Master account password is not provided in config.py file'
        elif app.config['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
            if client_secret == '':
                return 'Client secret is not provided in config.py file'
        elif app.config['SCOPE_BASE'] == '':
            return 'Scope base is not provided in the config.py file'
        elif app.config['AUTHORITY_URL'] == '':
            return 'Authority URL is not provided in the config.py file'
        
        return None

    def encrypt_data(data, passphrase):
        """
            Encrypt using AES-256-CBC with random/shared iv
            'passphrase' must be in hex, generate with 'openssl rand -hex 32'
        """
        try:
            key = binascii.unhexlify(passphrase)
            pad = lambda s : s+chr(16-len(s)%16)*(16-len(s)%16)
            iv = Random.get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted_64 = base64.b64encode(cipher.encrypt(pad(data).encode())).decode('ascii')
            iv_64 = base64.b64encode(iv).decode('ascii')
            json_data = {}
            json_data['iv'] = iv_64
            json_data['data'] = encrypted_64
            clean = base64.b64encode(json.dumps(json_data).encode('ascii'))
        except Exception as e:
            print("Cannot encrypt datas...")
            print(e)
            exit(1)
        return clean

    def decrypt_data(data, passphrase):
        """
            Decrypt using AES-256-CBC with iv
            'passphrase' must be in hex, generate with 'openssl rand -hex 32'
            # https://stackoverflow.com/a/54166852/11061370
        """
        try:
            unpad = lambda s : s[:-s[-1]]
            key = binascii.unhexlify(passphrase)
            encrypted = json.loads(base64.b64decode(data).decode('ascii'))
            encrypted_data = base64.b64decode(encrypted['data'])
            iv = base64.b64decode(encrypted['iv'])
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted_data)
            clean = unpad(decrypted).decode('ascii').rstrip()
        except Exception as e:
            print("Cannot decrypt datas...")
            print(e)
            exit(1)
        return clean