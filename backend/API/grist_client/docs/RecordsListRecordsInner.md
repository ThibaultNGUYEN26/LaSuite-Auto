# RecordsListRecordsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **float** |  | 
**fields** | **object** | A JSON object mapping column names to [cell values](https://support.getgrist.com/code/modules/GristData/#cellvalue). | 
**errors** | **object** | Included only when the record has formula errors. Maps the name of each column with an error to the name of the exception; the value in &#x60;fields&#x60; is then &#x60;null&#x60;. See [Grist data format](https://github.com/gristlabs/grist-core/blob/main/documentation/grist-data-format.md). | [optional] [readonly] 

## Example

```python
from grist_client.models.records_list_records_inner import RecordsListRecordsInner

# TODO update the JSON string below
json = "{}"
# create an instance of RecordsListRecordsInner from a JSON string
records_list_records_inner_instance = RecordsListRecordsInner.from_json(json)
# print the JSON string representation of the object
print(RecordsListRecordsInner.to_json())

# convert the object into a dict
records_list_records_inner_dict = records_list_records_inner_instance.to_dict()
# create an instance of RecordsListRecordsInner from a dict
records_list_records_inner_from_dict = RecordsListRecordsInner.from_dict(records_list_records_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


