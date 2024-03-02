import base64

class Headers():
    def get_fingerprint(client):
        try:
            fingerprint = client.get("https://discord.com/api/v9/experiments", timeout=5).json()["fingerprint"]
            return fingerprint
        except Exception as e:
            print("Womp Womp: ", e)
            return

    def get_super_properties():
        properties = '''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}'''
        properties = base64.b64encode(properties.encode()).decode()
        return properties
    
    def get_cookies(client):
        r = client.get("https://discord.com/", timeout=5)
        dcf = r.cookies.get("__dcfduid")
        sdc = r.cookies.get("__sdcfduid")
        return f'__dcfduid={dcf}; __sdcfduid={sdc}'
    
    def get_headers(client , token) -> dict:
        cookies = Headers.get_cookies(client)
        fingerprint = Headers.get_fingerprint(client)
        super_properties = Headers.get_super_properties()
        headers = {
            'authority': 'discord.com',
            'method': 'POST',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-US',
            'authorization': token,
            'cookie': cookies,
            'origin': 'https://discord.com',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-fingerprint': fingerprint,
            'x-super-properties': super_properties,
        }
        return headers
