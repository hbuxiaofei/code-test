#!/usr/bin/env bash

# https://resources.ovirt.org/pub/ovirt-4.4/rpm/el8/x86_64

rm -rf mirror.isoc.org.il
[ ! -d noarch ] && mkdir noarch
[ ! -d x86_64 ] && mkdir x86_64

wget -c -r -np -k -L -p \
    http://mirror.isoc.org.il/pub/ovirt/ovirt-4.4/rpm/el8/noarch

wget -c -r -np -k -L -p \
    http://mirror.isoc.org.il/pub/ovirt/ovirt-4.4/rpm/el8/x86_64


cat mirror.isoc.org.il/pub/ovirt/ovirt-4.4/rpm/el8/noarch | grep -oP "http://.*?\.rpm" > noarch.rpm.list
while read _line; do
    echo ">>> download ${_line}"
    mwget -n 20 -d noarch ${_line}
done < noarch.rpm.list

cat mirror.isoc.org.il/pub/ovirt/ovirt-4.4/rpm/el8/x86_64 | grep -oP "http://.*?\.rpm" > x86_64.rpm.list
while read _line; do
    echo ">>> download ${_line}"
    mwget -n 20 -d x86_64 ${_line}
done < x86_64.rpm.list
