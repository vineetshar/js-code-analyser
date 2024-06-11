1. docker-compose up

2. create new virtual env, activate it , copy .env.sample as .env for neo4j connection creds

3. install items from requirements.txt, pip install -r requirements.txt

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


## Screenshots

![Screenshot 1](screenshots/parserepo.png)
![Screenshot 2](screenshots/getIdentifiers.png)
![Screenshot 3](screenshots/neo4jvisual.png)
![Screenshot 4](screenshots/codeGraph.png)