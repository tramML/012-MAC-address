import re
import sys
from typing import Any, Dict, Optional

from rasa_sdk import FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

MAX_VALIDATION_FAILURES = 3


def get_mac(text: str) -> Optional[str]:
    """Return first MAC address matched if present, otherwise None."""
    pat = re.compile(r"\b[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}\b")
    m = re.search(pat, text)
    if m:
        return m[0]
    return None


class ValidateMACAddressForm(FormValidationAction):
    """
    Form is 'mac_address_form', slot is 'mac_address'.
    """

    def name(self) -> str:
        return "validate_mac_address_form"

    def validate_mac_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        """Validate the MAC address utterance."""

        dispatcher.utter_message(text=f"slot value: {slot_value}")
        mac_failures = tracker.slots.get("mac_failures", 0)
        print(f"{slot_value=} {mac_failures=}")
        sys.stderr.write(f"{slot_value=} {mac_failures=}")

        if (mac := get_mac(slot_value)) is not None:
            dispatcher.utter_message(text=f"Recognized MAC address '{mac}'")
            return {"mac_address": mac}
        else:
            mac_failures += 1

        if mac_failures < MAX_VALIDATION_FAILURES:
            dispatcher.utter_message(
                text=f"I don't see a MAC address in '{slot_value}'"
            )
            return {"mac_address": None, "mac_failures": mac_failures}

        # too many failures, exit the form via Arjaan's solution in
        # https://forum.rasa.com/t/how-do-i-deactivate-a-form-during-validation/40169
        dispatcher.utter_message(text="I still don't see a MAC address.")
        dispatcher.utter_message(text="Please contact customer support at 555-1212.")
        return {"mac_address": None, "requested_slot": None}


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
