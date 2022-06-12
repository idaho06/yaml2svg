#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import sys
import logging
import argparse
#from tokenize import String
from ruamel.yaml import YAML
#from diagram import DiagramBuilder
from diagrams import Cluster,Diagram
from diagrams.onprem.compute import Server
import json


# Globals and other helper functions


def main(args):
    logging.debug("Entering Main function")
    logging.debug(args)

    yaml = YAML()

    yaml_file = args.input
    yaml_dict = yaml.load(yaml_file)
    yaml_file.close()
    #logging.debug(yaml_dict)
    #logging.debug(yaml_dict['Environments'])
    # logging.debug(yaml_dict['Environments']['Hadoop and Solr']['Masters'][0]['Type'])

    #diag = DiagramBuilder(title="Test", filename=args.output.split(".")[0], format=args.output.split(".")[1])

    # for item in yaml_dict.keys():
    #    if item == "Environments":
    #        pass

    environments = yaml_dict['Environments']
    logging.debug(json.dumps(environments, sort_keys=False, indent=4))
    connections = yaml_dict['Connections']
    logging.debug(json.dumps(connections, sort_keys=False, indent=4))

    with Diagram(
            name=yaml_dict['Name'],
            filename=args.output.split(".")[0],
            outformat=args.output.split(".")[1],
            show=True):
        for env in environments.keys():
            logging.debug("Checking " + env)
            if environments[env]["Type"] == "Network":
                logging.debug("Network found: " + env)
        

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert YAML files describing systems architectures to svg diagrams.",
                                     epilog="Made by César (Idaho06) Rodríguez Moreno.")
    parser.add_argument(
        "-o", "--output", help="Output SVG file", default="output.svg")
    parser.add_argument(
        "-d", "--debug", help="Debug level: DEBUG, INFO, WARNING, ERROR or CRITICAL", default="WARNING")
    parser.add_argument("-erro", "--erroroutput",
                        help="File of error output. Default is stderr.", default="stderr")
    parser.add_argument("input", help="Input YAML file.",
                        nargs='?', type=argparse.FileType(mode='r', encoding="UTF-8"), default=sys.stdin)
    args = parser.parse_args()

    loglevel = logging.WARNING
    logoutput = None
    if args.debug == "DEBUG":
        loglevel = logging.DEBUG
    if args.debug == "INFO":
        loglevel = logging.INFO
    if args.debug == "ERROR":
        loglevel = logging.ERROR
    if args.debug == "CRITICAL":
        loglevel = logging.CRITICAL
    if args.erroroutput != "stderr":
        logging.basicConfig(level=loglevel, filename=args.erroroutput,
                            format="%(asctime)s %(levelname)s: %(funcName)s: %(message)s")
    else:
        logging.basicConfig(level=loglevel, stream=sys.stderr,
                            format="%(asctime)s %(levelname)s: %(funcName)s: %(message)s")
    logging.info("Logging level set to %s." % logging.getLevelName(loglevel))

    exit(main(args))
