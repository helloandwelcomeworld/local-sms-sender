import argparse
import sys
import time

import serial


CTRL_Z = b"\x1a"


class ModemError(RuntimeError):
    pass


def read_until(ser: serial.Serial, expected: bytes, timeout: float = 10.0) -> bytes:
    deadline = time.monotonic() + timeout
    data = b""
    while time.monotonic() < deadline:
        chunk = ser.read(ser.in_waiting or 1)
        if chunk:
            data += chunk
            if expected in data or b"ERROR" in data:
                return data
        else:
            time.sleep(0.05)
    return data


def command(ser: serial.Serial, text: str, expected: bytes = b"OK", timeout: float = 10.0) -> bytes:
    ser.write((text + "\r").encode("ascii"))
    response = read_until(ser, expected, timeout)
    if expected not in response:
        raise ModemError(f"Command failed: {text}\nResponse: {response.decode(errors='replace')}")
    return response


def send_sms(port: str, phone: str, message: str, baudrate: int) -> None:
    with serial.Serial(port=port, baudrate=baudrate, timeout=1, write_timeout=5) as ser:
        command(ser, "AT")
        command(ser, "ATE0")
        command(ser, "AT+CMGF=1")
        command(ser, 'AT+CSCS="GSM"')

        ser.write((f'AT+CMGS="{phone}"\r').encode("ascii"))
        prompt = read_until(ser, b">", timeout=10)
        if b">" not in prompt:
            raise ModemError(f"Modem did not accept recipient.\nResponse: {prompt.decode(errors='replace')}")

        safe_message = message.encode("ascii", errors="replace")
        ser.write(safe_message + CTRL_Z)
        response = read_until(ser, b"OK", timeout=60)
        if b"OK" not in response:
            raise ModemError(f"SMS send failed.\nResponse: {response.decode(errors='replace')}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send SMS through a local USB GSM/LTE modem.")
    parser.add_argument("port", help="Serial port, for example COM5")
    parser.add_argument("phone", help="Recipient phone number, for example +15551234567")
    parser.add_argument("message", help="SMS message body")
    parser.add_argument("--baudrate", type=int, default=115200)
    args = parser.parse_args()

    try:
        send_sms(args.port, args.phone, args.message, args.baudrate)
    except (serial.SerialException, ModemError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Sent SMS through modem on {args.port}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
