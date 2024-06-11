1. docker-compose up

2. create new virtual env, activate it

3. install items from requirements.txt

4. uvicorn main:app --reload

5. API to clone a public git repo - curl -X 'POST' \
  'http://127.0.0.1:8000/parse-repo/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "repo_url": "https://github.com/shreshthgoyal/gitgraph-bck"
}'

5. List the identifiers curl -X GET http://127.0.0.1:8000/list-identifiers/

6. curl -X 'POST' \  'http://127.0.0.1:8000/get-children-texts/?identifier_name=NameHere' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json'