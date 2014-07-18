Name: gandicli
Version: 0.1
Release: 1%{?dist}
Summary: Gandi CLI as a service
Group: System Management
License: unknown
URL: http://github.com/gandi/
Source0: gandicli-%{version}.tgz
Provides: gandicli
Requires: python
BuildRoot: %{mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Vous permet d'administrer, déployer vos instances Gandi

%prep
tar xpzf %{sources}

%build
mkdir -p %{buildroot}

%clean
rm -r %{buildroot}

%pre
echo nothing

%post
echo nooo

%postun
rm /etc/gandi/cli.yaml

%files
%defattr(0640,root,adm)
/etc/gandi/cli.yaml
%defattr(0644,root,root)
/usr/bin/gandicli

%changelog
* Fri Jul 18 2014 name surname <email> 0.1
- first rpm structure

