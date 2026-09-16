import uuid
from src.schema import WorkflowState, Node
from src.engine import Graph
from src.database.sqlite import init_db

# 1. Initialize the SQLite database table
init_db()

# 2. Define our Node Operations
def node_one_operation(state: WorkflowState) -> WorkflowState:
    print("-> Executing Node 1: Initialization")
    state.data["counter"] = state.data.get("counter", 0) + 1
    state.status = "success"
    return state

# Add this flag above the function
has_crashed = False

def node_two_operation(state: WorkflowState) -> WorkflowState:
    global has_crashed
    print("-> Executing Node 2: Processing")
    state.data["counter"] = state.data.get("counter", 0) + 1
    state.status = "success"
    
    # Only crash if we haven't crashed yet
    if not has_crashed:
        has_crashed = True
        print("   [!] Simulating sudden power loss before checkpoint can save!")
        raise Exception("💥 SERVER CRASH! Power lost abruptly.")
        
    print("   [*] Power restored! Node 2 completing successfully.")
    return state
def node_three_operation(state: WorkflowState) -> WorkflowState:
    print("-> Executing Node 3: Finalizing Workflow")
    state.data["counter"] = state.data.get("counter", 0) + 1
    state.status = "success"
    return state

# 3. Build the Graph
workflow = Graph()

# Add nodes
workflow.add_node(Node(name="node_one", operation=node_one_operation))
workflow.add_node(Node(name="node_two", operation=node_two_operation))
workflow.add_node(Node(name="node_three", operation=node_three_operation))

# Set entry point and edges
workflow.set_entry_point("node_one")
workflow.add_edge("node_one", "node_two", condition="success")
workflow.add_edge("node_two", "node_three", condition="success")

# 4. Run the simulation
run_id = str(uuid.uuid4())
initial_state = WorkflowState(run_id=run_id, data={"counter": 0})

print(f"=== Starting Workflow Run: {run_id} ===")
try:
    workflow.run(initial_state)
except Exception as e:
    print(f"\nCaught expected exception: {e}\n")

print("=== Simulating Server Reboot & Recovery ===")
# Now, let's call resume() using the exact same run_id!
recovered_result = workflow.resume(run_id)

print(f"\n=== Workflow Successfully Completed After Recovery! ===")
print(f"Final State History: {recovered_result.history}")
print(f"Final Data Counter: {recovered_result.data}")