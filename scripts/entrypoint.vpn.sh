#!/bin/sh
mkdir -p ~/.ssh
touch ~/.ssh/config
chmod 600 /root/.ssh/config
grep 'vpnjantit.com' ~/.ssh/config || echo $'\nHost *.vpnjantit.com\n StrictHostKeyChecking no\n UserKnownHostsFile=/dev/null\n\n' >> ~/.ssh/config
python3 -m vpn
