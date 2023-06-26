import os
from pathlib import Path
import pytest
import json
import sqlalchemy as sa

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from rasa.shared.core.domain import Domain



@pytest.fixture
def dispatcher():
    return CollectingDispatcher()


@pytest.fixture
def tracker():
    return Tracker.from_dict(dict(sender_id="unit_tester"))


@pytest.fixture(scope="session")
def domain() -> Domain:
    path = Path(__file__).parent.parent.resolve() / "domain.yml"
    return Domain.from_path(path)
