import numpy as np
import pandas as pd

def generate_noise_data(base_value=320, noise_level=0.09, num_samples=800, filename="noise_data.csv"):
    """
    生成带噪声的数据并保存到CSV文件
    
    参数:
    - base_value: 基准值，数据在此值周围波动
    - noise_level: 噪声强度 (如0.1表示10%的噪声)
    - num_samples: 生成数据的数量
    - filename: 保存的CSV文件名
    """
    
    # 生成噪声
    noise = np.random.normal(0, base_value * noise_level, num_samples)
    
    # 生成最终数据
    data_values = base_value + noise
    
    # 创建DataFrame
    df = pd.DataFrame({
        'value': data_values
    })
    
    # 保存到CSV文件
    df.to_csv(filename, index=False)
    print(f"已生成 {num_samples} 个数据点，保存到 {filename}")

# 使用示例
if __name__ == "__main__":
    # 示例1: 基本使用
    generate_noise_data(base_value=320, noise_level=0.015, num_samples=900, filename="data1.csv")
    
    # # 示例2: 更多数据点
    # generate_noise_data(base_value=100, noise_level=0.1, num_samples=2000, filename="data2.csv")
    
    # # 示例3: 自定义参数
    # generate_noise_data(base_value=200, noise_level=0.15, num_samples=1000, filename="data3.csv")