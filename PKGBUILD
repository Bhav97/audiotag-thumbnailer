# Contributor: Anubhav <anubhav7991@gmail.com>
# Contributor: solsTiCe d'Hiver <solstice.dhiver@gmail.com>

pkgname=audiotag-thumbnailer-git
_pkgname=audiotag-thumbnailer
pkgver=1.0
pkgrel=5
pkgdesc="A nautilus thumbnailer for audio files"

arch=("any")
url="https://www.github.com/bhav97/audiotag-thumbnailer"
license=("custom:none")
depends=("mutagen" "python3")
source=("git+https://www.github.com/bhav97/audiotag-thumbnailer.git")
md5sums=("SKIP")

pkver() {
	cd ${srcdir}/${_pkgname}
	git rev-lisr --count HEAD
}

build() {
	cd ${srcdir}/${_pkgname}
}

package() {
	mkdir -p ${pkgdir}/usr/{share/thumbnailers,bin}
	install -m644 audiotag.thumbnailer $p"{pkgdir}/usr/share/thumbnailers
	install -m755 audiotag-thumbnailer ${pkgdir}/usr/bin
}
