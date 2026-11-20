import re
import ipaddress

# IPv4 candidate extraction pattern
pattern = r'(?<![0-9.])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9.])'

samples = [
    "<string>Server: 193.11.166.194</string>",
    "<string>Version: 3608.80.24.1.8</string>",
    "<string>Server: 192.168.1.256</string>",
    "<string>Address: 10.0.0.1</string>",
    "<string>Server: 172.16.0.5</string>",
]

for text in samples:

    candidates = re.findall(pattern, text)

    print("\nOriginal text:", text)

    if not candidates:
        print("No candidate found")
        continue

    for candidate in candidates:

        try:
            ipaddress.IPv4Address(candidate)
            print(candidate, "-> Valid IPv4")

        except ipaddress.AddressValueError:
            print(candidate, "-> Invalid IPv4")
