class Data(object):
    def __init__(self,
                 x=None,
                 edge_index=None,
                 edge_attr=None,
                 y=None,
                 pos=None):
        self.x = x
        self.edge_index = edge_index
        self.edge_attr = edge_attr
        self.y = y
        self.pos = pos

    @staticmethod
    def from_dict(dictionary):
        data = Data()
        for key, item in dictionary.items():
            data[key] = item
        return data

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, item):
        setattr(self, key, item)

    def keys(self):
        return [key for key in self.__dict__.keys() if self[key] is not None]

    def __len__(self):
        return len(self.keys())

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        for key in self.keys():
            yield key, self[key]

    def __call__(self, *keys):
        for key in self.keys() if not keys else keys:
            if self[key] is not None:
                yield key, self[key]

    @property
    def num_nodes(self):
        for _, item in self('x', 'pos'):
            return item.size(0)
        if self.edge_index is not None:
            return self.edge_index.max().item() + 1
        return None

    def apply(self, func, *keys):
        for key, item in self(*keys):
            setattr(self, key, func(item))
        return self

    def contiguous(self, *keys):
        return self.apply(lambda x: x.contiguous(), *keys)

    def to(self, device, *keys):
        return self.apply(lambda x: x.to(device), *keys)

    def __repr__(self):
        info = ['{}={}'.format(key, list(item.size())) for key, item in self]
        return 'Data({})'.format(', '.join(info))