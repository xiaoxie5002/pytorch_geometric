import torch
import torch_unique

from ..dataset import Data
from ...utils.undirected import to_undirected


def read_off(filename):
    with open(filename, 'r') as f:
        data = f.read().split()

    if data[0] == 'OFF':
        data.pop(0)
    else:
        # Some files contain a bug and don't have a carriage return after OFF.
        data[0] = data[0][3:]

    num_nodes = int(data[0])

    pos = [float(x) for x in data[3:num_nodes * 3 + 3]]
    pos = torch.FloatTensor(pos).view(-1, 3)

    face = [int(x) for x in data[num_nodes * 3 + 3:]]
    face = torch.LongTensor(face).view(-1, 4)[:, 1:].contiguous().t()

    index = torch.cat([face[:2], face[1:], face[::2]], dim=1)
    index = to_undirected(index, num_nodes=pos.size(0))

    # Delete isolated vertices.
    unique = torch_unique.unique(index[0])
    pos = pos[unique]
    perm = []
    j = 0
    for i in range(num_nodes):
        if j < unique.size()[0] and i == unique[j]:
            perm.append(j)
            j += 1
        else:
            perm.append(-1)
    perm = torch.LongTensor(perm)
    index = torch.stack([perm[index[0]], perm[index[1]]], dim=0)

    # Create input features.
    input = torch.ones(pos.size(0))

    return Data(input, pos, index, None, None)
