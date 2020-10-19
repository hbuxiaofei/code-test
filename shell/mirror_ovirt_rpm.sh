#!/usr/bin/env bash

# https://resources.ovirt.org/pub/ovirt-4.4/rpm/el8/x86_64
#
# input_str="vdsm-network-4.40.22-1.el8.x86_64.rpm"
# echo "${input_str##*/}" | sed -e s/-[[:digit:]]./@/|  awk -F '@' '{print $1}'
# echo "${input_str##*/}" | sed -e s/-[[:digit:]]./@/|  awk -F '@' '{print $2}'

rm -rf mirror.isoc.org.il
[ ! -d noarch ] && mkdir noarch
[ ! -d x86_64 ] && mkdir x86_64

wget -c -r -np -k -L -p \
    http://mirror.isoc.org.il/pub/ovirt/ovirt-4.4/rpm/el8/noarch

wget -c -r -np -k -L -p \
    http://mirror.isoc.org.il/pub/ovirt/ovirt-4.4/rpm/el8/x86_64


cat mirror.isoc.org.il/pub/ovirt/ovirt-4.4/rpm/el8/noarch | grep -oP "http://.*?\.rpm" > noarch.rpm.list
while read _line; do
    echo ">>> download:"

    _path="${_line%/*}"
    _package="${_line##*/}"
    _name=$(echo "${_package##*/}" | sed -e s/-[[:digit:]]./@/ | awk -F '@' '{print $1}')
    _download=$(cat noarch.rpm.list | grep "${_path}/${_name}-" 2>/dev/null | tail -n1)
    echo ">>> $_download"

    mwget -n 20 -d noarch ${_download}
done < noarch.rpm.list

exit 0

cat mirror.isoc.org.il/pub/ovirt/ovirt-4.4/rpm/el8/x86_64 | grep -oP "http://.*?\.rpm" > x86_64.rpm.list
while read _line; do
    echo ">>> download:"

    _path="${_line%/*}"
    _package="${_line##*/}"
    _name=$(echo "${_package##*/}" | sed -e s/-[[:digit:]]./@/ | awk -F '@' '{print $1}')
    _download=$(cat x86_64.rpm.list | grep "${_path}/${_name}-" 2>/dev/null | tail -n1)
    echo ">>> $_download"

    mwget -n 20 -d x86_64 ${_download}
done < x86_64.rpm.list
