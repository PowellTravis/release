#!/bin/bash

create_podman_secret() {
    local name=""
    local secret=""
    local force=false
    local random=false
    local length=16

    while [[ $# -gt 0 ]]; do
        case $1 in
            --name)
                name=$2
                shift 2
                ;;
            --secret)
                secret=$2
                shift 2
                ;;
            --force)
                force=true
                shift
                ;;
            --random)
                random=true
                shift
                ;;
            --length)
                length=$2
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                return 1
                ;;
        esac
    done

    if [[ -z $name ]]; then
        echo "Secret name is required"
        return 1
    fi

    if $random; then
        secret=$(tr -dc '[:alnum:]' < /dev/urandom | head -c $length)
    fi

    if [[ -z $secret ]]; then
        echo "Secret content is required"
        return 1
    fi

    if $force; then
        ${CONTAINER_CMD:-docker} secret rm $name 2>/dev/null
    fi

    echo -n $secret | ${CONTAINER_CMD:-docker} secret create $name -
}

create_podman_secret --name postgres_password --secret supersecretpostgrespasswd
create_podman_secret --name bss_postgres_password --secret supersecretbsspasswd
create_podman_secret --name smd_postgres_password --secret supersecretsmdpasswd
create_podman_secret --name hydra_postgres_password --secret supersecrethydrapasswd
create_podman_secret --name hydra_system_secret --secret supersecretsystempasswd
HYDRA_DSN="postgres://hydra-user:$(podman secret inspect hydra_postgres_password --showsecret | jq -r '.[0].SecretData')@postgres:5432/hydradb?sslmode=disable&max_conns=20&max_idle_conns=4"
create_podman_secret --name hydra_dsn --secret "$HYDRA_DSN"
POSTGRES_MULTIPLE_DATABASES="hmsds:smd-user:$(podman secret inspect smd_postgres_password --showsecret | jq -r '.[0].SecretData'),bssdb:bss-user:$(podman secret inspect bss_postgres_password --showsecret | jq -r '.[0].SecretData'),hydradb:hydra-user:$(podman secret inspect hydra_postgres_password --showsecret | jq -r '.[0].SecretData')"
create_podman_secret --name postgres_multiple_databases --secret "$POSTGRES_MULTIPLE_DATABASES"