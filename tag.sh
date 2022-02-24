VERSION=$(cat pyproject.toml | grep version | sed 's/.*"\(.*\)"/\1/')
git tag -a v${VERSION} -m ''
