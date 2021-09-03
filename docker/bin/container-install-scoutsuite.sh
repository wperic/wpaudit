#!/bin/bash

# =====================================
# install wpaudit into a virtual env
# =====================================
# AUTHOR: ebrogdon@wembleypartners.com
# VERSION: 0.1.0
# =====================================
export DEBIAN_FRONTEND=noninteractive

WORKDIR=/root
TMPDIR=/tmp

# =====================================
# install wpaudit
# =====================================
cd ${WORKDIR}
virtualenv -p python3 wpaudit
source ${WORKDIR}/wpaudit/bin/activate
pip install wpaudit

echo -e "\n\nwpaudit Installation Complete!\n\n"
