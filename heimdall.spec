%define prerel %{nil}

%define udev_rules_dir /lib/udev/rules.d

Name:		heimdall
Version:	1.4.2
%if "%prerel" != ""
Release:	0.%prerel.1
%else
Release:	4
%endif
Summary:	Flash firmware (aka ROMs) onto Samsung Galaxy S devices
Group:		Development/Other
License:	MIT
URL:		https://www.glassechidna.com.au/products/%{name}/
Source0:	https://gitlab.com/BenjaminDobell/Heimdall/-/archive/v%{version}/Heimdall-v%{version}.tar.bz2
Patch0:		https://gitlab.com/BenjaminDobell/Heimdall/-/merge_requests/187.patch
Patch1:		https://gitlab.com/BenjaminDobell/Heimdall/-/merge_requests/222.patch
Patch2:		https://gitlab.com/BenjaminDobell/Heimdall/-/merge_requests/227.patch
Patch3:		https://gitlab.com/BenjaminDobell/Heimdall/-/merge_requests/240.patch
Patch4:		https://gitlab.com/BenjaminDobell/Heimdall/-/merge_requests/329.patch
Patch5:		https://gitlab.com/BenjaminDobell/Heimdall/-/merge_requests/459.patch
Patch6:		https://gitlab.com/BenjaminDobell/Heimdall/-/merge_requests/477.patch
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	dos2unix
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	pkgconfig(zlib)
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
%autosetup -p1 -n Heimdall-v%{version}

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
