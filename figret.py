import sys
from torch import nn
import torch
import numpy as np
from torch.utils.data import DataLoader
import random

from figret_helper import parse_args
from src.figret_env import FigretEnv
from src.figret_net import FigretNetWork
from src.figret_model import Figret, FigretDataset
from src.config import MODEL_DIR


def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    # 为了确保彻底避开显卡问题，这里也暂时注释掉 CUDA 相关的随机种子设置
    # if torch.cuda.is_available():
    #     torch.cuda.manual_seed(seed)
    #     torch.cuda.manual_seed_all(seed)
    # torch.backends.cudnn.benchmark = False
    # torch.backends.cudnn.deterministic = True


set_seed(521000)


def benchmark(props):
    # [修改点]: 强制使用 CPU，避开 RTX 5070 Ti 的兼容性报错
    # 原代码: device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    print(f"正在使用设备: {device} (已强制切换为 CPU 模式)")

    env = FigretEnv(props)
    figret = Figret(props, env, device)

    if props.mode == 'train':
        train_dataset = FigretDataset(props, env, 'train')
        # 注意: 如果在 Windows 上遇到 BrokenPipeError，可以将 num_workers 设置为 0
        train_dl = DataLoader(train_dataset, batch_size=props.batch_size, shuffle=True)
        model = FigretNetWork(props.hist_len * env.num_nodes * (env.num_nodes - 1), env.num_paths,
                              props.num_layer).double()
        optimizer = torch.optim.Adam(model.parameters())
        figret.train(train_dl, model, optimizer, device)
    elif props.mode == 'test':
        test_dataset = FigretDataset(props, env, 'test')
        test_dl = DataLoader(test_dataset, batch_size=1, shuffle=False)
        # 加载模型时添加 map_location=device 以防止尝试加载到 GPU
        model_path = f'{MODEL_DIR}/{props.topo_name}_{props.opt_name}.pt' if props.opt_name \
            else f'{MODEL_DIR}/{props.topo_name}.pt'

        # 确保加载模型时也映射到 CPU
        model = torch.load(model_path, map_location=device, weights_only=False)
        figret.test(test_dl, model, device)

    return


if __name__ == '__main__':
    props = parse_args(sys.argv[1:])
    benchmark(props)