class NoStagnation:
    def __init__(self, config=None, reporters=None):
        pass
    
    @classmethod
    def parse_config(cls, param_dict):
        return NoStagnation()
    
    def update(self, spieces_set, generation):
        return [(s.key, s, False) for s in spieces_set.species.values()]
