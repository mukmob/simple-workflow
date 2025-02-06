#!/bin/bash
# Copyright Broadcom, Inc. All Rights Reserved.
# SPDX-License-Identifier: APACHE-2.0

# shellcheck disable=SC1090,SC1091


set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purposes

# Load Odoo environment
. /opt/bitnami/scripts/odoo-env.sh

# Load libraries
. /opt/bitnami/scripts/libos.sh
. /opt/bitnami/scripts/liblog.sh
. /opt/bitnami/scripts/libodoo.sh

declare ODOO_BASE_DIR="/opt/bitnami/odoo"
declare ODOO_CONF_FILE="${ODOO_BASE_DIR}/conf/odoo.conf"
declare ODOO_BIN="${ODOO_BASE_DIR}/bin/odoo"
declare ODOO_DAEMON_USER="odoo"
declare ODOO_VENV_COVERAGE="/opt/bitnami/odoo/venv/bin/coverage"
declare ODOO_COVERAGE_RCFILE="/opt/bitnami/odoo/.coveragerc"

# Add the coverage file path
declare ODOO_COVERAGE_FOLDER="/opt/bitnami/odoo/coverage/"
# Check if the folder exists
if [ -d "$ODOO_COVERAGE_FOLDER" ]; then
    # Change the ownership of the folder
    chown "$ODOO_DAEMON_USER" "$ODOO_COVERAGE_FOLDER"
else
    echo "Folder $ODOO_COVERAGE_FOLDER does not exist."
fi

declare cmd="${ODOO_VENV_COVERAGE}"
declare coverage_rcfile="${ODOO_COVERAGE_RCFILE}"
declare run="run"
declare odoo_bin="$ODOO_BIN"
declare -a args=("--config" "$ODOO_CONF_FILE" "$@")

info "** Starting Odoo **"

if am_i_root; then
    info "** Starting Odoo to run coverage **"
    exec_as_user "$ODOO_DAEMON_USER" "$cmd" "$run" "--rcfile=$coverage_rcfile" "$odoo_bin" "${args[@]}"
else
    printf "running as non-root"
    ls -al
    exec "$cmd" "${args[@]}"
fi


