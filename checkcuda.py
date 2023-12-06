import os
import torch
from NGRFunctions import *
from torch import nn
from torch.utils.data import DataLoader
# from torchvision import datasets, transforms


device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
logger.info(f"Is torch using CUDNN? torch.backends.cudnn.enabled")
logger.info(f"Using {device} device")
logger.info(torch.__version__)
