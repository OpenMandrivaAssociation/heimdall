%define name	heimdall
%define version	1.0.0
%define release	%mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Flash firmware (aka ROMs) onto Samsung Galaxy S devices
Group:		Development/Other
License:	MIT
URL:		http://www.glassechidna.com.au/products/%{name}/
Source:		http://www.glassechidna.com.au/products/%{name}/%{name}-%{version}-source.zip
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	usb1.0-devel

%description
Heimdall is a cross-platform open-source utility to flash firmware (aka ROMs)
onto Samsung Galaxy S devices.

%prep
%setup -q -n Heimdall-Source

#fix rights
chmod 755 configure

#fix EOLs
dos2unix README

%build 
%configure2_5x
%make V=1

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README LICENSE
%{_bindir}/%{name}
