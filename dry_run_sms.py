import argparse
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Free local test mode. Logs an SMS request without sending a real SMS."
    )
    parser.add_argument("phone", help="Recipient phone number, for example +15551234567")
    parser.add_argument("message", help="Message body")
    parser.add_argument(
        "--out",
        default="outbox.log",
        help="Local log file to append to. Default: outbox.log",
    )
    args = parser.parse_args()

    out_path = Path(args.out)
    timestamp = datetime.now().isoformat(timespec="seconds")
    out_path.write_text(
        (out_path.read_text(encoding="utf-8") if out_path.exists() else "")
        + f"[{timestamp}] TO {args.phone}: {args.message}\n",
        encoding="utf-8",
    )
    print(f"Dry run saved to {out_path.resolve()}")
    print("No real SMS was sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
