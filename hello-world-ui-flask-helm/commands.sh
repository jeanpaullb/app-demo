oc new project redhat-app

#Empaquetar el chart (opcional)
helm package hello-world-ui-flask

#Instalar el Helm Chart
helm install hello-world-ui-flask ./hello-world-ui-flask-helm --namespace redhat-app

#Verificar el despliegue
kubectl get all -n demo

#Actualizar el Chart (si es necesario)
helm upgrade hello-world-ui-flask ./hello-world-ui-flask-helm --namespace redhat-app


podman pull registry-quay-quay-operator.apps.acm-dcl.clarocl.com/acm/hello-world-ui-flask:1.0 --tls-verify=false

registry-quay-app.quay-operator.svc.cluster.local:443/acm/hello-world-ui-flask:1.0


oc create secret docker-registry quay-pull-secret \
    --docker-server=registry-quay-app.quay-operator.svc.cluster.local:443 \
    --docker-username=jealopez \
    --docker-password=redhat01 -n redhat-app

oc create secret docker-registry quay-pull-secret \
    --docker-server=registry-quay-quay-operator.apps.acm-dcl.clarocl.com \
    --docker-username=jealopez \
    --docker-password=redhat01 -n redhat-app


oc secrets link default quay-pull-secret --for=pull -n redhat-app

podman pull registry-quay-quay-operator.apps.acm-dcl.clarocl.com/acm/hello-world-ui-flask


openssl s_client -connect registry-quay-quay-operator.apps.acm-dcl.clarocl.com:443

scp quay-ca.crt root@master2-acm:/etc/pki/ca-trust/source/anchors/

oc edit image.config.openshift.io/cluster

oc adm drain worker1-acm.acm-dcl.clarocl.com  --ignore-daemonsets --delete-emptydir-data --force
oc adm drain master1-acm.acm-dcl.clarocl.com  --ignore-daemonsets --delete-emptydir-data --force
oc adm drain master2-acm.acm-dcl.clarocl.com  --ignore-daemonsets --delete-emptydir-data --force
oc adm drain master3-acm.acm-dcl.clarocl.com  --ignore-daemonsets --delete-emptydir-data --force