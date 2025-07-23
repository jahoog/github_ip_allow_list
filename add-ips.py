import requests
import json

GH_TOKEN = '<ENTER YOUR GITHUB TOKEN HERE>'
OWNER_ID = '<ENTER YOUR GITHUB ORG NODE ID>'
HEADERS = {"Authorization": f"bearer {GH_TOKEN}"}

# Delete an entry from the Github Org IP Allow List
def delete_ip_allow_list_entry(entry_id):
    mutation = """
    mutation($id: ID!) {
      deleteIpAllowListEntry(input: { ipAllowListEntryId: $id }) {
        clientMutationId
      }
    }
    """
    variables = {"id": entry_id}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": mutation, "variables": variables},
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()

# Add an entry into the Github Org IP Allow List
def add_ip_allow_entry(owner_id, ip, name=None):
    mutation = '''
    mutation($ownerId: ID!, $ip: String!, $name: String) {
      createIpAllowListEntry(
        input: {
          ownerId: $ownerId
          allowListValue: $ip
          name: $name
          isActive: true
        }
      ) {
        ipAllowListEntry {
          id
          allowListValue
          name
        }
      }
    }
    '''
    variables = {"ownerId": owner_id, "ip": ip, "name": name}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": mutation, "variables": variables},
        headers=HEADERS
    )
    print(response.json())

# Reads in ip-ranges.json and allows to search by region and service.  
# This also filters an exact match of "region" to "network_border_group".  This removes any ranges that exist outside of the region's AZs, such as Local Zones.
# Retrieve Latest ip-ranges.json file at https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html
# See https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-syntax.html for ip-ranges.json syntax
# This only retrieves IPv4 ranges.
def get_ip_ranges(region=None, service=None):
    with open('ip-ranges.json', 'r') as fin:
        data = json.load(fin)
    
    rows = []
    for entry in data.get('prefixes', []):
        if (region is None or entry.get('region', '') == region) and (service is None or entry.get('service', '') == service) and (region is None or entry.get('network_border_group', '') == region):
            rows.append(entry.get('ip_prefix', ''))
    
    return rows

# Reads a file that has newline separated ids and returns a list of ids
def get_id_list(idFileName):
    with open(idFileName, 'r') as fin:
        return fin.read().splitlines()

# Deletes all ids from github IP Allow list that are in a file
def delete_id_list(idFileName):
	for ip in get_id_list(idFileName):
		delete_ip_allow_list_entry(ip)

# EXAMPLE USAGE: Retrieve all IP ranges for the EC2 service in us-west-2 and add to Github IP Allow List
ips_result = get_ip_ranges(region="us-west-2", service="EC2")
count = 0
for ip in ips_result:
    count += 1
    print(ip, "was added")
    add_ip_allow_entry(OWNER_ID, ip, f"EC2 {count}")
print(count, "entries added")

