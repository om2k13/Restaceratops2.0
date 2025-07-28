
import asyncio, time, logging, argparse, json, os
from .dsl_loader import load_tests, Step
from .client import APIClient
from .assertions import run_assertions, AssertionErrorDetails
from .reporters.console import ConsoleReporter
from .reporters.junit_xml import JUnitReporter
from .reporters.prometheus_exporter import record as prom_record, push as prom_push

log = logging.getLogger("agent.runner")

async def run_step(step: Step, client: APIClient, console: ConsoleReporter, junit: JUnitReporter, semaphore: asyncio.Semaphore):
    async with semaphore:
        start = time.perf_counter()
        ok = False
        error = None
        try:
            req = step.rendered_request()
            resp = await client.request(req["method"], req["url"], json=req.get("json"))
            run_assertions(resp, step.expect)
            step.save_from_response(resp)
            ok = True
        except AssertionErrorDetails as e:
            error = str(e)
        except Exception as e:
            error = f"Exception: {e}"
        latency_ms = (time.perf_counter() - start) * 1000
        console.record(step.name, ok, latency_ms, error)
        junit.record(step.name, ok, latency_ms, error)
        prom_record(step.name, latency_ms/1000, ok)
        return ok

async def run_suite(test_files_dir: str, max_in_flight: int = 5):
    console = ConsoleReporter()
    junit = JUnitReporter()
    semaphore = asyncio.Semaphore(max_in_flight)
    context = {}
    tasks = []

    for file_name, steps in load_tests(test_files_dir):
        for raw_step in steps:
            step = Step(raw_step, context)
            client = APIClient()
            tasks.append(asyncio.create_task(run_step(step, client, console, junit, semaphore)))

    results = await asyncio.gather(*tasks)
    success = all(results)
    junit.write()
    prom_push()
    if console.summary():
        return 0
    return 1

def main():
    parser = argparse.ArgumentParser(description="Restaceratops API-testing agent")
    parser.add_argument("--tests", default="tests", help="Directory containing YAML test files")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrent requests")
    args = parser.parse_args()
    exit_code = asyncio.run(run_suite(args.tests, args.concurrency))
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
