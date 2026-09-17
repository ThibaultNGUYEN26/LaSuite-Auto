# GetOrgUsage200ResponseAttachments


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_bytes** | **int** | Total attachment storage used in bytes | 
**limit_exceeded** | **bool** | Whether the attachment limit has been exceeded (only present when limit is exceeded) | [optional] 

## Example

```python
from grist_client.models.get_org_usage200_response_attachments import GetOrgUsage200ResponseAttachments

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrgUsage200ResponseAttachments from a JSON string
get_org_usage200_response_attachments_instance = GetOrgUsage200ResponseAttachments.from_json(json)
# print the JSON string representation of the object
print(GetOrgUsage200ResponseAttachments.to_json())

# convert the object into a dict
get_org_usage200_response_attachments_dict = get_org_usage200_response_attachments_instance.to_dict()
# create an instance of GetOrgUsage200ResponseAttachments from a dict
get_org_usage200_response_attachments_from_dict = GetOrgUsage200ResponseAttachments.from_dict(get_org_usage200_response_attachments_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


