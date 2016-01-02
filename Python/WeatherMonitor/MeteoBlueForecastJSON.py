import json
import webbrowser
import urllib.request

url='http://my.meteoblue.com/dataApi/dispatch.pl?apikey=41f2dd49fb6a&mac=feed&type=json_7day_3h_firstday&lat=43.5&lon=1.4133&asl=150&tz=Europe%2FZurich&city=Toulouse'


retour_api_meteo = urllib.request.urlopen(url)
Json_string = retour_api_meteo.read().decode('utf-8')
Json_decoded = json.loads(Json_string)
print(json.dumps(Json_decoded['current'],sort_keys=True, indent=4))
print('T° Act:',json.dumps(Json_decoded['current']['temperature']))
print('T° Max:',json.dumps(Json_decoded['forecast'][0]['temperature_max'], sort_keys=True, indent=4))
print('T° Min:',json.dumps(Json_decoded['forecast'][0]['temperature_min'], sort_keys=True, indent=4))
