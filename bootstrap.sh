#!/bin/bash

VERSION=$(grep "Version:" /vagrant/tomcat9.spec |cut -d ":" -f2 |tr -d "[:space:]")
RELEASE=$(grep "Release:" /vagrant/tomcat9.spec |cut -d ":" -f2 |tr -d "[:space:]")
ARCH=$(grep "BuildArch:" /vagrant/tomcat9.spec |cut -d ":" -f2 |tr -d "[:space:]")

echo "Version: $VERSION-$RELEASE BuildArch: $ARCH"

# Exclude kernels from update as they may break hgfs under VMWare
yum --exclude=kernel\* update -y
yum -y install policycoreutils-python rpmdevtools
if [ ! -f /root/.rpmmacros ];
then
  rpmdev-setuptree
fi

if [ ! -f /root/rpmbuild/SOURCES/apache-tomcat-$VERSION.tar.gz ];
then
  curl -o  /root/rpmbuild/SOURCES/apache-tomcat-$VERSION.tar.gz http://archive.apache.org/dist/tomcat/tomcat-9/v$VERSION/bin/apache-tomcat-$VERSION.tar.gz
fi

cp "/vagrant/tomcat9."{service,logrotate,conf} "/root/rpmbuild/SOURCES/"
cp "/vagrant/tomcat9.spec" "/root/rpmbuild/SPECS/"

if [ ! -f /vagrant/tomcat9-$VERSION-$RELEASE.x86_64.rpm ];
then
  cd /root/rpmbuild
  rpmbuild --buildroot "/root/rpmbuild/BUILDROOT" /root/rpmbuild/SPECS/tomcat9.spec -bb
  cp /root/rpmbuild/RPMS/x86_64/tomcat9-$VERSION-$RELEASE.x86_64.rpm /vagrant
  cp /root/rpmbuild/RPMS/x86_64/tomcat9-docs-webapp-$VERSION-$RELEASE.x86_64.rpm /vagrant
  cp /root/rpmbuild/RPMS/x86_64/tomcat9-webapps-$VERSION-$RELEASE.x86_64.rpm /vagrant
  cp /root/rpmbuild/RPMS/x86_64/tomcat9-admin-webapps-$VERSION-$RELEASE.x86_64.rpm /vagrant
fi
