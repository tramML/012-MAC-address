from typing import Text, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


from actions import get_mac


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_mac_address_form"

    def validate_mac_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `mac_address` value."""

        if (mac := get_mac(slot_value)) is not None:
            dispatcher.utter_message(text=f"Recognized MAC address '{mac}'")
            return {"mac_address": mac}

        dispatcher.utter_message(text=f"I don't see a MAC address in '{slot_value}'")
        return {"mac_address": None}
