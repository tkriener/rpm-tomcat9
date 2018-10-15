%global homedir /usr/share/%{name}

Name:             tomcat9
Version:          9.0.12
Release:          1.el7.harbottle
Summary:          Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API
License:          ASL 2.0
URL:              http://tomcat.apache.org/
Source0:          http://www-us.apache.org/dist/tomcat/tomcat-9/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1:          tomcat9.conf
Source2:          tomcat9.service
Source3:          tomcat9.logrotate
BuildRequires:    systemd-units
Provides:         tomcat9
Requires:         java >= 1:1.8.0
Requires(pre):    shadow-utils
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%prep
%setup -qn apache-tomcat-%{version}

%install
rm -rf webapps/*
rm -f bin/*.bat
sed -i -e '/^2localhost/d' -e '/\[\/localhost\]/d' \
    -e '/^3manager/d' -e '/\[\/manager\]/d' \
    -e '/^4host-manager/d' -e '/\[\/host-manager\]/d' \
    -e 's/, *4host-manager.org.apache.juli.AsyncFileHandler//' \
    -e 's/, *3manager.org.apache.juli.AsyncFileHandler//' \
    conf/logging.properties
install -d -m 755 $RPM_BUILD_ROOT%{homedir}
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}
install -d -m 755 $RPM_BUILD_ROOT%{_unitdir}
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -d -m 755 $RPM_BUILD_ROOT%{_var}/log
install -d -m 755 $RPM_BUILD_ROOT%{_var}/cache
install -d -m 755 $RPM_BUILD_ROOT%{_var}/cache/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_var}/lib
install -d -m 755 $RPM_BUILD_ROOT%{_var}/lib/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_libexecdir}


mv bin $RPM_BUILD_ROOT%{_libexecdir}/%{name}
mv conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mv lib $RPM_BUILD_ROOT%{homedir}/lib
mv logs $RPM_BUILD_ROOT%{_var}/log/%{name}
mv temp $RPM_BUILD_ROOT%{_var}/cache/%{name}/temp
mv work $RPM_BUILD_ROOT%{_var}/cache/%{name}/work
mv webapps $RPM_BUILD_ROOT%{_var}/lib/%{name}/webapps
mv * $RPM_BUILD_ROOT%{homedir}/

install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

ln -s %{_libexecdir}/%{name} $RPM_BUILD_ROOT%{homedir}/bin
ln -s %{_sysconfdir}/%{name} $RPM_BUILD_ROOT%{homedir}/conf
ln -s %{_var}/log/%{name} $RPM_BUILD_ROOT%{homedir}/logs
ln -s %{_var}/cache/%{name}/temp $RPM_BUILD_ROOT%{homedir}/temp
ln -s %{_var}/lib/%{name}/webapps $RPM_BUILD_ROOT%{homedir}/webapps
ln -s %{_var}/cache/%{name}/work $RPM_BUILD_ROOT%{homedir}/work

%pre
getent group %{name} >/dev/null || groupadd -f -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{homedir} -s /sbin/nologin -c "Apache Tomcat 9 user" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%attr(-,root,tomcat9) %dir %{homedir}
%attr(-,root,tomcat9) %{_libexecdir}/%{name}
%attr(0770,root,tomcat9) %dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(0740,root,tomcat9) %{_sysconfdir}/%{name}/*
%attr(-,root,tomcat9) %{homedir}/lib
%attr(-,tomcat9,tomcat9) %{_var}/log/%{name}
%attr(-,tomcat9,tomcat9) %{_var}/cache/%{name}/temp
%attr(-,tomcat9,tomcat9) %{_var}/lib/%{name}/webapps
%attr(-,tomcat9,tomcat9) %{_var}/cache/%{name}/work
%{_unitdir}/%{name}.service
%{_sysconfdir}/logrotate.d/%{name}
%{homedir}/bin
%{homedir}/conf
%{homedir}/logs
%{homedir}/temp
%{homedir}/webapps
%{homedir}/work
%doc %{homedir}/LICENSE
%doc %{homedir}/NOTICE
%doc %{homedir}/RELEASE-NOTES
%doc %{homedir}/RUNNING.txt
%doc %{homedir}/BUILDING.txt
%doc %{homedir}/CONTRIBUTING.md
%doc %{homedir}/README.md

%changelog
* Mon Oct 15 2018 - grainger@gmail.com - 9.0.12-1
  - 9.0.12
* Mon Jul 02 2018 - grainger@gmail.com - 9.0.10-1
  - 9.0.10
* Mon Jun 11 2018 - grainger@gmail.com - 9.0.8-1
  - 9.0.8
* Mon Apr 30 2018 - grainger@gmail.com - 9.0.7-1
  - Initial packaging
