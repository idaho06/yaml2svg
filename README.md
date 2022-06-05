YAML TO SVG
===========

Small utillity to transform a yaml file describing a systems architecture to a diagram in svg format.

    yaml2svg.py -h                 
    usage: yaml2svg.py [-h] [-o OUTPUT] [-d DEBUG] [-erro ERROROUTPUT] [input]

    Convert YAML files describing systems architectures to svg diagrams.

    positional arguments:
    input                 Input YAML file.

    options:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                            Output SVG file
    -d DEBUG, --debug DEBUG
                            Debug level: DEBUG, INFO, WARNING, ERROR or CRITICAL
    -erro ERROROUTPUT, --erroroutput ERROROUTPUT
                            File of error output. Default is stderr.

    Made by César (Idaho06) Rodríguez Moreno.