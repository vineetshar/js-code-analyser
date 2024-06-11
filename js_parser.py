from tree_sitter import Language, Parser
import tree_sitter_javascript as JavaScript

class ASTNode:
    def __init__(self, node_type, text=''):
        self.node_type = node_type
        self.text = text
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"ASTNode(type={self.node_type}, text={self.text}, children={len(self.children)})"

async def build_ast(node):
    node_type = node.type
    text = node.text.decode('utf-8') if node.text else ""
    ast_node = ASTNode(node_type, text)

    for child in node.children:
        if child.type in {'function', 'program','class_declaration'}:
            child_node = await build_ast(child)
            ast_node.add_child(child_node)
        else:
            text = child.text.decode('utf-8') if child.text else ""
            child_node = ASTNode(child.type, text)
            ast_node.add_child(child_node)

    return ast_node

def parse_code(code):
    JS_LANGUAGE = Language(JavaScript.language())
    parser = Parser()
    parser.set_language(JS_LANGUAGE)
    tree = parser.parse(bytes(code, 'utf8'))

    return tree
