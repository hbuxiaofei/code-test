#!/bin/bash

# mask NetworkManager
systemctl stop NetworkManager.service
systemctl mask NetworkManager.service

# mask firewall
systemctl stop firewalld.service
systemctl mask firewalld.service

# disable selinux
sed -i "s/SELINUX=enforcing/SELINUX=disable/g" /etc/selinux/config
setenforce 0

# limits setting
LIMITS_CONF_FILE="/etc/security/limits.conf"
if grep -q "soft.*nofile" $LIMITS_CONF_FILE; then
    sed -i '/soft.*nofile/d' $LIMITS_CONF_FILE
fi
echo "root    soft    nofile    65536" >> $LIMITS_CONF_FILE
if grep -q "hard.*nofile" $LIMITS_CONF_FILE; then
    sed -i '/hard.*nofile/d' $LIMITS_CONF_FILE
fi
echo "root    hard    nofile    65536" >> $LIMITS_CONF_FILE

