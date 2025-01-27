.PHONY: all clean

all: openchami.rpm

tarball:
       mkdir -p ~/rpmbuild/SOURCES
       rm -Rf ~/rpmbuild/SOURCES/openchami-0.9.0.tar.gz
       tar czvf ~/rpmbuild/SOURCES/openchami-0.9.0.tar.gz --transform 's,^,openchami-0.9.0/,' *

openchami.rpm: openchami.spec tarball
       rpmbuild -bb openchami.spec

clean:
       rm -rf ~/rpmbuild
