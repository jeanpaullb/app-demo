#local
podman build -t localhost/hello-world-ui:1.0 .
#labjp
podman build -t quay.apps.acm.labjp.xyz/homelab/hello-world-ui-flask:1. .
#clarocl
podman build -t registry-quay-quay-operator.apps.acm-dcl.clarocl.com/acm/hello-world-ui-flask:1.7 .

#labjp
podman login quay.apps.acm.labjp.xyz --tls-verify=false
#clarocl
podman login registry-quay-quay-operator.apps.acm-dcl.clarocl.com

#labjp
podman push quay.apps.acm.labjp.xyz/homelab/hello-world-ui-flask:1.0 --tls-verify=false
#clarocl
podman push registry-quay-quay-operator.apps.acm-dcl.clarocl.com/acm/hello-world-ui-flask:1.7 --tls-verify=false



podman run -d \
  --name hello-world-ui-container \
  --restart=always \
  --replace \
  -p 8080:8080 \
  localhost/hello-world-ui:1.0
