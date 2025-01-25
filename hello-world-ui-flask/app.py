from flask import Flask, render_template
import os
import platform
import socket
from kubernetes import client, config

app = Flask(__name__, template_folder="templates")

def get_cluster_info():
    try:
        # Cargar configuración desde dentro del clúster
        config.load_incluster_config()

        # Cliente de la API
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        version_api = client.VersionApi()

        # Información del clúster
        server_version = version_api.get_code()
        cluster_data = {
            "api_version": server_version.git_version,
            "platform": server_version.platform,
        }

        # Información de nodos
        nodes = v1.list_node()
        node_info = [
            {
                "name": node.metadata.name,
                "cpu_capacity": node.status.capacity["cpu"],
                "memory_capacity": node.status.capacity["memory"],
                "kubelet_version": node.status.node_info.kubelet_version,
                "roles": node.metadata.labels.get("kubernetes.io/role", "worker"),
            }
            for node in nodes.items
        ]

        # Información de Pods
        pods = v1.list_pod_for_all_namespaces()
        pod_info = {
            "total_pods": len(pods.items),
            "pods_by_namespace": {},
        }
        for pod in pods.items:
            ns = pod.metadata.namespace
            pod_info["pods_by_namespace"].setdefault(ns, 0)
            pod_info["pods_by_namespace"][ns] += 1

        # Información de Deployments
        deployments = apps_v1.list_deployment_for_all_namespaces()
        deployment_info = {
            "total_deployments": len(deployments.items),
        }

        # Información del almacenamiento
        pvs = v1.list_persistent_volume()
        pv_info = [
            {
                "name": pv.metadata.name,
                "capacity": pv.spec.capacity["storage"],
                "access_modes": pv.spec.access_modes,
                "reclaim_policy": pv.spec.persistent_volume_reclaim_policy,
                "status": pv.status.phase,
            }
            for pv in pvs.items
        ]

        # Consolidar información
        return {
            "cluster": cluster_data,
            "nodes": node_info,
            "pods": pod_info,
            "deployments": deployment_info,
            "pvs": pv_info,
        }
    except Exception as e:
        print(f"Error obteniendo información del clúster: {e}")
        return {}

@app.route("/")
def index():
    cluster_data = get_cluster_info()
    return render_template("index.html", data=cluster_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
