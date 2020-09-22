Name: gandicli
Version: 1.6
Release: 1%{?dist}
Summary: Gandi CLI as a service
Group: System Management
License: unknown
URL: http://github.com/gandi/
Source0: gandicli-%{version}.tar.gz
Provides: gandicli
BuildRequires: python-docutils, python2-devel
Requires: python >= 2.7, python-click, python-yaml, python-requests
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
administrate and deploy your gandi resources

%prep
%setup -n gandi.cli-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
rst2man --no-generator gandicli.man.rst | gzip -9 > gandi.1.gz
install -d -m 0755 %{buildroot}/usr/share/man/man1
install -m 0644 gandi.1.gz %{buildroot}/usr/share/man/man1

%clean
rm -r %{buildroot}

%files
%defattr(0755,root,root)
/usr/bin/gandi
%defattr(0644,root,root)
/usr/share/man/man1/gandi.1.gz
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*-nspkg.pth
%{python2_sitelib}/gandi/

%changelog
* Fri Jul 18 2014 Gandi <feedback@gandi.net> 0.1
- first rpm structure

