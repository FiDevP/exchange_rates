from zeep.transports import AsyncTransport
from zeep import AsyncClient

wsdl = 'http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'
client = AsyncClient(wsdl=wsdl)
with client.settings(raw_response=True):
    response_xml = await str(client.service.GetCursOnDate(f'{day}').text).encode()