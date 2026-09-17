# GetOrgUsage200ResponseCountsByDataLimitStatus

Count of documents grouped by data limit status

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**approaching_limit** | **int** |  | [optional] 
**grace_period** | **int** |  | [optional] 
**delete_only** | **int** |  | [optional] 

## Example

```python
from grist_client.models.get_org_usage200_response_counts_by_data_limit_status import GetOrgUsage200ResponseCountsByDataLimitStatus

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrgUsage200ResponseCountsByDataLimitStatus from a JSON string
get_org_usage200_response_counts_by_data_limit_status_instance = GetOrgUsage200ResponseCountsByDataLimitStatus.from_json(json)
# print the JSON string representation of the object
print(GetOrgUsage200ResponseCountsByDataLimitStatus.to_json())

# convert the object into a dict
get_org_usage200_response_counts_by_data_limit_status_dict = get_org_usage200_response_counts_by_data_limit_status_instance.to_dict()
# create an instance of GetOrgUsage200ResponseCountsByDataLimitStatus from a dict
get_org_usage200_response_counts_by_data_limit_status_from_dict = GetOrgUsage200ResponseCountsByDataLimitStatus.from_dict(get_org_usage200_response_counts_by_data_limit_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


