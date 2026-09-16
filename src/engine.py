from .schema import Node, WorkflowState
import src.database.sqlite as db

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

    def run(self,state: WorkflowState, start_node: str = None, max_steps: int = 25):
        current_node = self.entry_point

        if(start_node is not None):
            current_node = start_node
        steps = 0
        while(current_node is not None):
            steps += 1
            if(steps > max_steps):
                raise RuntimeError("Max steps exceeded, possible infinite loop detected")
            node = self.nodes[current_node]
            state = node.operation(state)

            state.history.append(current_node)
            state_json = state.model_dump_json()#inbuilt method provided by pydantic to convert data into valid json
            db.save_checkpoint(state.run_id,current_node,state_json)
            node_edges = self.edges.get(node.name,{}) # using get method so that if the key is absent then it will not throw an error
            if(state.status in node_edges):
                current_node = node_edges[state.status]
            else:
                current_node = None

        return state

    def resume(self, run_id: str):
        res = db.load_checkpoint(run_id)
        
        if(res is None):
            raise ValueError("No checkpoint found")
        
        last_node, raw_state = res
        state = WorkflowState.model_validate_json(raw_state)

        status = state.status
        node_edges = self.edges.get(last_node,{})
        next_node = None
        if(state.status in node_edges):
            next_node = node_edges[status]
        
        return self.run(state, start_node = next_node)