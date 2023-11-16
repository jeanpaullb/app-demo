FROM registry.access.redhat.com/ubi8/ubi-minimal:latest

RUN microdnf install -y curl tar gzip \
    && curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh \
    && microdnf clean all

ENTRYPOINT ["trivy"]