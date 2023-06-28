from pathlib import Path

import pytest
from rasa.shared.core.domain import Domain
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


@pytest.fixture(scope="session")
def dispatcher():
    return CollectingDispatcher()


@pytest.fixture
def tracker():
    return Tracker.from_dict(dict(sender_id="unit_tester"))


@pytest.fixture(scope="session")
def domain() -> Domain:
    path = Path(__file__).parent.parent.resolve() / "domain.yml"
    return Domain.from_path(path)


@pytest.fixture(scope="session")
def domaindict(domain) -> DomainDict:
    return domain.as_dict()
