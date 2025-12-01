import matplotlib.pyplot as plt
import numpy as np

# ==========================================================
# 🔴 请填入最后两个缺失的数字
# ==========================================================
# 1. FIGRET 数据 (单位: ms)
figret_pod = 0.1328  # ✅ 已知 (您刚才跑出来的)
figret_geant = 0.2175  # <--- ❓ 请填入 speed_test_figret.py 对 GEANT 的结果

# 2. Jupiter (Gurobi) 数据 (单位: ms) -> 公式: 1000 / (it/s)
# GEANT: 1000 / 25.97 = 38.51 ms
jupiter_geant = 38.51  # ✅ 已知
# PoD: 假设它是 800 it/s (仅为示例)，请填入真实计算值
jupiter_pod = 38.5  # <--- ❓ 请修改为: 1000 / (您跑出来的 PoD it/s)


# ==========================================================

def plot_speed_comparison():
    labels = ['Meta PoD (DC)', 'GEANT (WAN)']

    # 也就是对应 [PoD, GEANT] 的顺序
    figret_times = [figret_pod, figret_geant]
    jupiter_times = [jupiter_pod, jupiter_geant]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 6))

    # 绘制柱状图
    rects1 = ax.bar(x - width / 2, figret_times, width, label='FIGRET (CPU)', color='#28a745', alpha=0.9,
                    edgecolor='black')
    rects2 = ax.bar(x + width / 2, jupiter_times, width, label='Jupiter (Gurobi)', color='#ffc107', alpha=0.9,
                    edgecolor='black')

    # 在柱子上标数值
    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.3f} ms',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=10)

    # 计算加速比
    speedup_pod = jupiter_pod / figret_pod
    speedup_geant = jupiter_geant / figret_geant

    # 在图上标注加速倍数 (用红色箭头或文字)
    # 因为是对数坐标，位置需要稍微调整
    def annotate_speedup(idx, j_time, speedup):
        ax.text(idx, j_time * 1.3, f"Speedup: {speedup:.1f}x",
                ha='center', color='#d9534f', fontweight='bold', fontsize=12,
                bbox=dict(facecolor='white', edgecolor='#d9534f', boxstyle='round,pad=0.3'))

    annotate_speedup(0, jupiter_pod, speedup_pod)
    annotate_speedup(1, jupiter_geant, speedup_geant)

    ax.set_ylabel('Solver Time per Matrix (ms) - Log Scale', fontsize=12)
    ax.set_title('Computation Speed: FIGRET vs Traditional TE (Table 2 Reproduction)', fontsize=14, fontweight='bold',
                 pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12)
    ax.legend(fontsize=11)

    # 关键：使用对数坐标，否则0.1ms和40ms在同一张图上看不清
    ax.set_yscale('log')
    # 设置Y轴范围，下限设小一点以便显示0.1ms
    ax.set_ylim(0.05, max(jupiter_times) * 10)

    plt.grid(axis='y', linestyle='--', alpha=0.3, which='major')

    plt.tight_layout()
    plt.savefig('Final_Speed_Comparison.png', dpi=300)
    print(f"\n🎉 速度对比图已生成！")
    print(f"Meta PoD 加速比: {speedup_pod:.1f} 倍")
    print(f"GEANT 加速比:    {speedup_geant:.1f} 倍")
    plt.show()


if __name__ == "__main__":
    plot_speed_comparison()