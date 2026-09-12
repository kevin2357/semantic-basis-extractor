#!/bin/sh
set -eu

cd /out
/tool/mtftar -v -f /archive.bkf | tar -xvf -
