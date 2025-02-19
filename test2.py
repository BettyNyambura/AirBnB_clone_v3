from models import storage
from models.state import State

# Test count()
print("Total objects:", storage.count())
print("State objects:", storage.count(State))

# Test get()
state_id = "1234"  # Use the actual ID from your output
state = storage.get(State, state_id)
print("Retrieved state:", state)
