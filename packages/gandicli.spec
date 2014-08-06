Name: gandicli
Version: 0.1
Release: 1%{?dist}
Summary: Gandi CLI as a service
Group: System Management
License: unknown
URL: http://github.com/gandi/
Source0: gandicli-%{version}.tgz
Provides: gandicli
BuildRequires: python-docutils
Requires: python >= 2.8, python-click, python-yaml
BuildRoot: %{mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
administrate and deploy your gandi resources

%prep
tar xpzf %{sources}

%build
mkdir -p %{buildroot}
rst2man --no-generator gandicli.man.rst | gzip -9 > gandi.1.gz
install -d -m 0755 %{buildroot}/usr/share/man/man1
install -m 0644 gandi.1.gz %{buildroot}/usr/share/man/man1

%clean
rm -r %{buildroot}

%files
%defattr(0755,root,root)
/usr/bin/gandicli
%defattr(0644,root,root)
/usr/share/man/man1/gandi.1.gz
/usr/lib/python2.7/dist-packages/gandi.cli-0.1-nspkg.pth
/usr/lib/python2.7/dist-packages/gandi.cli-0.1.egg-info
/usr/lib/python2.7/dist-packages/gandi.cli

%changelog
* Fri Jul 18 2014 Gandi <feedback@gandi.net> 0.1
- first rpm structure

