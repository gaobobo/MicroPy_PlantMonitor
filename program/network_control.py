from network import (WLAN,
                     STA_IF,
                     STAT_CONNECTING,
                     STAT_WRONG_PASSWORD,
                     STAT_NO_AP_FOUND,
                     STAT_GOT_IP)
from asyncio import sleep

class NetworkError(Exception): pass
class NetworkWrongPasswordError(NetworkError): pass
class NetworkNoAPFoundError(NetworkError): pass


def disconnect(wlan:WLAN) -> None:
    wlan.disconnect()


def connect(wlan:WLAN, ssid:str, password:str) -> None:
    """Must disconnect first when connect others network.
    This func is not block, so you can check the connection status
    use wlan.status() ."""
    wlan.active(True)

    if wlan.isconnected(): return

    wlan.connect(ssid, password)


async def async_connect(wlan:WLAN, ssid:str, password:str, refresh_cycle_sec:float) -> None:
    """
    Must disconnect first when connect others network.

    This func is async and will throw exception when wlan is not connected and
    connect successfully return None.
    :param wlan: WLAN Object
    :param ssid: connect ssid
    :param password: connect password
    :param refresh_cycle_sec: seconds to check connect status per cycle. Support float.
    """
    wlan.active(True)

    if wlan.isconnected(): return

    wlan.connect(ssid, password)

    while wlan.status() == STAT_CONNECTING:
        await sleep(refresh_cycle_sec)

    if wlan.status() == STAT_GOT_IP:
        return
    elif wlan.status() == STAT_WRONG_PASSWORD:
        raise NetworkWrongPasswordError()
    elif wlan.status() == STAT_NO_AP_FOUND:
        raise NetworkNoAPFoundError()
    else:
        raise NetworkError()


def get_level(wlan:WLAN) -> int|None :
    """
    return rssi of WI-FI.
    :return: an int value of rssi. > -50 is 2, > -70 is 1, else is 0, disconnect is None.
    """

    if not wlan.isconnected(): return None

    rssi = wlan.status('rssi')

    if rssi > -50: return 2
    elif rssi > -70: return 1
    else: return 0
