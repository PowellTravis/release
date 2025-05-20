Name:           openchami
Version:        %{version}
Release:        %{release}%{?dist}
Summary:        OpenCHAMI RPM package

License:        MIT
URL:            https://openchami.org
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       podman
Requires:       jq
Requires:       curl
Requires:       skopeo

%description
This package installs all the necessary files for OpenChami, including all container images
referenced in the quadlet/systemd-unit files.

%prep
%setup -q

%build
# nothing to build

%install
# 1) Install config, unit, and script files
mkdir -p %{buildroot}/etc/openchami/configs \
         %{buildroot}/etc/openchami/pg-init \
         %{buildroot}/etc/containers/systemd \
         %{buildroot}/etc/systemd/system \
         %{buildroot}/usr/local/bin \
         %{buildroot}/etc/profile.d

cp -r systemd/configs/*           %{buildroot}/etc/openchami/configs/
cp -r systemd/containers/*        %{buildroot}/etc/containers/systemd/
cp -r systemd/volumes/*           %{buildroot}/etc/containers/systemd/
cp -r systemd/networks/*          %{buildroot}/etc/containers/systemd/
cp -r systemd/targets/*           %{buildroot}/etc/systemd/system/
cp -r systemd/system/*            %{buildroot}/etc/systemd/system/
cp scripts/bootstrap_openchami.sh %{buildroot}/usr/local/bin/
cp scripts/openchami_profile.sh   %{buildroot}/etc/profile.d/openchami.sh
cp scripts/multi-psql-db.sh       %{buildroot}/etc/openchami/pg-init/multi-psql-db.sh

chmod +x %{buildroot}/usr/local/bin/bootstrap_openchami.sh
chmod 600 %{buildroot}/etc/openchami/configs/openchami.env
chmod 644 %{buildroot}/etc/openchami/configs/*

# 2) Discover all ghcr.io/openchami image refs
image_list=$(grep -rho \
               --include="*.service" --include="*.target" \
               --include="*.network" --include="*.volume" \
               --include="*.container" \
               -e 'ghcr\.io/openchami[^\s"'"'"'<>]*' \
               %{buildroot}/etc/containers/systemd \
               %{buildroot}/etc/systemd/system \
               %{buildroot}/etc/openchami/configs \
             | grep -v '/$' \
             | sort -u)

# 3) Sync into a temp dir, then pack into one Docker-archive
mkdir -p %{buildroot}%{_datadir}/openchami
TARBALL=openchami-images-%{version}-%{release}.tar
dest_archive="%{buildroot}%{_datadir}/openchami/${TARBALL}"

# make tempdir
TMPDIR=$(mktemp -d)
# build docker:// URIs
sync_args=""
for img in $image_list; do
  sync_args="$sync_args docker://$img"
done

# A) sync all images (deduped) into TMPDIR
skopeo sync \
  --src docker \
  --dest dir:"$TMPDIR" \
  --dest-tls-verify=false \
  $sync_args

# B) copy that dir into a single Docker-archive
skopeo copy \
  --src dir \
  --dest docker-archive:"$dest_archive" \
  "$TMPDIR"

# clean up
rm -rf "$TMPDIR"

%files
%license LICENSE
/etc/openchami/configs/*
/etc/containers/systemd/*
/etc/systemd/system/openchami.target
/etc/systemd/system/openchami-cert-renewal.service
/etc/systemd/system/openchami-cert-renewal.timer
/usr/local/bin/bootstrap_openchami.sh
/etc/profile.d/openchami.sh
/etc/openchami/pg-init/multi-psql-db.sh
%attr(0644,root,root) %{_datadir}/openchami/openchami-images-%{version}-%{release}.tar

%post
# reload systemd so new units are seen
systemctl daemon-reload
# load all the bundled images
podman load -i %{_datadir}/openchami/openchami-images-%{version}-%{release}.tar
# bootstrap
systemctl stop firewalld
/usr/local/bin/bootstrap_openchami.sh

%postun
# reload systemd and remove tarball on uninstall
systemctl daemon-reload
if [ "$1" -eq 0 ]; then
  rm -f %{_datadir}/openchami/openchami-images-%{version}-%{release}.tar
fi

%changelog
* Tue May 20 2025 Your Name <you@example.com> - %{version}-%{release}
- Two-step Skopeo: sync→dir + copy→docker-archive to produce one tag-preserving, deduped tarball  
- Added Requires: skopeo  
- Retained versioned filename, daemon-reload, cleanup  
* Thu Jan 25 2024 Alex Lovell-Troy <alovelltroy@lanl.gov> - 0.9.0-1
- Initial package
