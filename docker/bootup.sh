#!/bin/bash
service tor restart
dnscrypt-proxy -check
dnscrypt-proxy -list
dnscrypt-proxy

