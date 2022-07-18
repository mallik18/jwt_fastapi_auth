First start the server: uvicorn src.main:app --reload

Second start providing input with curl:

1. curl localhost:8000/unprotected
-- {"hello":"world"}

2. curl localhost:8000/protected
-- {"detail":"Not authenticated"}

3. curl --header "Content-Type: application/json" --request POST --data '{"username": "ian", "password": "secretpassword"}' localhost:8000/register
-- {}

4. curl --header "Content-Type: application/json" --request POST --data '{"username": "ian", "password": "secretpassword"}' localhost:8000/register
-- {"detail":"Username is taken"}

5. curl --header "Content-Type: application/json" --request POST --data '{"username": "ian", "password": "secretpassword"}' localhost:8000/login
-- {"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTIwODUwNzYsImlhdCI6MTY1MjA4NDc3Niwic3ViIjoiaWFuIn0.g1mZwh6Ufw4pSdfqAbYL42reZNsJOPLpZhAq_buPn_k"}

6. curl --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTIwODUwNzYsImlhdCI6MTY1MjA4NDc3Niwic3ViIjoiaWFuIn0.g1mZwh6Ufw4pSdfqAbYL42reZNsJOPLpZhAq_buPn_k" localhost:8000/protected
-- {"name":"ian"}

After 5 minutes because token has 5 minutes expiration:

7. curl --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTIwODUwNzYsImlhdCI6MTY1MjA4NDc3Niwic3ViIjoiaWFuIn0.g1mZwh6Ufw4pSdfqAbYL42reZNsJOPLpZhAq_buPn_k" localhost:8000/protected
-- {"detail":"Signature has expired"}
