import json, subprocess, sys, logging
from multiprocessing import connection
from queue import Empty

def get_instances(resourcegroup = "", gateway = ""):
    cmd = ""
    if resourcegroup != "":
        cmd = "az vm list-ip-addresses --output json --resource-group " + resourcegroup
    else:
         cmd = "az vm list-ip-addresses --output json"

    azure = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (response_json, err ) = azure.communicate()
    exit_code = azure.wait()

    connections = []

    for instance in json.loads(response_json):
        connection = {}
        connection["Name"] = instance.get("virtualMachine").get("name")
        if len(instance.get("virtualMachine").get("network").get("publicIpAddresses")) >= 1:
            connection["ComputerName"] = instance.get("virtualMachine").get("network").get("publicIpAddresses")[0].get("ipAddress")
        else:
            connection["ComputerName"] = instance.get("virtualMachine").get("network").get("privateIpAddresses")[0]
        if gateway != "$CustomProperty.Gateway$":
                if gateway != "":
                    connection["SecureGatewayID"] = gateway
        connection["Type"] = "TerminalConnection"
        connection["TerminalConnectionType"] = "SSH"
        connection["CredentialsFromParent"] = "true"
        #connection["SecureGatewayFromParent"] = "true"
        connections.append(connection)
        
    store = {
        "Objects": connections
    }

    return json.dumps(store)

def main():
    print(get_instances())

if __name__ == "__main__":
    main()