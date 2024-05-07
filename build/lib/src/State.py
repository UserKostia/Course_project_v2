class GlobalState:
    def __init__(self):
        self._state = dict()

    def register_state(self, state):
        self._state[state.get_key()] = state

    def get_state(self):
        return self._state

    def set_state_by_key(self, key: str, value):
        self._state[key] = value

    def get_state_by_key(self, key: str):
        return self._state.get(key)
    
    def update_state_by_key(self, key: str, value):
        self._state[key] = value

    def delete_state_by_key(self, key: str):
        if key in self._state:
            del self._state[key]


global_state = GlobalState()
