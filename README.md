# Service API
Service API

| Resources         | Protocol | Path      | Description      | Parameter                                    | Status code                                              |
|-------------------|----------|-----------|------------------|----------------------------------------------|----------------------------------------------------------|
| Register user     | POST     | /register | add 2 nums       | username: String pw: String                  | 200 OK                                                   |
| Store Sentence    | POST     | /sub      | subtract 2 nums  | username: String pw: String sentence: String | 200 OK 301 Out of Tokens 302 Invalid username & password |
| Retrieve Sentence | GET      | /get      | multuiply 2 nums | username: String pw: String                  | 200 OK 301 Out of Tokens 302 Invalid username & password |
