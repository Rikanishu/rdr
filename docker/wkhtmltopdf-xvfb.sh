#!/usr/bin/env bash 

xvfb-run -a --server-args="-screen 0, 1024x768x24" /opt/wkhtmltox/bin/wkhtmltopdf -q $*