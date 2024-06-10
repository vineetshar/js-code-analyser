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

    def get_children_text(self, identifier_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_children_texts, identifier_name)
            return [record["parent_text"] for record in result]

    def list_identifiers(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._list_identifiers)
            return [record["identifier"] for record in result]

    @staticmethod
    def _find_children_texts(tx, identifier_name):
        query = (
            "MATCH (n:ASTNode {text: $identifier_name})<-[:HAS_CHILD]-(parent:ASTNode) "
            "RETURN parent.text AS parent_text"
        )
        result = tx.run(query, identifier_name=identifier_name)
        return [record for record in result]

    @staticmethod
    def _list_identifiers(tx):
        query = (
            "MATCH (n:ASTNode {type: 'identifier'}) "
            "RETURN n.text AS identifier"
        )
        result = tx.run(query)
        return [record for record in result]
