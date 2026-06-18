# Local SMS Sender Shopping List

This list is for running SMS locally from your Windows computer without a paid SMS API provider like Twilio, JMP.chat, OpenPhone, or similar.

Important: real SMS still requires access to a cellular network. That means you need either an active SIM card plan or an existing Android phone plan. The software is local and free to run; carrier network access is not something software can replace.

## Completely Free Mode

Buy nothing.

Use `dry_run_sms.py` to test the workflow locally:

```powershell
python .\dry_run_sms.py +15551234567 "hello from my computer"
```

This is free because it only writes to a local log file. It does not send real SMS.

## Recommended Build: USB Cellular Modem

Buy these:

1. Waveshare SIM7600NA-H 4G HAT
   - Product page: https://www.waveshare.com/sim7600na-h-4g-hat.htm
   - Purpose: the USB cellular modem board that sends SMS through AT commands.
   - Why this model: North America LTE bands, SIM slot, USB interface, SMS support, AT command support.

2. Physical SIM card with SMS service
   - Purpose: gives the modem a real phone number and carrier access.
   - Requirements:
     - Physical SIM card, not eSIM only.
     - SMS/texting enabled.
     - Active service on a carrier/MVNO compatible with your area.
   - Low-cost example: Tello physical SIM + minimal custom plan.

3. Windows computer with a USB port
   - Purpose: runs the Python program and talks to the modem over a COM port.

4. USB-C to USB-A adapter, only if needed
   - Purpose: use this only if your computer has USB-C ports and the included cable is USB-A.

Usually included with the Waveshare kit:

- LTE/SMA antenna
- GPS antenna
- USB type-A to micro-USB cable
- Screws/standoffs

You do not need a Raspberry Pi for this program.

## Alternative Build: Existing Android Phone

Buy nothing if you already have:

1. Android phone with active SMS service
2. USB cable that supports data
3. Windows computer

This uses `android_adb_sms.py`. It opens a pre-filled SMS compose window on the phone. You review and tap send on the phone.

This does not create a new private number. Recipients see your phone's number.

## What Not To Buy

- Old 2G/3G USB SMS sticks. U.S. 2G/3G networks are mostly shut down.
- Hotspots that only expose Wi-Fi internet and no AT-command COM port.
- eSIM-only plans for the Waveshare board.
- A Raspberry Pi, unless you separately want one.

## Minimum Practical Purchase

If you want the local USB modem route:

1. Waveshare SIM7600NA-H 4G HAT
2. Physical SIM card with SMS service
3. USB-C adapter if your computer needs one
