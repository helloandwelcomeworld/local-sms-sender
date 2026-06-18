import argparse
import shutil
import subprocess
import sys
from urllib.parse import quote


def require_adb() -> str:
    adb = shutil.which("adb")
    if not adb:
        raise RuntimeError(
            "adb was not found. Install Android Platform Tools and make sure adb.exe is on PATH."
        )
    return adb


def run_adb(adb: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [adb, *args],
        check=False,
        capture_output=True,
        text=True,
    )


def ensure_device(adb: str) -> None:
    result = run_adb(adb, ["devices"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Could not run adb devices.")

    devices = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])

    if not devices:
        raise RuntimeError(
            "No authorized Android device found. Connect the phone, enable USB debugging, "
            "and approve the USB debugging prompt on the phone."
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open a pre-filled SMS compose screen on a connected Android phone."
    )
    parser.add_argument("phone", help="Recipient phone number, for example +15551234567")
    parser.add_argument("message", help="Message body")
    args = parser.parse_args()

    try:
        adb = require_adb()
        ensure_device(adb)
        sms_uri = f"smsto:{args.phone}"
        encoded_body = quote(args.message)
        result = run_adb(
            adb,
            [
                "shell",
                "am",
                "start",
                "-a",
                "android.intent.action.SENDTO",
                "-d",
                sms_uri,
                "--es",
                "sms_body",
                encoded_body,
            ],
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("Opened the SMS compose screen on the connected Android phone.")
    print("Review the message on the phone, then tap send.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
