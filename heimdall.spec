%define prerel RC3

%define udev_rules_dir /lib/udev/rules.d

Name:		heimdall
Version:	1.4.1
%if "%prerel" != ""
Release:	0.%prerel.1
%else
Release:	1
%endif
Summary:	Flash firmware (aka ROMs) onto Samsung Galaxy S devices
Group:		Development/Other
License:	MIT
URL:		http://www.glassechidna.com.au/products/%{name}/
# Source has to be generated from https://github.com/Benjamin-Dobell/Heimdall/tree/v1.3.1
# using:
# git clone git://github.com/Benjamin-Dobell/Heimdall.git
# git archive --format tar --prefix heimdall-1.4.1/ -o heimdall-1.4.1RC2.tar v1.4.1RC2
Source0:	%{name}-%{version}%prerel.tar.xz
BuildRequires:	pkgconfig(libusb-1.0)
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
%setup -q
%apply_patches

#fix EOLs
dos2unix Linux/README

#fix frontend install
sed -i -e 's|/usr/local/bin|%{_bindir}|g' heimdall-frontend/heimdall-frontend.pro

%build 
cd libpit
	%configure
	%make
cd ..
cd heimdall
	./autogen.sh --help || :
	%configure2_5x
	%make V=1
cd ..

cd heimdall-frontend
	%qmake_qt4 heimdall-frontend.pro 
	%make V=1
cd ..

%install
pushd heimdall
	%makeinstall_std
popd

pushd heimdall-frontend
	%make INSTALL_ROOT=%{buildroot} install
popd

# udev rule
mkdir -p %{buildroot}%{udev_rules_dir}
cat > %{buildroot}%{udev_rules_dir}/60-heimdall-galaxy-s.rules << EOF
SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", ATTR{idProduct}=="6601", MODE="0666" 
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

%post
udevadm control --reload

%postun
udevadm control --reload

%files
%defattr(-,root,root)
%doc Linux/README
%{_bindir}/%{name}
%{udev_rules_dir}/60-heimdall.rules
%{udev_rules_dir}/60-heimdall-galaxy-s.rules

%files frontend
%defattr(-,root,root)
%doc Linux/README
%{_bindir}/%{name}-frontend
%{_datadir}/applications/mandriva-%{name}.desktop
