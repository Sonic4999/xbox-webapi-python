import pytest
from betamax import Betamax

from xbox.webapi.common.exceptions import AuthenticationException
from xbox.webapi.authentication.token import AccessToken, RefreshToken, UserToken, XSTSToken


def test_extract_js_node(auth_manager, windows_live_authenticate_response):
    js_node = auth_manager._extract_js_object(windows_live_authenticate_response, 'ServerData')

    assert js_node is not None
    assert js_node['sFTTag'] == "<input name=\"PPFT\" value=\"normally_base64_encoded_string_here+\"/>"
    assert js_node['urlPost'] == "https://login.live.com/ppsecure/post.srf?response_type=token"


def test_auth_invalid_credentials(auth_manager):
    auth_manager.email_address = "invalid@mail.com"
    auth_manager.password = "abc123"

    with Betamax(auth_manager.session).use_cassette('invalid_auth'):
        with pytest.raises(AuthenticationException):
            auth_manager.authenticate()


def test_auth_valid_credentials(auth_manager):
    auth_manager.email_address = "pyxb-testing@outlook.com"
    auth_manager.password = "password"

    with Betamax(auth_manager.session).use_cassette('full_auth'):
        auth_manager.authenticate(do_refresh=False)

    assert auth_manager.xsts_token.is_valid is True
    assert auth_manager.access_token.is_valid is True
    assert auth_manager.refresh_token.is_valid is True
    assert auth_manager.user_token.is_valid is True
    assert auth_manager.userinfo.userhash == '1674471606081042789'
    assert auth_manager.userinfo.xuid == '2535428504476914'
    assert auth_manager.userinfo.gamertag == 'xboxWebapiGamertag'
