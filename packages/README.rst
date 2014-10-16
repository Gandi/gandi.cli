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

Arch Linux package
==================

Upon release:

- update the 'pkgver' with the tag version
- eventually reset the 'pkgrel' to 1
- eventually update the 'depends' and 'makedepends' lists
- run 'updpkgsums' to update the 'sha256sums' or update it by hand
- run 'makepkg' to build the package
- install and test it!
- run 'mkaurball' to build the source package
- upload it to aur.archlinux.org
