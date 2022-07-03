#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
from shutil import disk_usage
import sys
import logging
import argparse
#from tokenize import String
from ruamel.yaml import YAML
#from diagram import DiagramBuilder
from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.compute import Server
from diagrams.oci.compute import VM
from diagrams.oci.network import LoadBalancer
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Hadoop
from diagrams.onprem.analytics import Hive
from diagrams.onprem.network import Zookeeper
from diagrams.onprem.search import Solr
from diagrams.onprem.database import HBase
from diagrams.onprem.database import MySQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana
from diagrams.azure.identity import ActiveDirectory
from diagrams.custom import Custom
import json


# Globals and other helper functions

GRAPH_ELEMENTS = {}


def makeLabel(**kwargs):
    if "nolabel" in kwargs and kwargs["nolabel"] == True:
        return ""

    label = ""
    for key, value in kwargs.items():
        cr = ""
        pre = ""
        post = ""
        if label != "":
            cr = "\n"
        if key == "nolabel":
            value = ""
            cr = ""
        elif key == "cores":
            pre = "CPU cores: "
        elif key == "memory":
            pre = "RAM: "
        elif key == "disk":
            pre = "Disks: "
        elif key == "epg":
            pre = "EPG: "
        if value != "":
            label += f"{cr}{pre}{value}{post}"
    return label


def iterateList(nodes_list):
    global GRAPH_ELEMENTS
    if isinstance(nodes_list, list):
        for node in nodes_list:
            type = node.get("Type", "No Type")
            nolabel = node.get("NoLabel", False)
            if type == "Physical":
                name = node.get("Name", "")
                ip = node.get("IP", "")
                memory = node.get("Memory", "")
                disk = node.get("Disk", "")
                cores = node.get("Cores", "")
                operating_system = node.get("OS", "")
                label = makeLabel(nolabel=nolabel, name=name, ip=ip, type="Physical server",
                                  operating_system=operating_system, cores=cores, memory=memory, disk=disk)
                if "Services" in node:
                    GRAPH_ELEMENTS[name] = Cluster(label=label)
                    with GRAPH_ELEMENTS[name]:
                        iterateList(node["Services"])
                else:
                    GRAPH_ELEMENTS[name] = Server(label=label)
            elif type == "VM":
                name = node.get("Name", "")
                ip = node.get("IP", "")
                memory = node.get("Memory", "")
                disk = node.get("Disk", "")
                cores = node.get("Cores", "")
                operating_system = node.get("OS", "")
                label = makeLabel(nolabel=nolabel, name=name, ip=ip, type="Virtual machine",
                                  operating_system=operating_system, cores=cores, memory=memory, disk=disk)
                if "Services" in node:
                    GRAPH_ELEMENTS[name] = Cluster(label=label)
                    with GRAPH_ELEMENTS[name]:
                        iterateList(node["Services"])
                else:
                    GRAPH_ELEMENTS[name] = VM(label=label)
            elif type == "Users":
                name = node["Name"]
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Users(label=label)
            elif type == "Hadoop":
                name = node["Name"]
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Hadoop(label=label)
            elif type == "Knox":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/knox.png")
            elif type == "Ssh":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/ssh.png")
            elif type == "Ambari":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/ambari.png")
            elif type == "Hive":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Hive(
                    label=label)
            elif type == "Zookeeper":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Zookeeper(
                    label=label)
            elif type == "Solr":
                name = node.get("Name", "")
                ip = node.get("IP", "")
                memory = node.get("Memory", "")
                disk = node.get("Disk", "")
                cores = node.get("Cores", "")
                operating_system = node.get("OS", "")
                machine = node.get("Machine", "")
                label = makeLabel(nolabel=nolabel, name=name, ip=ip, machine=machine,
                                  operating_system=operating_system, cores=cores, memory=memory, disk=disk)
                GRAPH_ELEMENTS[name] = Solr(
                    label=label, icon_path="./icons/streamsets.png")
            elif type == "Oozie":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/oozie.png")
            elif type == "Spark":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/spark.png")
            elif type == "HBase":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = HBase(
                    label=label)
            elif type == "MySql":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = MySQL(
                    label=label)
            elif type == "Kafka":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Kafka(
                    label=label)
            elif type == "Grafana":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Grafana(
                    label=label)
            elif type == "LoadBalancer":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = LoadBalancer(
                    label=label)
            elif type == "ActiveDirectory":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = ActiveDirectory(
                    label=label)
            elif type == "Zeppelin":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/zeppelin_classic_logo.png")
            elif type == "Ranger":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/ranger.png")
            elif type == "Kerberos":
                name = node.get("Name", "")
                label = makeLabel(nolabel=nolabel, name=name)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/kerberos.png")
            elif type == "NFS":
                name = node.get("Name", "")
                ip = node.get("IP", "")
                exports = node.get("Exports", "")
                label = makeLabel(nolabel=nolabel, name=name, ip=ip, exports=exports)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/nfs.png")
            elif type == "Streamsets":
                name = node.get("Name", "")
                ip = node.get("IP", "")
                memory = node.get("Memory", "")
                disk = node.get("Disk", "")
                cores = node.get("Cores", "")
                operating_system = node.get("OS", "")
                machine = node.get("Machine", "")
                label = makeLabel(nolabel=nolabel, name=name, ip=ip, machine=machine,
                                  operating_system=operating_system, cores=cores, memory=memory, disk=disk)
                GRAPH_ELEMENTS[name] = Custom(
                    label=label, icon_path="./icons/streamsets.png")
            else:
                name = node.get("Name", "")
                GRAPH_ELEMENTS[name] = Custom(
                    label=name, icon_path="./icons/unknown.png")


def iterateEnvironment(env_dict):
    global GRAPH_ELEMENTS
    for env_key in env_dict.keys():
        logging.debug("Checking " + env_key)
        if isinstance(env_dict[env_key], dict):
            if env_dict[env_key]["Type"] == "Network":
                logging.debug("Network found: " + env_key)
                #label = env_key + "\n" + env_dict[env_key]["Subnet"]
                subnet = env_dict[env_key].get("Subnet", "")
                epg = env_dict[env_key].get("EPG", "")
                label = makeLabel(name=env_key, epg=epg, subnet=subnet)
                GRAPH_ELEMENTS[env_key] = Cluster(label=label)
                with GRAPH_ELEMENTS[env_key]:
                    iterateEnvironment(env_dict=env_dict[env_key])
            elif env_dict[env_key]["Type"] == "Role":
                logging.debug("Role found: " + env_key)
                label = env_key
                GRAPH_ELEMENTS[env_key] = Cluster(label=label)
                with GRAPH_ELEMENTS[env_key]:
                    iterateEnvironment(env_dict=env_dict[env_key])
        elif isinstance(env_dict[env_key], list):
            logging.debug("Nodes found: " + env_key)
            iterateList(nodes_list=env_dict[env_key])


def interateConnections(conn_list):
    global GRAPH_ELEMENTS
    if isinstance(conn_list, list):
        for connection in conn_list:
            type = connection.get("Type", "simple")
            label = connection.get("Label", "")
            color = connection.get("Color", "")
            style = connection.get("Style", "")
            for origin, destination in connection.items():
                if origin in GRAPH_ELEMENTS and destination in GRAPH_ELEMENTS:
                    if type == "simple":
                        GRAPH_ELEMENTS[origin] >> Edge(label=label, color=color, style=style
                                                       ) >> GRAPH_ELEMENTS[destination]
                    elif type == "reverse":
                        GRAPH_ELEMENTS[origin] << Edge(label=label, color=color, style=style
                                                       ) << GRAPH_ELEMENTS[destination]
                    elif type == "double":
                        GRAPH_ELEMENTS[origin] >> Edge(label=label, color=color, style=style
                                                       ) << GRAPH_ELEMENTS[destination]
                    elif type == "line":
                        GRAPH_ELEMENTS[origin] - Edge(label=label, color=color, style=style
                                                      ) - GRAPH_ELEMENTS[destination]


def main(args):
    global GRAPH_ELEMENTS
    logging.debug("Entering Main function")
    logging.debug(args)

    yaml = YAML()

    yaml_file = args.input
    yaml_dict = yaml.load(yaml_file)
    yaml_file.close()

    environments = yaml_dict['Environments']
    logging.debug(json.dumps(environments, sort_keys=False, indent=4))
    connections = yaml_dict['Connections']
    logging.debug(json.dumps(connections, sort_keys=False, indent=4))

    with Diagram(
            name=yaml_dict['Name'],
            filename=args.output.split(".")[0],
            outformat=args.output.split(".")[1],
            show=args.show,
            direction="TB",
            curvestyle="curved"):
        iterateEnvironment(env_dict=environments)
        interateConnections(conn_list=connections)

    logging.debug(GRAPH_ELEMENTS)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert YAML files describing systems architectures to svg diagrams.",
                                     epilog="Made by César (Idaho06) Rodríguez Moreno.")
    parser.add_argument(
        "-o", "--output", help="Output SVG file", default="output.svg")
    parser.add_argument(
        "-s", "--show", help="Show output file", action='store_true')
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
