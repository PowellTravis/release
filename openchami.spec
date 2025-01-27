Name:           openchami
Version:        0.9.0
Release:        1%{?dist}
Summary:        OpenCHAMI RPM package

License:        MIT
URL:            https://openchami.org
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
This package installs all the necessary files for OpenChami.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/etc/openchami/configs
mkdir -p %{buildroot}/etc/containers/systemd
mkdir -p %{buildroot}/etc/systemd/system
mkdir -p %{buildroot}/usr/local/bin
mkdir -p %{buildroot}/etc/profile.d


cp -r systemd/configs/* %{buildroot}/etc/openchami/configs/
cp -r systemd/containers/* %{buildroot}/etc/containers/systemd/
cp -r systemd/volumes/* %{buildroot}/etc/containers/systemd/
cp -r systemd/networks/* %{buildroot}/etc/containers/systemd/
cp -r systemd/targets/* %{buildroot}/etc/systemd/system/
cp scripts/bootstrap_openchami_secrets.sh %{buildroot}/usr/local/bin/
cp scripts/openchami_profile.sh %{buildroot}/etc/profile.d/openchami.sh
chmod +x %{buildroot}/usr/local/bin/bootstrap_openchami_secrets.sh

%files
%license LICENSE
/etc/openchami/configs/*
/etc/containers/systemd/*
/etc/systemd/system/openchami.target
/usr/local/bin/bootstrap_openchami_secrets.sh
/etc/profile.d/openchami.sh

%changelog
* Thu Jan 25 2024 Alex Lovell-Troy <alovelltroy@lanl.gov> - 0.9.0-1
- Initial package
