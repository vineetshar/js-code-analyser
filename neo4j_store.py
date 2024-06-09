# neo4j_store.py

from neo4j import GraphDatabase

class Neo4jASTStore:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, tx, node_id, node_type, text):
        query = (
            "CREATE (n:ASTNode {id: $node_id, type: $node_type, text: $text})"
        )
        tx.run(query, node_id=node_id, node_type=node_type, text=text)

    def create_relationship(self, tx, parent_id, child_id):
        query = (
            "MATCH (p:ASTNode {id: $parent_id}), (c:ASTNode {id: $child_id}) "
            "CREATE (p)-[:HAS_CHILD]->(c)"
        )
        tx.run(query, parent_id=parent_id, child_id=child_id)

    def store_ast(self, root):
        with self.driver.session() as session:
            self._store_node_recursive(session, root, None)

    def _store_node_recursive(self, session, node, parent_id):
        node_id = id(node)
        with session.begin_transaction() as tx:
            self.create_node(tx, node_id, node.node_type, node.text)

            if parent_id is not None:
                self.create_relationship(tx, parent_id, node_id)

        for child in node.children:
            self._store_node_recursive(session, child, node_id)
