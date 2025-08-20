from utils.is_reachable import is_reachable
from tests.config import SERVER_GI, SERVER_SIESA
import pytest

@pytest.mark.parametrize(
        "server_ip, expected",
        [
            (SERVER_SIESA, True),
            (SERVER_GI, True)
        ]
)
def test_is_reachable(server_ip: str, expected: bool):
    assert is_reachable(server_ip) == expected