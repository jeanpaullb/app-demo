#Empaquetar el chart (opcional)
helm package hello-world-ui-flask

#Instalar el Helm Chart
helm install hello-world-ui-flask ./hello-world-ui-flask --namespace demo --create-namespace

#Verificar el despliegue
kubectl get all -n demo

#Actualizar el Chart (si es necesario)
helm upgrade hello-world-ui-flask ./hello-world-ui-flask --namespace demo
