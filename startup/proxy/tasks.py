import datetime
import logging

import pendulum
from django.utils.timezone import now
from kubernetes import client, config
from kubernetes.client.rest import ApiException

from startup.proxy.models import Proxy
from startup.settings import SERVICE_NAME, SERVICE_PORT

logger = logging.getLogger(__name__)

config.load_incluster_config()
# config.load_kube_config()
apps_api = client.AppsV1Api()
ingress_api = client.ExtensionsV1beta1Api()


def check_resources():
    for proxy in Proxy.objects.all():
        logger.info(
            "Checking proxy with name %s and %s %s" %
            (proxy.name, proxy.scale_resource_type, proxy.scale_resource_name))
        name = proxy.scale_resource_name
        type = proxy.scale_resource_type
        host = proxy.host
        ingress = find_ingress_for_host(host)
        resource = find_resource(name, type)

        if resource is None:
            continue

        logger.info("%s" % proxy.last_access_time)
        if proxy.start_at and proxy.ends_at and not proxy.autostart:
            if proxy.should_turn_on():
                scale_resource(resource, type=type, replicas=1)
            else:
                scale_resource(resource, type=type, replicas=0)
        elif (proxy.last_access_time +
              datetime.timedelta(minutes=proxy.duration_threshold)) < now():
            scale_resource(resource, type=type, replicas=0)
            change_ingress_service_to_startup_proxy(proxy, ingress, resource)


def get_all_ingresses():
    try:
        response = ingress_api.list_ingress_for_all_namespaces()
        return response.items
    except ApiException as e:
        logger.error("Exception when calling NetworkingV1beta1Api->" +
                     "list_ingress_for_all_namespaces: %s\n" % e)


def change_ingress_service_to_startup_proxy(proxy, ingress, resource):
    logger.info("Changing host %s from ingress %s to startup proxy" %
                (proxy.host, ingress.metadata.name))
    rule = find_host_in_ingress(proxy.host, ingress)
    if len(rule.http.paths) > 0:
        backend = rule.http.paths[0].backend
        backend.service_name = SERVICE_NAME
        backend.service_port = int(SERVICE_PORT)
        rule.http.paths[0].backend = backend
    try:
        ingress_api.patch_namespaced_ingress(ingress.metadata.name,
                                             ingress.metadata.namespace,
                                             ingress)
        logger.info("Patched host %s from ingress %s to sucessfully" %
                    (proxy.host, ingress.metadata.name))
    except ApiException as e:
        logger.error("Exception when calling patch_namespaced_ingress: %s\n" %
                     str(e))


def change_ingress_service_to_normal(ingress, proxy):
    logger.info("Changing host %s from ingress %s to normal" %
                (proxy.host, ingress.metadata.name))
    rule = find_host_in_ingress(proxy.host, ingress)
    if len(rule.http.paths) > 0:
        backend = rule.http.paths[0].backend
        backend.service_name = proxy.service_name
        backend.service_port = proxy.service_port
        rule.http.paths[0].backend = backend
    try:
        ingress_api.patch_namespaced_ingress(ingress.metadata.name,
                                             ingress.metadata.namespace,
                                             ingress)
        logger.info("Patched host %s from ingress %s to normal sucessfully" %
                    (proxy.host, ingress.metadata.name))
    except ApiException as e:
        logger.error("Exception when calling patch_namespaced_ingress: %s\n" %
                     str(e))


def find_resource(name, type):
    if type == "deployment":
        try:
            items = apps_api.list_deployment_for_all_namespaces().items
        except ApiException as e:
            logger.error(
                "Exception when calling list_deployment_for_all_namespaces: %s\n"
                % str(e))
    elif type == "statefulset":
        try:
            items = apps_api.list_stateful_set_for_all_namespaces().items
        except ApiException as e:
            logger.error(
                "Exception when calling list_stateful_set_for_all_namespaces: %s\n"
                % str(e))
    else:
        raise ValueError("Invalid resource type: %s" % (name))

    for item in items:
        if item.metadata.name == name:
            logger.info("Found resource with type %s and name %s" %
                        (name, type))
            return item
    return None


def find_host_in_ingress(host, ingress):
    for conf in ingress.spec.rules:
        if conf.host == host:
            return conf


def find_ingress_for_host(host):
    ingresses = get_all_ingresses()
    for ing in ingresses:
        for conf in ing.spec.rules:
            if conf.host == host:
                return ing


def scale_resource(resource, type, replicas=0):
    logger.info("Scaling resource %s to %s replicas" %
                (resource.metadata.name, replicas))
    resource.spec.replicas = replicas
    if type == "deployment":
        try:
            apps_api.patch_namespaced_deployment(resource.metadata.name,
                                                 resource.metadata.namespace,
                                                 resource)
            logger.info("Patched successfully resource %s" %
                        resource.metadata.name)
        except ApiException as e:
            logger.error(
                "Exception when calling list_deployment_for_all_namespaces: %s\n"
                % str(e))
    elif type == "statefulset":
        try:
            apps_api.patch_namespaced_stateful_set(resource.metadata.name,
                                                   resource.metadata.namespace,
                                                   resource)
            logger.info("Patched successfully resource %s" %
                        resource.metadata.name)
        except ApiException as e:
            logger.error(
                "Exception when calling list_stateful_set_for_all_namespaces: %s\n"
                % str(e))
    else:
        raise ValueError("Invalid resource type: %s" % (type))


def is_ready(proxy):
    name = proxy.scale_resource_name
    type = proxy.scale_resource_type
    resource = find_resource(name, type)
    return resource.status.replicas, resource.status.ready_replicas


def turn_on_resource(proxy):
    name = proxy.scale_resource_name
    type = proxy.scale_resource_type
    ingress = find_ingress_for_host(proxy.host)
    resource = find_resource(name, type)

    if resource is None:
        raise ValueError("Resource not found")

    scale_resource(resource, type, replicas=1)
    change_ingress_service_to_normal(ingress, proxy)


def turn_off_all_resources(filter=None):
    for proxy in Proxy.objects.filter(
            **filter).all() if filter else Proxy.objects.all():
        resource = find_resource(proxy.scale_resource_name,
                                 proxy.scale_resource_type)
        ingress = find_ingress_for_host(proxy.host)
        scale_resource(resource, type=proxy.scale_resource_type, replicas=0)
        change_ingress_service_to_startup_proxy(proxy, ingress, resource)
