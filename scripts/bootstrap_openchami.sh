#!/bin/bash

source /etc/profile.d/openchami.sh

pull_openchami_images

create_podman_secret --name postgres_password --secret supersecretpostgrespasswd
create_podman_secret --name bss_postgres_password --secret supersecretbsspasswd
create_podman_secret --name smd_postgres_password --secret supersecretsmdpasswd
create_podman_secret --name hydra_postgres_password --secret supersecrethydrapasswd
create_podman_secret --name hydra_system_secret --secret supersecretsystempasswd
HYDRA_DSN="postgres://hydra-user:$(podman secret inspect hydra_postgres_password --showsecret | jq -r '.[0].SecretData')@postgres:5432/hydradb?sslmode=disable&max_conns=20&max_idle_conns=4"
create_podman_secret --name hydra_dsn --secret "$HYDRA_DSN"
POSTGRES_MULTIPLE_DATABASES="hmsds:smd-user:$(podman secret inspect smd_postgres_password --showsecret | jq -r '.[0].SecretData'),bssdb:bss-user:$(podman secret inspect bss_postgres_password --showsecret | jq -r '.[0].SecretData'),hydradb:hydra-user:$(podman secret inspect hydra_postgres_password --showsecret | jq -r '.[0].SecretData')"
create_podman_secret --name postgres_multiple_databases --secret "$POSTGRES_MULTIPLE_DATABASES"