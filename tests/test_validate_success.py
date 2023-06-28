import pytest
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import Tracker

from actions import actions


def test_validate_mac_address_form_name():
    """Simple test borrowed from https://github.com/RasaHQ/nib-rasa-x"""
    form = actions.ValidateMACAddressForm()
    assert form.name() == "validate_mac_address_form"


@pytest.fixture
def tracker():
    foo = {
        "active_loop": {
            "name": "form_mac_address",
        },
        "events": [
            {
                "event": "active_loop",
                "name": "mac_address_form",
            },
            {
                "event": "slot",
                "name": "requested_slot",
                "value": "mac_address",
            },
            {
                "event": "bot",
                "metadata": {"utter_action": "utter_ask_mac_address"},
                "text": "Enter your MAC address at the prompt.",
            },
            {
                "event": "action",
                "name": "action_listen",
                "policy": "RulePolicy",
            },
            {
                "event": "user",
                "text": "11:22:33:44:55:66",
            },
            {
                "event": "slot",
                "name": "mac_address",
                "value": "11:22:33:44:55:66",
            },
        ],
        "latest_action_name": "mac_address_form",
        "sender_id": "unit_test_user",
        "latest_message": {
            "text": "11:22:33:44:55:66",
        },
        "paused": False,
        "slots": {
            "mac_address": None,
            "mac_failures": 0,
            "requested_slot": "mac_address",
            "session_started_metadata": None,
        },
    }
    return Tracker.from_dict(foo)


@pytest.mark.asyncio
async def test_validate_mac_address_form_success(dispatcher, tracker, domaindict):
    form = actions.ValidateMACAddressForm()
    assert tracker.get_slot("mac_address") is None
    assert tracker.get_slot("mac_failures") == 0
    evt_actual = await form.run(dispatcher, tracker, domaindict)
    assert tracker.get_slot("mac_address") == "11:22:33:44:55:66"
    assert tracker.get_slot("mac_failures") == 0
    assert evt_actual == [SlotSet("mac_address", "11:22:33:44:55:66")]
