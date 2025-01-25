oc create secret generic --from-file config.yaml=./config.yaml registry-config-bundle-secret

oc create secret generic registry-config-bundle-secret --from-file=config.yaml=./config.yaml -n quay-operator --dry-run=client -o yaml | oc apply -f -


---
oc rsh registry-quay-database-76886fc865-8z5x2

psql -U registry-quay-database -d registry-quay-database


oc get secret registry-quay-database -n quay-operator -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 -d


SELECT email, last_accessed FROM user;
SELECT * FROM "user";
\dt

curl -kv -X POST -H "Content-Type: application/json" \
  -d '{
    "username": "quayadmin",
    "email": "quayadmin@mail.com",
    "password": "password123",
    "super_user": true
  }' \
  https://registry-quay-quay-operator.apps.acm-dcl.clarocl.com/api/v1/user/initialize

#Para crear