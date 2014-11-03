# Copyright 1999-2014 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=5
PYTHON_COMPAT=( python{2_6,2_7,3_2,3_3} )

inherit distutils-r1

MY_PN="${PN//-/.}"
DESCRIPTION="CLI to easily create and manage web resources for your Gandi account."
HOMEPAGE="http://github.com/Gandi/gandicli"
SRC_URI="http://github.com/Gandi/${MY_PN}/archive/${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE=""
REQUIRED_USE="
	${PYTHON_REQUIRED_USE}
"

RDEPEND="
	${PYTHON_DEPS}
	<=dev-python/click-4
	dev-python/requests
	dev-python/pyyaml
"

S=${WORKDIR}/${MY_PN}-${PV}
