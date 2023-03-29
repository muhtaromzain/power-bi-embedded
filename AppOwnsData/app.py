# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from services.pbiembedservice import PbiEmbedService
from utils import Utils
from flask import Flask, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import json
import os
from services.aadservice import AadService

# Initialize the Flask app
app = Flask(__name__)
cors = CORS(app)

# Load configuration
app.config.from_object('config.BaseConfig')

@app.route('/')
def index():
    '''Returns a static HTML page'''

    return render_template('index.html')

@app.route('/getembedinfo/<workspace_id>/<report_id>/<tenant_id>/<client_id>/<client_secret>', methods=['GET'])
@cross_origin()
def get_embed_info(workspace_id, report_id, tenant_id, client_id, client_secret):
    '''Returns report embed configuration'''

    config_result = Utils.check_configuration(app, workspace_id, report_id, tenant_id, client_id, client_secret)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report(workspace_id, report_id, tenant_id, client_id, client_secret)
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

@app.route('/getEmbeddedInfo', methods=['POST'])
@cross_origin()
def getInfo():
    '''Returns report embed configuration'''

    dataJson        = request.json
    encryptedData   = dataJson['data']
    
    # decode response
    decode          = Utils.decrypt_data(encryptedData, app.config['AES_KEY'])
    decodeData      = json.loads(decode)

    workspace_id    = decodeData['workspace_id']
    report_id       = decodeData['report_id']
    tenant_id       = decodeData['tenant_id']
    client_id       = decodeData['client_id']
    client_secret   = decodeData['client_secret']

    config_result = Utils.check_configuration(app, workspace_id, report_id, tenant_id, client_id, client_secret)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report(workspace_id, report_id, tenant_id, client_id, client_secret)
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

@app.route('/favicon.ico', methods=['GET'])
def getfavicon():
    '''Returns path of the favicon to be rendered'''

    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/gettoken', methods=['GET'])
def get_token():
    '''Returns report embed configuration'''

    config_result = Utils.check_config(app)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        # embed_info = PbiEmbedService().get_embed_params_for_single_report(app.config['WORKSPACE_ID'], app.config['REPORT_ID'])
        token = AadService.get_access_token()
        return token
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500


if __name__ == '__main__':
    app.run()