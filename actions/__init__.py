import re
from typing import Optional


def get_mac(text: str) -> Optional[str]:
    """Return first MAC address matched if present, otherwise None."""
    pat = re.compile(r"\b[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}\b")
    m = re.search(pat, text)
    if m:
        return m[0]
    return None


if __name__ == "__main__":
    tests = [
        "11:22:33:44:55:66",
        "aa:bb:cc:dd:ee:ff",
        'my mac address is "aa:bb:cc:dd:ee:ff"',
        'my mac address is "aa:BB:cC:dD:EE:11"',
        'my mac address is "aa:BB:cC:dD:EE:11:gg"',
        'my mac address is "aa:BB:cC:dD:EE:11gg"',
        '"aa:bb:cc:dd:ee:ff"',
    ]

    for t in tests:
        print(f"'{t}' ==> '{get_mac(t)}'")
