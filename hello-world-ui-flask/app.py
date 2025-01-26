from flask import Flask, render_template
import socket
from kubernetes import client, config

app = Flask(__name__, template_folder="templates")


def get_cluster_info():
    try:
        # Cargar configuración desde dentro del clúster
        config.load_incluster_config()

        # Clientes de la API
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        version_api = client.VersionApi()
        custom_objects_api = client.CustomObjectsApi()

        # Información general del clúster
        server_version = version_api.get_code()
        cluster_data = {
            "api_version": server_version.git_version,
            "platform": server_version.platform,
        }

        # Recuperar la versión de OpenShift
        openshift_version = "Unknown"
        try:
            cluster_version = custom_objects_api.get_cluster_custom_object(
                group="config.openshift.io",
                version="v1",
                plural="clusterversions",
                name="version"
            )
            openshift_version = cluster_version.get("status", {}).get("desired", {}).get("version", "Unknown")
        except Exception:
            openshift_version = "Unknown"

        # Nombre del pod y namespace
        pod_name = socket.gethostname()
        namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read().strip()

        # Información de nodos
        nodes = v1.list_node()
        node_count = len(nodes.items)
        node_info = [
            {
                "name": node.metadata.name,
                "os_image": node.status.node_info.os_image,
                "cpu_capacity": node.status.capacity["cpu"],
                "memory_capacity": node.status.capacity["memory"],
                "kubelet_version": node.status.node_info.kubelet_version,
                "roles": extract_roles(node.metadata.labels),
            }
            for node in nodes.items
        ]

        # Información de Pods
        pods = v1.list_pod_for_all_namespaces()
        pod_count = len(pods.items)

        # Información de Namespaces
        namespaces = v1.list_namespace()
        namespace_count = len(namespaces.items)

        # Información de Deployments
        deployments = apps_v1.list_deployment_for_all_namespaces()
        deployment_count = len(deployments.items)

        # Información de Servicios
        services = v1.list_service_for_all_namespaces()
        service_count = len(services.items)

        # Consolidar información
        return {
            "cluster": cluster_data,
            "openshift_version": openshift_version,
            "pod_name": pod_name,
            "namespace": namespace,
            "node_count": node_count,
            "nodes": node_info,
            "pod_count": pod_count,
            "namespace_count": namespace_count,
            "deployment_count": deployment_count,
            "service_count": service_count,
        }
    except Exception as e:
        print(f"Error obteniendo información del clúster: {e}")
        return {}


def extract_roles(labels):
    """
    Extrae los roles de un nodo basándose en sus etiquetas.
    """
    roles = []
    for key, value in labels.items():
        if "role" in key or "node-role.kubernetes.io" in key:
            if value:  # Algunas etiquetas pueden tener valores vacíos
                roles.append(value)
            else:
                roles.append(key.split("/")[-1])
    return ", ".join(roles) if roles else "worker"


@app.route("/")
def index():
    cluster_data = get_cluster_info()
    return render_template("index.html", data=cluster_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
