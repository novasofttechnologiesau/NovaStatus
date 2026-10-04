import sys
import time
from urllib.request import Request, urlopen


def check(url: str) -> tuple[bool, float, str]:
    start = time.perf_counter()
    try:
        with urlopen(Request(url, method="HEAD"), timeout=8) as response:
            return (
                response.status < 500,
                (time.perf_counter() - start) * 1000,
                str(response.status),
            )
    except (OSError, ValueError) as exc:
        return False, (time.perf_counter() - start) * 1000, str(exc)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: novastatus https://example.com [...]", file=sys.stderr)
        raise SystemExit(2)
    failed = False
    for url in sys.argv[1:]:
        ok, latency, detail = check(url)
        failed |= not ok
        print(f"{'UP' if ok else 'DOWN':4} {url} {latency:.1f}ms {detail}")
    raise SystemExit(int(failed))
