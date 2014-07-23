# Copyright 1999-2014 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=5

PYTHON_COMPAT=( python{2_7} )

inherit distutils-r1

DESCRIPTION="Updater daemon for TwoDNS"
HOMEPAGE="https://github.com/tablet-mode/twod"
SRC_URI="https://github.com/tablet-mode/twod/tarball/${PV} -> ${P}.tar.gz"

LICENSE="GPLv3"
SLOT="0"
KEYWORDS="~x86 ~amd64"
IUSE=""

DEPEND="dev-python/setuptools[${PYTHON_USEDEP}]"
RDEPEND="${DEPEND}"

python_test() {
	esetup.py test
}
