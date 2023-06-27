import json
from pathlib import Path

import pytest
from rasa_sdk.events import ActionExecuted, SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.types import DomainDict

from actions import actions


def test_validate_mac_address_form_name():
    """Simple test borrowed from https://github.com/RasaHQ/nib-rasa-x"""
    form = actions.ValidateMACAddressForm()
    assert form.name() == "validate_mac_address_form"


class TestSuccess:
    """Set up the tracker with conversation info, the slot should be set"""

    @pytest.fixture
    def tracker(self):
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
            "slots": {"mac_failures": 0, "mac_address": None},
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
    async def test_validate_mac_address_form_success(
        self, dispatcher, tracker, domaindict
    ):
        form = actions.ValidateMACAddressForm()
        evt_actual = await form.run(dispatcher, tracker, domaindict)
        assert tracker.get_slot('mac_address') == '11:22:33:44:55:66'
        assert tracker.get_slot('mac_failures') == 0


# @pytest.mark.asyncio
# async def test_validate_mac_address_form_fail(capsys, dispatcher, trackers, domain):
#     action = actions.ValidateMACAddressForm()
#     tracker = trackers["mac_address_fail"]
#     # import pdb; pdb.set_trace()
#     evt_actual = await action.run(dispatcher, tracker, domain)
#     evt_expected = [
#         SessionStarted(),
#         SlotSet("mac_address", "11:22:33:44:55:66"),
#         ActionExecuted("action_listen"),
#     ]
#     captured = capsys.readouterr()
#     assert evt_actual == []
