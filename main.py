from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j_store import Neo4jASTStore
from js_parser import parse_code, build_ast, print_ast
from git_utils import clone_repo, delete_repo, get_js_files

app = FastAPI()

class RepoInput(BaseModel):
    repo_url: str

@app.post("/parse-repo/")
async def parse_repository(input: RepoInput):
    repo_url = input.repo_url
    dest_path = f"cloned-repos/{repo_url.split('/')[-1]}"
    
    clone_repo(repo_url, dest_path)
    
    js_files = get_js_files(dest_path)
    if not js_files:
        delete_repo(dest_path)
        raise HTTPException(status_code=400, detail="No JavaScript files found in the repository.")

    all_information = []

    for js_file in js_files:
        with open(js_file, 'r', encoding='utf8') as f:
            code = f.read()
        tree = parse_code(code)
        root_node = tree.root_node
        information = await build_ast(root_node)
        all_information.append(information)

    neo4j_store = Neo4jASTStore("bolt://localhost:7687", "neo4j", "password")
    for information in all_information:
        neo4j_store.store_ast(information)
    neo4j_store.close()

    delete_repo(dest_path)

    return {"status": "success"}

@app.post("/get-children-texts/")
def get_children_texts(identifier_name: str):
    neo4j_store = Neo4jASTStore("bolt://localhost:7687", "neo4j", "password")
    children_texts = neo4j_store.get_children_text(identifier_name)
    neo4j_store.close()

    if not children_texts:
        raise HTTPException(status_code=404, detail="No children found for the given identifier name")
    
    return {"identifier_name": identifier_name, "children_texts": children_texts}

@app.get("/list-identifiers/")
def list_identifiers():
    neo4j_store = Neo4jASTStore("bolt://localhost:7687", "neo4j", "password")
    identifiers = neo4j_store.list_identifiers()
    neo4j_store.close()

    return {"identifiers": identifiers}