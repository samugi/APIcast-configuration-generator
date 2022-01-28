import requests 
import json 

class Api:
    def __init__(self, admin_portal_url, access_token, environment):
        self.admin_portal_url = admin_portal_url
        self.access_token = access_token
        self.environment = environment

    def get_services_list(self):
        page = 1
        services = []
        while True:
            r = requests.get(f"{self.admin_portal_url}/admin/api/services.json?access_token={self.access_token}&page={str(page)}&per_page=500", verify=False)

            json_resp = r.json()
            svcs = json_resp["services"]
        
            if len(svcs) == 0:
                break

            for service_container in svcs:
                service = service_container["service"]
                services.append(service["id"])
                
            page += 1
        return services

    def get_service_config(self, service_id):
        r = requests.get(f"{self.admin_portal_url}/admin/api/services/{service_id}/proxy/configs/{self.environment}/latest.json?access_token={self.access_token}", verify=False)
        json_resp = r.json()
        return json_resp['proxy_config']['content']
        