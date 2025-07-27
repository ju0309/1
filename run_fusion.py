import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- Step 0: 加载数据 ---
# 请确保您的CSV数据文件名是 'pa.csv'，并与此脚本放在同一个文件夹下
file_name = 'pa.csv'

try:
    data = pd.read_csv(file_name)
    print(f"文件 '{file_name}' 加载成功！开始进行数据融合分析...")
    
    # 动态获取列名
    area_col = data.columns[0]
    perimeter_col = data.columns[1]

    # --- Step 1: 定义计算所需的参数 (源自您论文3.3节) ---
    
    # 稳定周长基准模型: P_stable = a * A^b
    a = 4.29438
    b = 0.48324

    # 面积目标设定值 (A_sp): 基于前100个数据点的平均值
    A_sp = data[area_col].iloc[:100].mean()

    # 自适应权重函数 w_S 的参数
    w_S_max = 0.5 # 论文中已定义
    
    # 以下两个参数论文未提供，采用合理的工程假设值
    I_S_crit = 0.05  # 不稳定性激活阈值
    lambda_val = 100 # 权重切换灵敏度

    # --- Step 2: 执行加权融合计算 ---

    # 计算归一化面积偏差 (E_A)
    data['E_A'] = (data[area_col] - A_sp) / A_sp

    # 计算理论稳定周长 (P_stable)
    data['P_stable'] = a * (data[area_col] ** b)

    # 计算稳定性偏离指数 (I_S)
    data['I_S'] = (data[perimeter_col] - data['P_stable']) / data['P_stable']

    # 定义Sigmoid函数用于计算权重
    def calculate_wS(IS, w_max, lamb, IS_crit):
        return w_max / (1 + np.exp(-lamb * (IS - IS_crit)))

    # 计算稳定性权重 (w_S) 和 面积权重 (w_A)
    data['w_S'] = calculate_wS(data['I_S'], w_S_max, lambda_val, I_S_crit)
    data['w_A'] = 1 - data['w_S']

    # 计算最终的融合后综合误差 (E_total)
    data['E_total'] = data['w_A'] * data['E_A'] + data['w_S'] * data['I_S']


    # --- Step 3: 生成并显示可视化图表 ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 8))

    # 设置一个常用的中文字体
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei'] 
        plt.rcParams['axes.unicode_minus'] = False 
    except Exception as e:
        print(f"设置中文字体失败，将使用默认字体。错误: {e}")

    # 绘制三条曲线
    ax.plot(data.index, data['E_total'], label='融合后综合误差 (E_total)', color='red', linewidth=2.5, zorder=10)
    ax.plot(data.index, data['E_A'], label='归一化面积偏差 (E_A)', color='blue', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.plot(data.index, data['I_S'], label='稳定性偏离指数 (I_S)', color='green', linestyle=':', linewidth=1.5, alpha=0.8)

    # 美化图表
    ax.set_title('熔池面积与周长自适应加权融合结果', fontsize=18, fontweight='bold')
    ax.set_xlabel('数据点 (帧)', fontsize=14)
    ax.set_ylabel('误差 / 偏离指数', fontsize=14)
    ax.legend(fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.axhline(0, color='black', linewidth=0.75, linestyle='-')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # 显示图表
    plt.show()

    # 打印出计算中使用的参数，供您参考
    print("\n计算中使用的参数小结：")
    print("="*30)
    print(f"稳定周长基准模型: P_stable = {a} * A^{b}")
    print(f"面积目标设定值 (A_sp): {A_sp:.2f} (基于数据前100点的平均值)")
    print("\n自适应权重函数参数:")
    print(f"最大稳定性权重 (w_S,max): {w_S_max}")
    print(f"不稳定性激活阈值 (I_S,crit): {I_S_crit} (假设值)")
    print(f"权重切换灵敏度 (λ): {lambda_val} (假设值)")

except FileNotFoundError:
    print(f"错误：无法找到文件 '{file_name}'。请确保您的CSV文件与此Python脚本放在同一个文件夹下。")
except Exception as e:
    print(f"处理数据时发生错误: {e}")