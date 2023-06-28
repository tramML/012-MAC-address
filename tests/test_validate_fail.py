import json
from pathlib import Path

import pytest
from rasa_sdk.events import ActionExecuted, SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.types import DomainDict

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
        "slots": {"mac_failures": 0, "mac_address": None},
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
async def test_validate_mac_address_form_fail(dispatcher, tracker, domaindict):
    form = actions.ValidateMACAddressForm()
    evt_actual = await form.run(dispatcher, tracker, domaindict)
    assert tracker.get_slot("mac_address") == None
    assert tracker.get_slot("mac_failures") == 1
