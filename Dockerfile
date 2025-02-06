ARG tag=14.0.20231110-debian-11-r0

FROM bitnami/odoo:$tag

ARG ADDONS_PATH="/opt/bitnami/odoo/addons"

ARG BASE_PATH="/opt/bitnami/odoo/bin/odoo-bin"

ARG RUN_SH_PATH="/opt/bitnami/scripts/odoo/run.sh"

ARG COVERAGE_PATH="/opt/bitnami/odoo/coverage"

ARG ODOO_BASE_PATH="/opt/bitnami/odoo"

ARG COVERAGERC_PATH="/opt/bitnami/odoo/.coveragerc"

# copy custom addons
COPY ./addons/ ${ADDONS_PATH}

COPY ./run.sh ${RUN_SH_PATH}

COPY ./.coveragerc ${ODOO_BASE_PATH}

# hadolint ignore=SC1091
RUN ls ${ADDONS_PATH} && \ 
  chmod ugo+x ${RUN_SH_PATH} && \
  chmod ugo+x ${COVERAGERC_PATH} && \
  chmod ugo+x /opt/bitnami/odoo/venv/bin/activate && \
  . /opt/bitnami/odoo/venv/bin/activate && \
  pip3 install --no-cache-dir -r ${ADDONS_PATH}/requirements.txt
