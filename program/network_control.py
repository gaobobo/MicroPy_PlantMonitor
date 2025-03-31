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

class network_control:

    wlan:WLAN = None

    def __init__(self, ssid:str, password:str):
        self.ssid = ssid
        self.password = password
        self.wlan = WLAN(mode=STA_IF)


    def disconnect(self):
        self.wlan.disconnect()

    def connect(self):
        """Must disconnect first when connect others network.
        This func is not block, so you can check the connection status
        use self.wlan.status() ."""
        self.wlan.active(True)

        if self.wlan.isconnected(): return

        self.wlan.connect(self.ssid, self.password)


    async def async_connect(self, refresh_cycle_sec:float) -> None:
        """
        Must disconnect first when connect others network.

        This func is async and will throw exception when wlan is not connected and
        connect successfully return None.
        :param refresh_cycle_sec: seconds to check connect status per cycle. Support float.
        """
        self.wlan.active(True)

        if self.wlan.isconnected(): return

        self.wlan.connect(self.ssid, self.password)

        while self.wlan.status() == STAT_CONNECTING:
            await sleep(refresh_cycle_sec)

        if self.wlan.status() == STAT_GOT_IP:
            return
        elif self.wlan.status() == STAT_WRONG_PASSWORD:
            raise NetworkWrongPasswordError()
        elif self.wlan.status() == STAT_NO_AP_FOUND:
            raise NetworkNoAPFoundError()
        else:
            raise NetworkError()


    def get_level(self) -> int|None :
        """
        return rssi of WI-FI.
        :return: an int value of rssi. > -50 is 2, > -70 is 1, else is 0, disconnect is None.
        """

        if not self.wlan.isconnected(): return None

        rssi = self.wlan.status('rssi')

        if rssi > -50: return 2
        elif rssi > -70: return 1
        else: return 0
