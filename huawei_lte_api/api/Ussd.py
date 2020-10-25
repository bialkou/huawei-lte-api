from collections import OrderedDict
from time import sleep
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType
from huawei_lte_api.exceptions import ResponseErrorException

class Ussd(ApiGroup):
    def get(self):
        return self._connection.get('ussd/get')

    def status(self):
        return self._connection.get('ussd/status')

    def send(self, content, codeType: str = "CodeType") -> GetResponseType:
        self._connection.post_get('ussd/send', OrderedDict((
            ('content', content),
            ('CodeType', codeType)
        )))
        def check_status():
            if self.status()["result"] == "0":
                return self.get()
            else:
                sleep(0.5)
                return check_status()
        sleep(1)
        return check_status()

    def release(self):
        try:
            return self._connection.get('ussd/release')
        except ResponseErrorException:
            pass
