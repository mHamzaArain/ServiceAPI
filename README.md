# Service API
Service API

| Resources            | Protocol | Path      | Parameter                                          | Status code                                                    | Description |
|----------------------|----------|-----------|----------------------------------------------------|----------------------------------------------------------------|-------------|
| Register<br>user     | POST     | /register | username: String<br>pw: String                     | 200 OK                                                         |             |
| Store<br>Sentence    | POST     | /sub      | username: String<br>pw: String<br>sentence: String | 200 OK<br>301 Out of Tokens<br>302 Invalid username & password |             |
| Retrieve<br>Sentence | GET      | /get      | username: String<br>pw: String                     | 200 OK<br>301 Out of Tokens<br>302 Invalid username & password |             |
