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

%description
This package installs all the necessary files for OpenChami, including all container images
referenced in the quadlet/systemd-unit files.

%prep
%setup -q

%build
# no build step

%install
# -- Install config, unit, script files as before --
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

# -- Discover, pull, and save all ghcr.io/openchami images referenced in those files --
mkdir -p %{buildroot}%{_datadir}/openchami

# gather unique image references
image_list=$(grep -RHo --include="*.service" --include="*.target" --include="*.network" \
                  --include="*.volume" --include="*.container" \
                  -e 'ghcr\.io/openchami[^\s"'\''<>]*' \
                  %{buildroot}/etc/containers/systemd \
                  %{buildroot}/etc/systemd/system \
                  %{buildroot}/etc/openchami/configs \
            | sort -u)

declare -a _imgs
for img in $image_list; do
  echo "Pulling $img"
  podman pull "$img"
  _imgs+=("$img")
done

# include version-and-release in the filename
TARBALL=openchami-images-%{version}-%{release}.tar
echo "Saving images to %{_datadir}/openchami/${TARBALL}"
podman save -m -o %{buildroot}%{_datadir}/openchami/${TARBALL} "${_imgs[@]}"

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
# reload systemd units so new .service/.target files are recognized
systemctl daemon-reload

# load all bundled container images
podman load -i %{_datadir}/openchami/openchami-images-%{version}-%{release}.tar

# existing bootstrap
systemctl stop firewalld
/usr/local/bin/bootstrap_openchami.sh

%postun
# on upgrade or uninstall, reload systemd and clean up old tarball
systemctl daemon-reload
if [ $1 -eq 0 ]; then
  # removal case
  rm -f %{_datadir}/openchami/openchami-images-%{version}-%{release}.tar
fi

%changelog
* Tue May 20 2025 Your Name <you@example.com> - %{version}-%{release}
- Include version-release in tarball filename
- Ensure tarball removed on uninstall
- Run systemctl daemon-reload in %post and %postun
* Thu Jan 25 2024 Alex Lovell-Troy <alovelltroy@lanl.gov> - 0.9.0-1
- Initial package
