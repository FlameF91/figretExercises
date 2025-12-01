import time
import torch
import numpy as np
import sys
from figret_helper import parse_args
from src.figret_env import FigretEnv
from src.figret_net import FigretNetWork
from src.config import MODEL_DIR

# 强制使用 CPU
device = torch.device("cpu")


def measure_speed(topo_name):
    print(f"正在测试拓扑: {topo_name} ...")

    # 1. 模拟参数
    # 我们不需要加载真实数据，只需要初始化网络结构
    sys.argv = ['figret.py', '--topo_name', topo_name, '--batch_size', '1']
    props = parse_args(sys.argv[1:])

    # 2. 初始化环境和模型结构
    env = FigretEnv(props)
    # 输入维度: 历史长度 * 节点数 * (节点数-1)
    input_dim = props.hist_len * env.num_nodes * (env.num_nodes - 1)
    output_dim = env.num_paths

    model = FigretNetWork(input_dim, output_dim, props.num_layer).double().to(device)
    model.eval()  # 切换到评估模式

    # 3. 生成随机输入数据 (模拟一个流量矩阵)
    # Batch size = 1
    dummy_input = torch.rand(1, input_dim).double().to(device)

    # 4. 预热 (Warm up) - 让 CPU 缓存加载
    for _ in range(10):
        with torch.no_grad():
            _ = model(dummy_input)

    # 5. 正式测速 (运行 1000 次取平均)
    loops = 1000
    start_time = time.time()

    with torch.no_grad():
        for _ in range(loops):
            _ = model(dummy_input)

    end_time = time.time()

    avg_time_ms = ((end_time - start_time) / loops) * 1000
    print(f"✅ [FIGRET] {topo_name} 平均推理耗时: {avg_time_ms:.4f} ms")
    return avg_time_ms


if __name__ == "__main__":
    print("=" * 50)
    print(f"FIGRET 推理速度测试 (Device: {device})")
    print("=" * 50)

    # 测试 GEANT 和 Meta PoD
    t1 = measure_speed("GEANT")
    t2 = measure_speed("Facebook_pod_a")
    # 如果有 Facebook_pod_b 也可以测，结构一样的，速度也一样

    print("\n" + "=" * 50)