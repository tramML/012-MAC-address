import pytest
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import Tracker

from actions import actions


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
                "text": "1.2.3.4",
            },
            {
                "event": "slot",
                "name": "mac_address",
                "value": "1.2.3.4",
            },
        ],
        "latest_action_name": "mac_address_form",
        "sender_id": "unit_test_user",
        "latest_message": {
            "text": "1.2.3.4",
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
@pytest.mark.filterwarnings("ignore:Slot auto-fill has been removed")
async def test_validate_mac_address_form_fail(dispatcher, tracker, domaindict):
    form = actions.ValidateMACAddressForm()
    assert tracker.get_slot("mac_address") is None
    assert tracker.get_slot("mac_failures") == 0
    evt_actual = await form.run(dispatcher, tracker, domaindict)
    assert tracker.get_slot("mac_address") is None
    assert tracker.get_slot("mac_failures") == 1
    assert evt_actual == [
        SlotSet("mac_address", None),
        SlotSet("mac_failures", 1),
    ]
