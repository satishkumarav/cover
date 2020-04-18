# Cover API to get location base statistics

## Usage
URL: http://<hostname>/cover/api/v1.0/locations

## Request Parameters
Method: Post
Example JSON 
```python
{
    "location": "World",
    "breakdown": true,
    "historical": true,
    "rowwise": true,
    "fromtime": "2020-04-01",
    "totime": "2020-04-13"
}
```


| Request Parameter        | Require       | Usage                                                                |
| :------------------------|:--------------| :--------------------------------------------------------------------|
| location                 | yes           | World or Country or City or District                                 |
| breakdown                | yes           | false - specified location, true - regions belonging to location     |
| historical               | yes           | false - latest record, true - all the historical records             |
| fromtime                 | no            | if historical = true, from which date YYYY-MM-DD format              |
| totime                   | no            | if historical = true, to which date YYYY-MM-DD format                |
| rowwis                   | no            | if true, display by timestamp order, false - group by lo             |

## Data

| Data                     | Source        | Data Range                                                           |
| :------------------------|:--------------| :--------------------------------------------------------------------|
| World                    | John Hopkins  | All the countries data from Jan 20th to April 16, India - from MOH   |
| India                    | MOHI          | All the States data from Jan 20th to current dae, India - from MOH   |
| Telangana                | MOHT          | Telangana district for April 15th (WIP)                              |
