from actions.actions import get_mac


def test_mac_address_extractor():

    assert get_mac("") is None
    assert get_mac("aabbccddeeff") is None
    assert get_mac("11:22:33:44:55:66") == "11:22:33:44:55:66"
    assert get_mac("my mac address is 11:22:33:44:55:66") == "11:22:33:44:55:66"
    assert get_mac("adsfads 11:22:33:44:55:66 asdfadsf") == "11:22:33:44:55:66"
    assert get_mac("11:22:33:aa:bb:cc") == "11:22:33:aa:bb:cc"
    assert get_mac("11:22:33:AA:BB:CC") == "11:22:33:AA:BB:CC"
    assert get_mac("aa:bb:cc:dd:ee:ff") == "aa:bb:cc:dd:ee:ff"
