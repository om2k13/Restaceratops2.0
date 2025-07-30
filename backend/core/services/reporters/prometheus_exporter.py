
from prometheus_client import Summary, CollectorRegistry, push_to_gateway
import os

registry = CollectorRegistry()
LATENCY = Summary('restaceratops_step_latency_seconds', 'Step latency', ['step'], registry=registry)
FAILURES = Summary('restaceratops_step_failures', 'Failed steps', ['step'], registry=registry)

def record(step_name, latency_seconds, success):
    LATENCY.labels(step=step_name).observe(latency_seconds)
    if not success:
        FAILURES.labels(step=step_name).observe(1)

def push():
    gateway = os.getenv("PUSHGATEWAY_URL")
    if gateway:
        push_to_gateway(gateway, job="restaceratops", registry=registry)
