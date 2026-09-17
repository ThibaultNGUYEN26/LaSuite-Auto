# GetOrgUsage200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**counts_by_data_limit_status** | [**GetOrgUsage200ResponseCountsByDataLimitStatus**](GetOrgUsage200ResponseCountsByDataLimitStatus.md) |  | [optional] 
**attachments** | [**GetOrgUsage200ResponseAttachments**](GetOrgUsage200ResponseAttachments.md) |  | [optional] 

## Example

```python
from grist_client.models.get_org_usage200_response import GetOrgUsage200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrgUsage200Response from a JSON string
get_org_usage200_response_instance = GetOrgUsage200Response.from_json(json)
# print the JSON string representation of the object
print(GetOrgUsage200Response.to_json())

# convert the object into a dict
get_org_usage200_response_dict = get_org_usage200_response_instance.to_dict()
# create an instance of GetOrgUsage200Response from a dict
get_org_usage200_response_from_dict = GetOrgUsage200Response.from_dict(get_org_usage200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


