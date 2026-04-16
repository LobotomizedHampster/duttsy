pkgname=duttsy
pkgver=0.1.0
pkgrel=1
pkgdesc="Simple dotfile manager based on stow."
arch=('any')
url="https://github.com/LobotomizedHampster/duttsy"
license=('MIT')
depends=('python')
makedepends=('git' 'python-build' 'python-installer' 'python-wheel')

source=("git+$url.git")
sha256sums=('SKIP')

build() {
    cd "$srcdir/$pkgname"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$pkgname"
    python -m installer --destdir="$pkgdir" dist/*.whl
}
