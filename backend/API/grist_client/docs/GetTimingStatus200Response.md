# GetTimingStatus200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | - disabled: timing is not enabled - pending: timing is enabled but no data yet - active: timing is enabled and data is available  | 
**timing** | **object** | Timing data (only present when status is &#39;active&#39;) | [optional] 

## Example

```python
from grist_client.models.get_timing_status200_response import GetTimingStatus200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetTimingStatus200Response from a JSON string
get_timing_status200_response_instance = GetTimingStatus200Response.from_json(json)
# print the JSON string representation of the object
print(GetTimingStatus200Response.to_json())

# convert the object into a dict
get_timing_status200_response_dict = get_timing_status200_response_instance.to_dict()
# create an instance of GetTimingStatus200Response from a dict
get_timing_status200_response_from_dict = GetTimingStatus200Response.from_dict(get_timing_status200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


