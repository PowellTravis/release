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
# no build step

%install
# Install configs, units, scripts
mkdir -p %{buildroot}/etc/openchami/configs
mkdir -p %{buildroot}/etc/openchami/pg-init
mkdir -p %{buildroot}/etc/containers/systemd
mkdir -p %{buildroot}/etc/systemd/system
mkdir -p %{buildroot}/usr/local/bin
mkdir -p %{buildroot}/etc/profile.d

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
chmod 644 %{buildroot}/etc/openchami/configs/*
chmod 600 %{buildroot}/etc/openchami/configs/openchami.env

# Discover all ghcr.io/openchami image refs in quadlet/unit files
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

# Prepare multi-image archive via Skopeo (deduped, tags preserved)
mkdir -p %{buildroot}%{_datadir}/openchami
TARBALL=openchami-images-%{version}-%{release}.tar
dest_archive="%{buildroot}%{_datadir}/openchami/${TARBALL}"

# Build the list of docker:// URIs
sync_args=""
for img in $image_list; do
  sync_args="$sync_args docker://$img"
done

# Run skopeo sync once
skopeo sync \
  --src docker \
  --dest docker-archive:$dest_archive \
  --dest-tls-verify=false \
  $sync_args

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
# Reload systemd units
systemctl daemon-reload

# Load all bundled container images
podman load -i %{_datadir}/openchami/openchami-images-%{version}-%{release}.tar

# Existing bootstrap
systemctl stop firewalld
/usr/local/bin/bootstrap_openchami.sh

%postun
# Reload systemd and clean up tarball on uninstall
systemctl daemon-reload
if [ "$1" -eq 0 ]; then
  rm -f %{_datadir}/openchami/openchami-images-%{version}-%{release}.tar
fi

%changelog
* Tue May 20 2025 Your Name <you@example.com> - %{version}-%{release}
- Switched to `skopeo sync` with correct image discovery regex
- Single deduplicated, tag-preserving multi-image archive
- Added Requires: skopeo
- Retained versioned tarball, daemon-reload, uninstall cleanup
* Thu Jan 25 2024 Alex Lovell-Troy <alovelltroy@lanl.gov> - 0.9.0-1
- Initial package
