# Contributor: Anubhav <anubhav7991@gmail.com>
# Contributor: solsTiCe d'Hiver <solstice.dhiver@gmail.com>

pkgname=audiotag-thumbnailer-git
_pkgname=audiotag-thumbnailer
pkgver=1.0
pkgrel=9
pkgdesc="A thumbnailer for audio files"
arch=("any")
url="https://www.github.com/bhav97/audiotag-thumbnailer"
license=("custom:none")
depends=("mutagen" "python3" "python-pillow")
source=("git+https://github.com/bhav97/audiotag-thumbnailer.git")
md5sums=("SKIP")

pkgver() {
	cd ${srcdir}/${_pkgname}
	git rev-list --count HEAD
}

build() {
	cd ${srcdir}/${_pkgname}
}

package() {
	cd ${srcdir}/${_pkgname}
	mkdir -p ${pkgdir}/usr/{share/thumbnailers,bin}
	mv audio_thumbnailer.py audiotag-thumbnailer
	install -m644 audiotag.thumbnailer ${pkgdir}/usr/share/thumbnailers
	install -m755 audiotag-thumbnailer ${pkgdir}/usr/bin
}
