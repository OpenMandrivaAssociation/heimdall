%define prerel %{nil}

%define udev_rules_dir /lib/udev/rules.d

Name:		heimdall
Version:	1.4.2
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
Source0:	https://github.com/Benjamin-Dobell/Heimdall/archive/v%{version}.tar.gz
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	dos2unix
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	qt5-macros
BuildRequires:	qmake5

%description
Heimdall is a cross-platform open-source utility to flash firmware (aka ROMs)
onto Samsung Galaxy S devices.

%package frontend
Summary:	Qt based frontend for %{name}
Group:		Graphical desktop/KDE
Requires:	%{name} = %{version}-%{release}

%description frontend
Heimdall is a cross-platform open-source utility to flash firmware (aka ROMs)
onto Samsung Galaxy devices.

This package provides Qt based frontend for %{name}.

%prep
%setup -qn Heimdall-%{version}
%apply_patches

#fix EOLs
dos2unix Linux/README

%cmake_qt5 -G Ninja

%build 
%ninja -C build

%install
mkdir -p %{buildroot}%{_bindir}
cp -a build/bin/* %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{udev_rules_dir}
cp heimdall/*.rules %{buildroot}%{udev_rules_dir}/

# desktop file
# TODO: better icon
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/heimdall.desktop << EOF
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
%{udev_rules_dir}/*.rules

%files frontend
%defattr(-,root,root)
%doc Linux/README
%{_bindir}/%{name}-frontend
%{_datadir}/applications/%{name}.desktop
