from actions import actions


def test_validate_mac_address_form_name():
    """Simple test borrowed from https://github.com/RasaHQ/nib-rasa-x"""
    form = actions.ValidateMACAddressForm()
    assert form.name() == "validate_mac_address_form"
