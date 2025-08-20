from utils.is_valid_ip import is_valid
import pytest

def test_is_valid():
    assert is_valid('192.168.1.1') == True

@pytest.mark.parametrize(
        "ip, expected",
        [
        # Válidas
        ("192.168.0.255", True),
        ("8.8.8.8", True),
        ("2001:db8::1", True),   # IPv6
        # Inválidas
        ("256.256.256.256", False),   # valores fuera de rango
        ("192.168.1.999", False),     # último octeto fuera de rango
        ("192.168.1", False),         # incompleta
        ("192.168.1.1.1", False),     # demasiados octetos
        ("abc.def.gha.bcd", False),   # no numérica
        ("192.168.-1.1", False),      # número negativo
        ("1200::AB00:1234::2552:7777:1313", False), # IPv6 con "::" repetido
        ("", False),                  # cadena vacía
        ("...", False),               # solo puntos
    ]
)
def test_is_valid_params(ip: str, expected: bool):
    assert is_valid(ip) == expected
