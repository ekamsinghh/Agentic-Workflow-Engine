import sqlite3 as sq

def init_db(db_path: str = "checkpoints.sqlite"):
    connection = sq.connect(db_path) # connection object to the disk based local database

    cur = connection.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS checkpoints (run_id TEXT PRIMARY KEY,current_node TEXT,state_data TEXT)"
    )
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='checkpoints'")
    if(res.fetchone() is None):
        print("Error in creating table⚠️")
        
    connection.commit()
    connection.close()

def save_checkpoint(run_id: str, current_node: str, state_json: str, db_path: str = "checkpoints.sqlite"):

    connection = sq.connect(db_path)
    cur = connection.cursor()

    cur.execute(
        "INSERT OR REPLACE INTO checkpoints (run_id, current_node, state_data)VALUES (?, ?, ?)",(run_id,current_node,state_json)
    )
    connection.commit() # to commit the current transaction
    connection.close()

def load_checkpoint(run_id: str,db_path: str = "checkpoints.sqlite") -> (tuple[str,str] | None): # tuple[str,str] ,means the function will return tuple of size 2 with 2 string entries
    connection = sq.connect(db_path)
    cur = connection.cursor()

    res = cur.execute(
        "SELECT current_node,state_data FROM checkpoints where run_id = ?",(run_id,)
    )

    loaded_data = res.fetchone() # None if no saved checkpoints
    connection.close()
    return loaded_data