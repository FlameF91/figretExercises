import os
import numpy as np
import pandas as pd

# 定义我们要搜集的拓扑和算法
TOPOLOGIES = ["Facebook_pod_a", "Facebook_pod_b", "GEANT"]
# 这里的 Key 是文件夹名字，Value 是我们想在图表中显示的算法名
METHODS = {
    "Figret": "FIGRET (Ours)",
    "Jupiter": "Jupiter",
    "Pred": "Pred TE",  # 注意：如果文件夹叫 Predict，请这里改成 "Predict": "Pred TE"
    "Oblivious": "Oblivious",
    "COPE": "COPE"
}


def get_average_mlu(topo, folder_name):
    """读取 result.txt 并计算平均值"""
    # 尝试匹配 result.txt 位置
    path = os.path.join("Result", topo, folder_name, "result.txt")

    # 容错处理：有时 Pred TE 的文件夹可能叫 Predict
    if folder_name == "Pred" and not os.path.exists(path):
        path = os.path.join("Result", topo, "Predict", "result.txt")

    if not os.path.exists(path):
        return None

    try:
        with open(path, 'r') as f:
            # 读取非空行，转为 float
            data = [float(line.strip()) for line in f if line.strip()]
        if len(data) == 0: return None
        return np.mean(data)
    except:
        return None


def main():
    print("=" * 60)
    print("正在自动扫描 Result 文件夹...")
    print("=" * 60)

    results = {}

    for topo in TOPOLOGIES:
        results[topo] = {}
        print(f"\n处理拓扑: {topo}")
        for folder, display_name in METHODS.items():
            score = get_average_mlu(topo, folder)
            if score is not None:
                results[topo][display_name] = score
                print(f"  ✅ {display_name:<15}: {score:.4f}")
            else:
                results[topo][display_name] = 0.0
                print(f"  ❌ {display_name:<15}: 未找到结果文件 (Result/{topo}/{folder}/result.txt)")

    # 打印最终字典，方便直接复制到画图脚本
    print("\n" + "=" * 60)
    print("【数据采集完成】请复制以下字典到绘图脚本中：")
    print("=" * 60)
    print(results)


if __name__ == "__main__":
    main()