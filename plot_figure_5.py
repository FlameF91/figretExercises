import matplotlib.pyplot as plt
import numpy as np

# =================================================================
# 🔴 请将 collect_scores.py 输出的字典粘贴在下面
# =================================================================
DATA = {
    'Facebook_pod_a':{'FIGRET (Ours)': 1.124492204491678, 'Jupiter': 1.2256165405531187, 'Pred TE': 1.212954662149011, 'Oblivious': 1.3861413165575924, 'COPE': 1.2518563764261852},
    'Facebook_pod_b':{'FIGRET (Ours)': 1.0779133930658904, 'Jupiter': 1.470552859937153, 'Pred TE': 1.293712422322798, 'Oblivious': 1.8977997222155063, 'COPE': 1.4817284508960844},
    'GEANT':{'FIGRET (Ours)': 1.0053174914437932, 'Jupiter': 1.0788517296835018, 'Pred TE': 1.9233202189479432, 'Oblivious': 2.2636702693920703, 'COPE': 1.4308251086377513}
}



# =================================================================

def plot_reproduction():
    # 准备数据
    topologies = list(DATA.keys())
    # 提取所有出现的算法名
    schemes = list(DATA[topologies[0]].keys())

    # 映射显示的拓扑名称 (论文中的叫法)
    topo_labels = ["Meta PoD A (DB)", "Meta PoD B (Web)", "GEANT (WAN)"]

    x = np.arange(len(topologies))
    width = 0.15

    fig, ax = plt.subplots(figsize=(14, 7))

    # 颜色盘 (参考论文风格)
    colors = ['#28a745', '#ffc107', '#17a2b8', '#6c757d', '#343a40']

    for i, scheme in enumerate(schemes):
        vals = [DATA[topo].get(scheme, 0) for topo in topologies]
        rects = ax.bar(x + (i - 2) * width, vals, width, label=scheme, color=colors[i], edgecolor='black')

        # 标数值
        for rect in rects:
            height = rect.get_height()
            if height > 0.01:
                ax.annotate(f'{height:.2f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points",
                            ha='center', va='bottom', fontsize=8, rotation=0)

    # 图表装饰
    ax.set_ylabel('Normalized MLU (Lower is Better)', fontsize=12)
    ax.set_title('Reproduction of Figure 5: FIGRET vs Baselines', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(topo_labels, fontsize=12)
    ax.legend(ncol=5, loc='upper center', bbox_to_anchor=(0.5, -0.08), fontsize=10)

    # 获取最大值以设置Y轴上限
    all_vals = [v for sub in DATA.values() for v in sub.values()]
    ax.set_ylim(0.8, max(all_vals) * 1.1)

    # 画最优线
    plt.axhline(y=1.0, color='r', linestyle='--', linewidth=1.5, label='Optimal')

    plt.tight_layout()
    plt.savefig('Final_Reproduction_Fig5.png', dpi=300)
    print("✅ 图表生成完毕: Final_Reproduction_Fig5.png")
    plt.show()


if __name__ == "__main__":
    plot_reproduction()