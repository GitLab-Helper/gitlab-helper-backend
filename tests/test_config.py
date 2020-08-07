from config import settings


def test_app_name_default_value():
    assert settings.app_name == "Gitlab Helper"


def test_secret_key_default_value():
    assert settings.secret_key == "default_secret_key"


def test_fernet_key_default_value():
    assert settings.fernet_key == bytes("default_fernet_key", "utf-8")


def test_access_token_algorithm_default_value():
    assert settings.access_token_algorithm == "HS256"


def test_access_token_expire_minutes_default_value():
    assert settings.access_token_expire_minutes == 5


def test_refresh_token_expire_minutes_default_value():
    assert settings.refresh_token_expire_minutes == 60
