#!/bin/bash
cat <<'EOF' >> /root/.bashrc
cd ${HOME}
source ${HOME}/wpaudit/bin/activate
echo -e "Welcome to wpaudit!\nTo run wpaudit, just type \`scout -h\` to see the help documentation.\nHave fun!\n\n"
EOF