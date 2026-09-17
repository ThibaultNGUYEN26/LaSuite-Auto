# CsvDialect

The CSV dialect descriptor.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**csvddf_version** | **float** | A number to indicate the schema version of CSV Dialect. Version 1.0 was named CSV Dialect Description Format and used different field names. | [optional] [default to 1.2]
**delimiter** | **str** | A character sequence to use as the field separator. | [default to ',']
**double_quote** | **bool** | Specifies the handling of quotes inside fields. | [default to True]
**line_terminator** | **str** | Specifies the character sequence that must be used to terminate rows. | [optional] [default to '''
''']
**null_sequence** | **str** | Specifies the null sequence, for example, &#x60;\\N&#x60;. | [optional] 
**quote_char** | **str** | Specifies a one-character string to use as the quoting character. | [optional] [default to '"']
**escape_char** | **str** | Specifies a one-character string to use as the escape character. | [optional] 
**skip_initial_space** | **bool** | Specifies the interpretation of whitespace immediately following a delimiter. If false, whitespace immediately after a delimiter should be treated as part of the subsequent field. | [optional] [default to False]
**header** | **bool** | Specifies if the file includes a header row, always as the first row in the file. | [optional] [default to True]
**comment_char** | **str** | Specifies that any row beginning with this one-character string, without preceeding whitespace, causes the entire line to be ignored. | [optional] 
**case_sensitive_header** | **bool** | Specifies if the case of headers is meaningful. | [optional] [default to False]

## Example

```python
from grist_client.models.csv_dialect import CsvDialect

# TODO update the JSON string below
json = "{}"
# create an instance of CsvDialect from a JSON string
csv_dialect_instance = CsvDialect.from_json(json)
# print the JSON string representation of the object
print(CsvDialect.to_json())

# convert the object into a dict
csv_dialect_dict = csv_dialect_instance.to_dict()
# create an instance of CsvDialect from a dict
csv_dialect_from_dict = CsvDialect.from_dict(csv_dialect_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


