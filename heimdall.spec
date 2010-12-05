%define name	heimdall
%define version	1.1.0
%define release	%mkrel 1

%define udev_rules_dir /lib/udev/rules.d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Flash firmware (aka ROMs) onto Samsung Galaxy S devices
Group:		Development/Other
License:	MIT
URL:		http://www.glassechidna.com.au/products/%{name}/
#Sources from github, no reasonable tarball, yet..
Source:		http://download.github.com/Benjamin-Dobell-Heimdall-400e41e.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	usb1.0-devel
BuildRequires:	dos2unix
BuildRequires:	qt4-devel

%description
Heimdall is a cross-platform open-source utility to flash firmware (aka ROMs)
onto Samsung Galaxy S devices.

%package frontend
Summary:	Qt4 based frontend for %{name}
Group:		Graphical desktop/KDE
Requires:	%{name} = %{version}-%{release}

%description frontend
Heimdall is a cross-platform open-source utility to flash firmware (aka ROMs)
onto Samsung Galaxy S devices.

This package provides Qt4 based frontend for %{name}.

%prep
%setup -q -n Benjamin-Dobell-Heimdall-400e41e

#fix EOLs
dos2unix Linux/README

#fix frontend install
sed -i -e 's|\(DESIREDINSTALLDIR =\).*|\1%{_bindir}|' heimdall-frontend/heimdall-frontend.pro

%build 
pushd heimdall
	%configure2_5x
	%make V=1
popd

pushd heimdall-frontend
	%qmake_qt4 heimdall-frontend.pro 
	%make V=1
popd

%install
rm -rf %{buildroot}

pushd heimdall
	%makeinstall_std
popd

pushd heimdall-frontend
	%make INSTALL_ROOT=%{buildroot} install
popd

# udev rule
mkdir -p %{buildroot}%{udev_rules_dir}
cat > %{buildroot}%{udev_rules_dir}/60-heimdall-galaxy-s.rules << EOF
SUBSYSTEM=="usb", SYSFS{idVendor}=="04e8", SYSFS{idProduct}=="6601", MODE="0666" 
EOF

# desktop file
# TODO: better icon
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/mandriva-heimdall.desktop << EOF
[Desktop Entry]
Name=Heimdall
Comment=Flash firmware (aka ROMs) onto Samsung Galaxy S devices
Icon=phone
Exec=%{name}-frontend
Terminal=false
Type=Application
Categories=Qt;Utility;
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Linux/README heimdall/LICENSE
%{_bindir}/%{name}
%{udev_rules_dir}/60-heimdall-galaxy-s.rules

%files frontend
%defattr(-,root,root)
%doc Linux/README heimdall/LICENSE
%{_bindir}/%{name}-frontend
%{_datadir}/applications/mandriva-%{name}.desktop
