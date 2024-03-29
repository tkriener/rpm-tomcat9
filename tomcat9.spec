%global homedir /usr/share/%{name}

Name:             tomcat9
Version:          9.0.86
Release:          1.el7.harbottle
BuildArch:        x86_64
Summary:          Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API
Group:            Applications/System
License:          Apache-2.0
URL:              http://tomcat.apache.org/
Source0:          https://downloads.apache.org/tomcat/tomcat-9/v%{version}/bin/apache-tomcat-%{version}.tar.gz
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

%package admin-webapps
Group: Applications/System
Summary: The host-manager and manager web applications for Apache Tomcat 9
Requires: %{name} = %{version}-%{release}

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat 9.

%package docs-webapp
Group: Applications/Text
Summary: The docs web application for Apache Tomcat 9
Requires: %{name} = %{version}-%{release}

%description docs-webapp
The docs web application for Apache Tomcat 9.

%package webapps
Group:    Applications/Internet
Summary:  The ROOT and examples web applications for Apache Tomcat 9
Requires: %{name} = %{version}-%{release}

%description webapps
The ROOT and examples web applications for Apache Tomcat 8.

%prep
%setup -qn apache-tomcat-%{version}

%install
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
%attr(-,tomcat9,tomcat9) %dir %{_var}/lib/%{name}/webapps
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

%files admin-webapps
%defattr(0664,root,tomcat9,0755)
%{_var}/lib/%{name}/webapps/host-manager
%{_var}/lib/%{name}/webapps/manager
%config(noreplace) %{_var}/lib/%{name}/webapps/host-manager/WEB-INF/web.xml
%config(noreplace) %{_var}/lib/%{name}/webapps/manager/WEB-INF/web.xml

%files docs-webapp
%defattr(-,root,root,-)
%{_var}/lib/%{name}/webapps/docs

%files webapps
%defattr(0644,tomcat9,tomcat9,0755)
%{_var}/lib/%{name}/webapps/ROOT
%{_var}/lib/%{name}/webapps/examples

%changelog
* Tue Aug 08 2023 - thomas.kriener@possehl-secure.de - 9.0.78-1
  - Bump version

* Tue Apr 25 2023 - thomas.kriener@possehl-secure.de - 9.0.74-1
  - Bump version

* Mon Jan 09 2023 - thomas.kriener@twinsec.de - 9.0.70-1
  - Bump version

* Thu Jun 09 2022 - harbottle@room3d3.com - 9.0.64-1
  - Bump version

* Mon May 16 2022 - harbottle@room3d3.com - 9.0.63-1
  - Bump version

* Fri Apr 01 2022 - harbottle@room3d3.com - 9.0.62-1
  - Bump version

* Mon Mar 14 2022 - harbottle@room3d3.com - 9.0.60-1
  - Bump version

* Mon Feb 28 2022 - harbottle@room3d3.com - 9.0.59-1
  - Bump version

* Thu Jan 20 2022 - harbottle@room3d3.com - 9.0.58-1
  - Bump version

* Sun Dec 12 2021 - harbottle@room3d3.com - 9.0.56-1
  - Bump version

* Fri Oct 01 2021 - harbottle@room3d3.com - 9.0.54-1
  - Bump version

* Fri Sep 10 2021 - harbottle@room3d3.com - 9.0.53-1
  - Bump version

* Fri Aug 06 2021 - harbottle@room3d3.com - 9.0.52-1
  - Update download location
  - Bump version

* Fri Jul 02 2021 - harbottle@room3d3.com - 9.0.50-1
  - Bump version

* Tue Jun 15 2021 - harbottle@room3d3.com - 9.0.48-1
  - Bump version

* Wed May 12 2021 - harbottle@room3d3.com - 9.0.46-1
  - Bump version

* Tue Apr 06 2021 - harbottle@room3d3.com - 9.0.45-1
  - Bump version

* Thu Mar 11 2021 - harbottle@room3d3.com - 9.0.44-1
  - Bump version

* Tue Feb 02 2021 - harbottle@room3d3.com - 9.0.43-1
  - Bump version

* Tue Dec 08 2020 - harbottle@room3d3.com - 9.0.41-1
  - Bump version

* Fri Nov 20 2020 - harbottle@room3d3.com - 9.0.40-1
  - Bump version

* Fri Oct 09 2020 - harbottle@room3d3.com - 9.0.39-1
  - Bump version

* Tue Sep 15 2020 - harbottle@room3d3.com - 9.0.38-1
  - Bump version

* Sun Jul 05 2020 - harbottle@room3d3.com - 9.0.37-1
  - Bump version

* Sun Jun 07 2020 - harbottle@room3d3.com - 9.0.36-1
  - Bump version

* Mon May 11 2020 - harbottle@room3d3.com - 9.0.35-1
  - Bump version

* Wed Apr 08 2020 - harbottle@room3d3.com - 9.0.34-1
  - Bump version

* Mon Mar 16 2020 - harbottle@room3d3.com - 9.0.33-1
  - Bump version

* Tue Feb 11 2020 - harbottle@room3d3.com - 9.0.31-1
  - Bump version

* Thu Dec 19 2019 - harbottle@room3d3.com - 9.0.30-2
  - Build for el8
  - Tidy spec file

* Thu Dec 19 2019 - harbottle@room3d3.com - 9.0.30-1
  - Bump version

* Thu Nov 21 2019 - harbottle@room3d3.com - 9.0.29-1
  - Bump version

* Fri Oct 11 2019 - harbottle@room3d3.com - 9.0.27-1
  - Bump version

* Thu Sep 19 2019 - harbottle@room3d3.com - 9.0.26-1
  - Bump version

* Sat Aug 17 2019 - harbottle@room3d3.com - 9.0.24-1
  - Bump version

* Tue Jul 09 2019 - harbottle@room3d3.com - 9.0.22-1
  - Bump version

* Sat Jun 08 2019 - harbottle@room3d3.com - 9.0.21-2
  - Add webapps packages

* Fri Jun 07 2019 - harbottle@room3d3.com - 9.0.21-1
  - Bump version

* Mon Jun 03 2019 - harbottle@room3d3.com - 9.0.20-1
  - Bump version

* Sat Apr 13 2019 - harbottle@room3d3.com - 9.0.19-1
  - Bump version

* Mon Mar 18 2019 - harbottle@room3d3.com - 9.0.17-1
  - Bump version

* Fri Feb 08 2019 - harbottle@room3d3.com - 9.0.16-1
  - Bump version

* Fri Feb 01 2019 - harbottle@room3d3.com - 9.0.14-2
  - Fix systemd service

* Fri Dec 21 2018 - harbottle@room3d3.com - 9.0.14-1
  - Bump version
* Mon Oct 15 2018 - grainger@gmail.com - 9.0.12-1
  - 9.0.12
* Mon Jul 02 2018 - grainger@gmail.com - 9.0.10-1
  - 9.0.10
* Mon Jun 11 2018 - grainger@gmail.com - 9.0.8-1
  - 9.0.8
* Mon Apr 30 2018 - grainger@gmail.com - 9.0.7-1
  - Initial packaging
