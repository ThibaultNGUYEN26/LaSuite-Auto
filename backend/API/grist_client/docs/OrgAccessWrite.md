# OrgAccessWrite


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | **Dict[str, str]** |  | 

## Example

```python
from grist_client.models.org_access_write import OrgAccessWrite

# TODO update the JSON string below
json = "{}"
# create an instance of OrgAccessWrite from a JSON string
org_access_write_instance = OrgAccessWrite.from_json(json)
# print the JSON string representation of the object
print(OrgAccessWrite.to_json())

# convert the object into a dict
org_access_write_dict = org_access_write_instance.to_dict()
# create an instance of OrgAccessWrite from a dict
org_access_write_from_dict = OrgAccessWrite.from_dict(org_access_write_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


