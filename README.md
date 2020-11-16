Simple CyberQ data collector, with
[docker-compose](https://github.com/docker/compose/) stack to collect data with
[Prometheus](https://prometheus.io/) and graph in [Grafana](https://grafana.com).

## Usage

*note: these instructions are for running the script interactively, skip to the
next section to just run the docker stack*

The collector is a Python 3 script, install dependancies with:

    pip3 install --user -r requirements.txt

(consider settinp up a [virtual
env](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment))

Then run 

    ./cyberq.py --help
    
to see the help text.

## Docker stack

To run the stack, you need Docker and docker-compose. Then run

    CYBERQ_URL=http://my_cyberq_ip docker-compose up -d
    
Where `my_cyberq_ip` is the IP address to your CyberQ. Alternatively you can
specify the address in the `.env` file.

This will do the following:

* Build container image with the `cyberq.py` script
* Download prometheus and grafana images from docker hub
* Run containers in the background
    
The grafana service provisions the prometheus datasource and a basic dashboard
that displays set and current temperature.

Access Grafana at http://localhost:3000 and login with the default admin/admin
username and password (you'll be prompted to change the password).

## Note

This is not a production-ready deployment; there's no persistence of Prometheus
data or the Grafana database, so changes will be lost when the services are
recreated. To do that you'd want to bind-mount local paths to the reepective
data directories; consult each project's documentation for details.
