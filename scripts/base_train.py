import torch
import torch.nn as nn

class GPT(nn.Module):
    def __init__(self, config):
        super.__init__()
        self.config = config