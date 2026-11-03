# Maintainer: tejonaco: tejonaco@gmail.com
pkgname=libfprint-elan-0c4f-elanpress-git
pkgver=1.94.10.r16.gfa2f98f
pkgrel=1
pkgdesc="libfprint patch for Elan 04f3:0c4f (80x80)"
arch=('x86_64')
url="https://github.com/filip-rs/libfprint"
license=('LGPL-2.1-or-later')
depends=('libgusb' 'pixman' 'nss' 'systemd-libs' 'libgudev' 'glib2')
makedepends=('git' 'meson' 'ninja' 'gobject-introspection' 'glib2-devel' 'python')
provides=('libfprint' 'libfprint-2.so=2-64')
conflicts=('libfprint' 'libfprint-elan-0c4f-press' 'libfprint-elan-0c4f-git')
source=(
  "git+https://github.com/filip-rs/libfprint.git#branch=elanpress"
  "patch-elanpress.py"
)
sha256sums=('SKIP' 'SKIP')

pkgver() {
  cd "$srcdir/libfprint"
  git describe --long --tags --abbrev=7 | sed 's/^v//;s/\([^-]*-g\)/r\1/;s/-/./g'
}

prepare() {
  cd "$srcdir/libfprint"
  git reset --hard HEAD

  python3 "$srcdir/patch-elanpress.py"
}

build() {
  arch-meson "$srcdir/libfprint" build \
    -Ddoc=false \
    -Dinstalled-tests=false
  meson compile -C build
}

package() {
  meson install -C build --destdir "$pkgdir"
}
