# Maintainer: AdmiralAkber

pkgname='thinkpad-yoga-14-s3-git'
_gitname='thinkpad-yoga-14-s3'
pkgver=20150329
pkgrel=2
pkgdesc='A collection of scripts and systemd services for tablet functionality of the ThinkPad Yoga 14 S3'
url="https://github.com/johanneswilm/thinkpad-yoga-14-s3"
source=('thinkpad-yoga-14-s3::git+https://github.com/johanneswilm/thinkpad-yoga-14-s3')
license=('GPL3')
arch=('any')
depends=('xorg-xrandr' 'xorg-xinput' 'xbindkeys' 'kbd' 'systemd' 'gawk')
md5sums=('SKIP')
makedepends=('git')
install=$pkgname.install

pkgver() {
  cd "$_gitname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
  cd $srcdir/$_gitname

  # Install scripts into /opt
  mkdir -p "$pkgdir/opt/$_gitname"
  ## Rotate scripts
  cp -r rotate "$pkgdir/opt/$_gitname"
  ## Backlight script
  cp -r backlight "$pkgdir/opt/$_gitname"

  # ThinkPad Yoga Systemd Services
  mkdir -p "$pkgdir/usr/lib/systemd/system/"
  cp systemd/*.service "$pkgdir/usr/lib/systemd/system/"

  # Install license
  install -D -m644 "LICENSE" "$pkgdir/usr/share/licenses/$_gitname/LICENSE"
}
