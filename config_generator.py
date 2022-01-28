import json
import time
from api import Api
from argparse import ArgumentParser

class ConfigProcessor:

    def __init__(self, admin_portal_url, access_token, services_list=[], environment="sandbox"):
        self.api = Api(admin_portal_url, access_token, environment)
        self.configuration = {"services":[]}
        self.services_list = services_list

    def fetch_configuration(self):
        if len(self.services_list) == 0:
            self.services_list = self.api.get_services_list()
        
        for service in self.services_list:
            self.configuration['services'].append(self.api.get_service_config(service))

    def dump_configuration(self):
        with open(f"configuration{int(time.time())}.json", "w") as config_output:
            output = json.dumps(self.configuration)
            config_output.write(output)

if __name__ == "__main__":
    # arg parsing
    parser = ArgumentParser()
    parser.add_argument("admin_portal_url", help="Admin Portal URL including scheme://")
    parser.add_argument("access_token", help="Access token")
    parser.add_argument("-s", "--services", dest="services", help="Comma separated list of service ids to include (defaults to all services)") 
    parser.add_argument("-e", "--environment", dest="environment", choices=['production', 'sandbox'], default="sandbox", help="Environment to configure, defaults to sandbox")
    args = parser.parse_args()

    admin_portal = args.admin_portal_url
    access_token = args.access_token
    services_list = []
    environment = "sandbox"
    if args.services:
        services_list = [int(s.strip()) for s in args.services.split(",")]
    if args.environment:
        environment = args.environment
    config_processor = ConfigProcessor(admin_portal, access_token, services_list, environment)
    config_processor.fetch_configuration()
    config_processor.dump_configuration()