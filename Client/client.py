# ----------------------------------------------------------------------------
# Copyright © Lyon e-Sport, 2018
#
# Contributeur(s):
#     * Ortega Ludovic - ludovic.ortega@lyon-esport.fr
#     * Barbou Théo - theobarbou@gmail.com
#     * Dupessy Clément - clement07131@hotmail.fr
#     * Julian Marty - julian.marty83@gmail.com
#
# Ce logiciel, Supervision, est un programme informatique servant à lancer des tests réseaux
# (ping/jitter/packet loss/mos/download/upload) sur des sondes via un site web.
#
# Ce logiciel est régi par la licence CeCILL soumise au droit français et
# respectant les principes de diffusion des logiciels libres. Vous pouvez
# utiliser, modifier et/ou redistribuer ce programme sous les conditions
# de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA
# sur le site "http://www.cecill.info".
#
# En contrepartie de l'accessibilité au code source et des droits de copie,
# de modification et de redistribution accordés par cette licence, il n'est
# offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
# seule une responsabilité restreinte pèse sur l'auteur du programme,  le
# titulaire des droits patrimoniaux et les concédants successifs.
#
# A cet égard  l'attention de l'utilisateur est attirée sur les risques
# associés au chargement,  à l'utilisation,  à la modification et/ou au
# développement et à la reproduction du logiciel par l'utilisateur étant
# donné sa spécificité de logiciel libre, qui peut le rendre complexe à
# manipuler et qui le réserve donc à des développeurs et des professionnels
# avertis possédant  des  connaissances  informatiques approfondies.  Les
# utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
# logiciel à leurs besoins dans des conditions permettant d'assurer la
# sécurité de leurs systèmes et ou de leurs données et, plus généralement,
# à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.
#
# Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
# pris connaissance de la licence CeCILL, et que vous en avez accepté les
# termes.
# ----------------------------------------------------------------------------

import os
import json
import re
import time

import zmq
from functions.ServerZMQ import ServerZMQREP
from functions.ClientZMQ import ClientZMQREQ

regex_ip = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
regex_name = r"^[0-9a-zA-Z -_]{4,20}$"

# get client ZMQ configuration

# get clientZMQ config
config = {
    "name": os.environ.get("PROBE_NAME", None),
    "probe_server": {
        "address": os.environ.get("SERVER_IP", None),
        "port": int(os.environ.get("SERVER_PORT", 0))
    }
}

# overwrite with an external json config file
try:
    with open('config/clientZMQ.json', 'r') as json_data_file:
        config.update(json.load(json_data_file))
except Exception as error:
    pass

# do sanity checks
try:
    if not re.match(regex_name, config["name"]) \
            or not (1 <= config["probe_server"]["port"] <= 65535):
        raise Exception('clientZMQ.json wrong format')
except Exception as error:
    print('Caught this error: ' + repr(error))
    exit()

print(config)

context = zmq.Context()
worker = context.socket(zmq.DEALER)
worker.setsockopt(zmq.IDENTITY, config["name"].encode("utf-8"))
worker.connect("tcp://{}:{}".format(config['probe_server']['address'], config['probe_server']['port']))

client = ClientZMQREQ(worker)
client.start()
server = ServerZMQREP(worker)
server.start()

while True:
    time.sleep(10)