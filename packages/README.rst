Debian packages
===============

create a symbolic link of ./packages/debian to ./debian:
 $ ln -sf ./packages/debian ./debian

start the build process:
 $ debuild -us -uc -b
or
 $ dpkg-buildpackage -rfakeroot -us -uc -b
or use sbuild/pbuilder
 


RPM packages
============
