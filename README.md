The goal of this project is to start tests (ping/jitter/packet loss/mos/download/upload) from a client (can be everything as long as it meets requirements) to a target to monitor networks between the client and the target.

![Application_example.png](https://i.imgur.com/bzOrcxy.png)

# This tool uses :

* [Flask](http://flask.pocoo.org/) - Web microframework
* [Gunicorn](https://gunicorn.org/) - WSGI HTTP Server for UNIX
* [Jinja2](http://jinja.pocoo.org/) - Template engine
* [Bulma](https://bulma.io/) - CSS framework
* [PyZMQ](http://zguide.zeromq.org/py:all) - Python bindings for ØMQ
* [Requests](http://docs.python-requests.org/) - HTTP library

# Requirements

#### Server Python
*  Linux
*  Python 3.6 or newer

#### Client Python
*  Python 3.6 or newer

# Install

Download or clone –> https://github.com/lyon-esport/Supervision.git

Extract the Supervision files

#### Server Python
1. Open a terminal in Server folder

2. Install the requirements: `pip install -r requirements.txt`

3. Create the database `python3 setup.py` to generate the database (database.sqlite will appear)

4. Edit `config/server.json` with the right settings

#### Client Python
1. Open a terminal in Client folder

2. Install the requirements: `pip install -r requirements.txt`

3. Edit `clientZMQ.json` with the right settings

# Start the application

#### Server Python

1. Open a terminal in Server folder

2. Start the server with: `gunicorn  --bind 0.0.0.0:80`

2. Access to the server on `http:myIPAdress:80/` **-> replace myIPAdress by your IP address** 

#### Client Python

1. Open a terminal in Client folder

2. Start the client with `python3 client.py`

# Usage guide

#### Index (Start a test)

1. Standard test

    The probe will start a test and will give you the ping/jitter/packet loss/mos. standard test target can be anything (phone, laptop, server etc...) you just need to put the IP of the device

2. Speedtest

    The probe will start a test and will give you the download and the upload. Speedtest target is an iPerf server you need to put the IP and the Port of the iPerf server you can add iPerf options

3. Autotest

    If checked, the probe will repeat a test each X seconds and will send the result to InfluxDB else the probe will do one test and will save it in the local database

4. Comment

    You can write what you want, this field is often used to write a comment about the test performed

#### Setting (Add/edit/delete a server)

If you want to save time, you can save `Standard test` and `Speedtest` server.

#### Archive (See and manage your test)

You have two type of test : `test` and `autotest`

`test` will be saved in a local database (sqlite) and will be visible on archive page

`autotest` will be saved in InfluxDB database

#### Autotest (Delete autotest)

You can see all autotest launched and you stop them.

## HTTP request InfluxDB

#### For standard test

packet number-> `packet_number,probe=<probe_name> value=<packet_number>`

packet timeout-> `packet_timeout,probe=<probe_name> value=<packet_timeout>`

ping -> `ping,probe=<probe_name> min=<min_ping>, max=<max_ping>, avg=<average_ping>`

jitter -> `jitter,probe=<probe_name> value=<jitter_value>`

packet_loss -> `packet_loss,probe=<probe_name> number=<pack_loss_number>, percent=<packet_loss_percent>`

mos -> `mos,probe=<probe_name> value=<mos_value>`

#### For speedtest

download -> `download,probe=<probe_name> min=<min_download>, max=<max_download>, avg=<average_download>`

upload -> `upload,probe=<probe_name> min=<min_upload>, max=<max_upload>, avg=<average_upload>`

speedtest option-> `speedtest_option,probe=<probe_name> value=<speedtest_option>`

#### For standard test and speedtest

comment -> `comment,probe=<probe_name> value=<test_comment>`

# Licence

The code is under CeCILL license.

You can find all details here: http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Lyon e-Sport, 2018

Contributor(s):

-Ortega Ludovic - ludovic.ortega@lyon-esport.fr

-Barbou Théo - theobarbou@gmail.com

-Dupessy Clément - clement07131@hotmail.fr

-Julian Marty - julian.marty83@gmail.com
