from schema import Node, WorkflowState

class Graph:
    def __init__(self):
        self.nodes: dict[str,Node] = {}
        self.edges: dict[str,dict[str,Node]] = {}
        self.entry_point: str | None = None

    def add_node(self, node: Node):
        self.nodes[node.name] = node

    def set_entry_point(self,node_name: str):
        self.entry_point = node_name

    def add_edge(self,source_name: str, end: Node,condition: str):
        if(source_name not in self.edges):
            self.edges[source_name] = {}

        self.edges[source_name][condition] = end

    def run(self,state: WorkflowState):
        current_node = self.entry_point

        while(current_node is not None):
            node = self.nodes[current_node]
            state = node.operation(state)

            state.history.append(current_node)
            node_edges = self.edges.get(node.name,{}) # using get method so that if the key is absent then it will not throw an error
            if(state.status in node_edges):
                current_node = node_edges[state.status]
            else:
                current_node = None

        return state
