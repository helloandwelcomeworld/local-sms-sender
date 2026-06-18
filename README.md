# Local SMS Sender

This folder contains local-only SMS sender options.

A computer cannot send real SMS by software alone. SMS has to leave through a cellular network, which means you need one of these:

1. An Android phone connected to the computer by USB.
2. A USB GSM/LTE modem with an active SIM card.

No paid SMS API provider is used by these scripts.

## License

MIT

## Free Local Test Mode

This mode is completely free because it does not send a real SMS. It writes the message to a local outbox log so you can test the program flow.

```powershell
python .\dry_run_sms.py +15551234567 "hello from my computer"
```

Real SMS cannot be made free by code alone. To send to an actual phone number, use Option A with an existing Android phone plan or Option B with an active SIM.

## Option A: Android Phone Over USB

This is the easiest no-provider path. It uses your connected Android phone and opens a pre-filled SMS compose screen.

Requirements:

- Android phone with an active SIM/eSIM.
- USB cable.
- Android Platform Tools / `adb`.
- USB debugging enabled on the phone.

Send/open a text:

```powershell
python .\android_adb_sms.py +15551234567 "hello from my computer"
```

The phone will open the messaging app with the recipient and body filled in. Review it on the phone and tap send.

This uses the phone's number. It does not give you a new private number.

## Option B: USB GSM/LTE Modem

This is the closest to a true local computer SMS setup. You plug in a cellular USB modem with a SIM card, then send through the modem.

Install dependency:

```powershell
python -m pip install -r requirements.txt
```

Find the modem COM port in Device Manager, then send:

```powershell
python .\modem_sms.py COM5 +15551234567 "hello from my computer"
```

Replace `COM5` with your modem's port.

Notes:

- The SIM/carrier number is what recipients see.
- Some carriers block SMS on data-only SIMs.
- Some modems do not support SMS text mode. This script uses standard AT commands that work on many, but not all, modems.
- Do not use this for spam, bulk unsolicited messaging, harassment, or bypassing service rules.
