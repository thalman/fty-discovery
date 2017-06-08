#
#    fty-discovery - 42ity service for discovering devices
#
#    Copyright (C) 2014 - 2017 Eaton                                        
#                                                                           
#    This program is free software; you can redistribute it and/or modify   
#    it under the terms of the GNU General Public License as published by   
#    the Free Software Foundation; either version 2 of the License, or      
#    (at your option) any later version.                                    
#                                                                           
#    This program is distributed in the hope that it will be useful,        
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
#    GNU General Public License for more details.                           
#                                                                           
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.            
#

# To build with draft APIs, use "--with drafts" in rpmbuild for local builds or add
#   Macros:
#   %_with_drafts 1
# at the BOTTOM of the OBS prjconf
%bcond_with drafts
%if %{with drafts}
%define DRAFTS yes
%else
%define DRAFTS no
%endif
Name:           fty-discovery
Version:        1.0.0
Release:        1
Summary:        42ity service for discovering devices
License:        GPL-2.0+
URL:            https://42ity.org/
Source0:        %{name}-%{version}.tar.gz
Group:          System/Libraries
# Note: ghostscript is required by graphviz which is required by
#       asciidoc. On Fedora 24 the ghostscript dependencies cannot
#       be resolved automatically. Thus add working dependency here!
BuildRequires:  ghostscript
BuildRequires:  asciidoc
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  systemd-devel
BuildRequires:  systemd
%{?systemd_requires}
BuildRequires:  xmlto
BuildRequires:  zeromq-devel
BuildRequires:  czmq-devel
BuildRequires:  malamute-devel
BuildRequires:  fty-proto-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
fty-discovery 42ity service for discovering devices.

%package -n libfty_discovery0
Group:          System/Libraries
Summary:        42ity service for discovering devices shared library

%description -n libfty_discovery0
This package contains shared library for fty-discovery: 42ity service for discovering devices

%post -n libfty_discovery0 -p /sbin/ldconfig
%postun -n libfty_discovery0 -p /sbin/ldconfig

%files -n libfty_discovery0
%defattr(-,root,root)
%{_libdir}/libfty_discovery.so.*

%package devel
Summary:        42ity service for discovering devices
Group:          System/Libraries
Requires:       libfty_discovery0 = %{version}
Requires:       zeromq-devel
Requires:       czmq-devel
Requires:       malamute-devel
Requires:       fty-proto-devel

%description devel
42ity service for discovering devices development tools
This package contains development files for fty-discovery: 42ity service for discovering devices

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libfty_discovery.so
%{_libdir}/pkgconfig/libfty_discovery.pc
%{_mandir}/man3/*
%{_mandir}/man7/*

%prep
%setup -q

%build
sh autogen.sh
%{configure} --enable-drafts=%{DRAFTS} --with-systemd-units
make %{_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# remove static libraries
find %{buildroot} -name '*.a' | xargs rm -f
find %{buildroot} -name '*.la' | xargs rm -f

%files
%defattr(-,root,root)
%doc README.md
%{_bindir}/fty-discovery
%{_mandir}/man1/fty-discovery*
%config(noreplace) %{_sysconfdir}/fty-discovery/fty-discovery.cfg
/usr/lib/systemd/system/fty-discovery.service
%dir %{_sysconfdir}/fty-discovery
%if 0%{?suse_version} > 1315
%post
%systemd_post fty-discovery.service
%preun
%systemd_preun fty-discovery.service
%postun
%systemd_postun_with_restart fty-discovery.service
%endif

%changelog