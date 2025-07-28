
import logging, time, json

class ConsoleReporter:
    def __init__(self):
        self.results = []
        self.start_time = time.time()

    def record(self, step_name, success, latency_ms, error=None):
        self.results.append((step_name, success, latency_ms, error))

    def summary(self):
        total = len(self.results)
        fails = [r for r in self.results if not r[1]]
        print("\n\n=== Restaceratops Report ===")
        for name, ok, latency, err in self.results:
            badge = "✓" if ok else "✗"
            print(f"{badge} {name} ({latency:.1f} ms)")
            if err:
                print(f"    → {err}")
        print(f"Total: {total}, Failed: {len(fails)}, Time: {(time.time()-self.start_time):.1f}s")
        return len(fails) == 0
