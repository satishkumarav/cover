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
    "totime": "2020-04-13",
    "source":"MOHRJ"
}
```


| Request Parameter        | Require       | Usage                                                                                            |
| :------------------------|:--------------| :------------------------------------------------------------------------------------------------|
| location                 | yes           | World or Country or City or District                                                             |
| breakdown                | yes           | false - specified location, true - regions belonging to location                                 |
| historical               | yes           | false - latest record, true - all the historical records                                         |
| fromtime                 | no            | if historical = true, from which date YYYY-MM-DD format                                          |
| totime                   | no            | if historical = true, to which date YYYY-MM-DD format                                            |
| rowwis                   | no            | if true, display by timestamp order, false - group by lo                                         |
| source                   | yes           | strongly recommended, World - JHCSEE,India - MOHI, RAJASTHAN - MOHRJ , Telangana - MOHT          |


## Data

| Data                     | Source        | Data Range                                                           |
| :------------------------|:--------------| :--------------------------------------------------------------------|
| World                    | John Hopkins  | All the countries data from Jan 20th to April 16, India - from MOH   |
| India                    | MOHI          | All the States data from Jan 20th to current dae, India - from MOH   |
| Telangana                | MOHT          | All districts for April 15th (WIP)                                   |
| Rajasthan                | MOHRJ         | All districts for April 19th                                         |


### List of the supported countries
```
Italy
Jamaica
Japan
Jordan
Kazakhstan
Kenya
KoreaSouth
Kosovo
Kuwait
Kyrgyzstan
Laos
Latvia
Lebanon
Liberia
Libya
Liechtenstein
Ethiopia
Fiji
Finland
France
Gabon
Gambia
Georgia
Germany
Ghana
Greece
Grenada
Guatemala
Guinea
Guinea-Bissau
Guyana
Haiti
HolySee
Honduras
Hungary
Iceland
India
Indonesia
Iran
Iraq
Ireland
Israel
```
### List of the supported states for India
```Python
AndamanandNicobarIslands
AndhraPradesh
ArunachalPradesh
Assam
Bihar
Chandigarh
Chhattisgarh
Delhi
Goa
Gujarat
Haryana
HimachalPradesh
JammuandKashmir
Jharkhand
Karnataka
Kerala
Ladakh
MadhyaPradesh
Maharashtra
Manipur
Meghalaya
Mizoram
Nagaland
Odisha
Puducherry
Punjab
Rajasthan
TamilNadu
Telangana
Tripura
UttarPradesh
Uttarakhand
WestBengal
```
### List of the districts for Telangana
```
Adilabad
Asifabad
Badradri
Bhupalpally
Hyderabad
Jagtial
Jangaon
Jogulamba
Kamareddy
Karimnagar
Khammam
Mahabubabad
Mahabubnagar
Medak
Medchal
Mulugu
Nagarkurnool
Nalgonda
Nirmal
Nizamabad
Peddapalli
Rajanna
Rangareddy
SangaReddy
Siddipet
Suryapet
Vikarabad
WarangalUrban
```
