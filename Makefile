.PHONY: all clean

all: openchami.rpm

openchami.rpm: openchami.spec
    rpmbuild -bb openchami.spec

clean:
    rm -rf ~/rpmbuild