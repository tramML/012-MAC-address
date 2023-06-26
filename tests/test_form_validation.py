import json
import pytest

from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.events import SlotSet, ActionExecuted, SessionStarted

from actions import actions
from pathlib import Path



def test_validate_mac_address_form_name():
    """Simple test borrowed from https://github.com/RasaHQ/nib-rasa-x"""
    form = actions.ValidateMACAddressForm()
    assert form.name() == 'validate_mac_address_form'


class TestSuccess:

    @pytest.fixture
    def tracker(self):
        tdict = {
            "sender_id": "unit_test_user",
            "slots": {
              "mac_failures": 0
            },
            "latest_message": {
              "intent": {},
              "entities": [],
              "metadata": {}
            },
            "latest_event_time": 1612422342.865033865,
            "paused": False,
            "events": [
              {
                "event": "action",
                "timestamp": 1612422342.8649258614,
                "name": "action_session_start",
                "confidence": 1.0
              },
              {
                "event": "session_started",
                "timestamp": 1612422342.8649988174,
              },
              {
                "event": "action",
                "timestamp": 1612422342.865033865,
                "name": "action_listen"
              }
            ],
            "active_loop": {
                "name": "form_mac_address",
            },
            "latest_action": {
              "action_name": "action_listen"
            },
            "latest_action_name": "action_listen"
        }
        return Tracker.from_dict(tdict)

    @pytest.mark.asyncio
    async def test_validate_mac_address_form_success(dispatcher, tracker, domain):
        form = actions.ValidateMACAddressForm()
#       import pdb; pdb.set_trace()
        evt_actual = await form.run(dispatcher, tracker, domain)
        evt_expected = [
            SessionStarted(),
            SlotSet("mac_address", "11:22:33:44:55:66"),
            ActionExecuted("action_listen"),
        ]
        assert evt_actual == evt_expected


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
