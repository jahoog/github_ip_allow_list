# Github IP Allow List Python Script 
This is a python script to interact with Github IP Allow List for a GH Org.  This is provided as an example with no warranty or support.
*NOTE that this script could add hundreds of IP ranges to your allow list, so make sure that is what you intend.  You can change the service or region to only retrieve those ip ranges that you need. (eg. *CODEBUILD* and *us-east-2*)

## EXAMPLE USAGE: Retrieve all IP ranges for the EC2 service in us-west-2 and add to Github IP Allow List

```
ips_result = get_ip_ranges(region="us-west-2", service="EC2")
count = 0
for ip in ips_result:
    count += 1
    print(ip, "was added")
    add_ip_allow_entry(OWNER_ID, ip, f"EC2 {count}")
print(count, "entries added")
```

## Other Docs
- IP Ranges for AWS: https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html
- IP Range Json file syntax: https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-syntax.html
- Github API for adding AllowList entries: https://docs.github.com/en/graphql/reference/mutations#createipallowlistentry
- Managing Allowlists for your Github org: https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization
