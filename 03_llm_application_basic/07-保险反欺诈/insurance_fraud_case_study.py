"""
保险反欺诈案例研究
==================

本脚本演示了如何使用机器学习和大模型技术来识别潜在的保险欺诈行为。
主要包含以下步骤：
1. 数据加载和探索性数据分析
2. 数据预处理和特征工程
3. 多种机器学习模型训练和评估
4. 模型性能对比和结果分析
5. 大模型在保险反欺诈中的应用示例

作者: AI助手
日期: 2024
版本: 1.0
"""

# =============================================================================
# 环境依赖和库导入
# =============================================================================
# 请确保已安装以下依赖包：
# pip install pandas scikit-learn matplotlib seaborn python-dotenv dashscope

# 标准库导入
import os
import json
import warnings
from pathlib import Path

# 第三方库导入
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 机器学习相关库
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, 
    roc_auc_score, precision_recall_curve, roc_curve,
    precision_score, recall_score, f1_score
)

# 大模型API相关库
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

# 忽略警告信息，保持输出整洁
warnings.filterwarnings('ignore')

# =============================================================================
# 环境配置和API密钥设置
# =============================================================================
# 加载环境变量文件（包含API密钥）
env_file = Path('../.env')
load_dotenv(env_file)

# 获取大模型API密钥并配置
api_key = os.environ.get('DASHSCOPE_API_KEY')
if api_key:
    dashscope.api_key = api_key
    print("✅ API密钥配置成功")
else:
    print("⚠️ 警告: 未找到DASHSCOPE_API_KEY，大模型功能将不可用")

# =============================================================================
# 1. 数据加载和探索性数据分析
# =============================================================================
print("=" * 60)
print("📊 开始数据加载和探索性数据分析")
print("=" * 60)

# 加载训练数据集
print("\n🔍 加载训练数据集...")
train_df = pd.read_csv('train.csv')

# 显示数据基本信息
print("\n📋 训练集基本信息:")
print(f"   📈 数据规模: {len(train_df)} 行 × {len(train_df.columns)} 列")
print(f"   🎯 目标变量分布:")
print(f"      - 欺诈案例: {train_df['fraud_reported'].sum()} 个 ({train_df['fraud_reported'].mean():.2%})")
print(f"      - 正常案例: {len(train_df) - train_df['fraud_reported'].sum()} 个 ({(1 - train_df['fraud_reported'].mean()):.2%})")

# 显示数据前5行
print("\n📄 训练集前5行数据:")
print(train_df.head())

# 检查数据质量 - 缺失值分析
print("\n🔍 数据质量检查 - 缺失值统计:")
missing_stats = train_df.isnull().sum().sort_values(ascending=False)
print(missing_stats.head(10))  # 显示前10个缺失值最多的列

def analyze_fields_with_llm(df, api_key):
    """
    使用大模型分析保险数据集中各字段的含义及其在欺诈检测中的重要性
    
    参数:
        df (DataFrame): 包含保险数据的DataFrame
        api_key (str): 大模型API密钥
    
    返回:
        dict: 包含字段分析结果的字典
    """
    # 准备数据集样本用于分析
    columns = train_df.head()
    
    # 构建分析提示词
    prompt = f"""
    作为一名保险欺诈检测专家，请分析以下保险数据集中各字段的含义及其在欺诈检测中的重要性。
    
    数据集前五行内容：
    columns = {columns}
    
    对于每个字段，请提供以下信息：
    1. 字段含义：该字段在保险业务中代表什么
    2. 欺诈相关性：该字段与欺诈检测的相关程度（高/中/低）
    3. 分析理由：为什么该字段对欺诈检测重要或不重要
    4. 异常模式：该字段中哪些值或模式可能暗示欺诈行为
    
    请以JSON格式返回分析结果，不要包含任何额外文本，按以下模板响应：
    {{"字段名": {{"含义": "<字段含义>", "欺诈相关性": "高/中/低", "分析理由": "<分析理由>", "异常模式": "<异常模式>"}}}}
    """
    
    # 调用大模型API进行分析
    try:
        response = Generation.call(
            model="qwen-max",  # 使用通义千问大模型
            prompt=prompt,
            result_format='message',
            temperature=0.1,   # 低温度以获得更确定性的回答
            max_tokens=4000    # 确保有足够的token来分析所有字段
        )
        
        # 处理API响应
        if response.status_code == 200:
            try:
                content = response.output.choices[0].message.content
                # 提取JSON内容
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    result = json.loads(json_str)
                    return result
                else:
                    return {"error": "无法从响应中提取JSON格式内容"}
            except json.JSONDecodeError as e:
                return {"error": f"JSON解析错误: {str(e)}"}
            except Exception as e:
                return {"error": f"响应处理错误: {str(e)}"}
        else:
            return {"error": f"API调用失败，状态码: {response.status_code}"}
    except Exception as e:
        return {"error": f"API调用异常: {str(e)}"}

def display_field_analysis(analysis_result):
    """
    以易读的格式显示大模型分析的字段结果
    
    参数:
        analysis_result (dict): 大模型返回的字段分析结果
    """
    # 检查是否有错误
    if "error" in analysis_result:
        print(f"❌ 分析错误: {analysis_result['error']}")
        return
    
    print("\n" + "=" * 60)
    print("🤖 大模型字段分析结果")
    print("=" * 60)
    
    # 定义相关性评分函数，用于排序
    def relevance_score(field_info):
        """根据欺诈相关性计算评分（高=3, 中=2, 低=1）"""
        relevance = field_info.get("欺诈相关性", "低")
        if relevance == "高":
            return 3
        elif relevance == "中":
            return 2
        else:
            return 1
    
    # 按欺诈相关性排序（高->中->低）
    sorted_fields = sorted(analysis_result.items(), 
                          key=lambda x: relevance_score(x[1]), 
                          reverse=True)
    
    # 显示分析结果
    for field_name, field_info in sorted_fields:
        print(f"\n📊 字段名: {field_name}")
        print(f"   📝 含义: {field_info.get('含义', '未提供')}")
        print(f"   🎯 欺诈相关性: {field_info.get('欺诈相关性', '未知')}")
        print(f"   💡 分析理由: {field_info.get('分析理由', '未提供')}")
        print(f"   ⚠️  异常模式: {field_info.get('异常模式', '未提供')}")
        print("-" * 60)

# 使用大模型分析数据集字段含义
print("\n🤖 正在使用大模型分析数据集字段含义...")
if api_key:
    analysis_result = analyze_fields_with_llm(train_df, api_key)
    display_field_analysis(analysis_result)
else:
    print("⚠️ 跳过大模型分析（API密钥未配置）")

# 加载测试数据集
print("\n🔍 加载测试数据集...")
test_df = pd.read_csv('test.csv')

# 显示测试集基本信息
print("\n📋 测试集基本信息:")
print(f"   📈 数据规模: {len(test_df)} 行 × {len(test_df.columns)} 列")

# 显示测试集前5行
print("\n📄 测试集前5行数据:")
print(test_df.head())

# 检查测试集数据质量
print("\n🔍 测试集数据质量检查 - 缺失值统计:")
test_missing_stats = test_df.isnull().sum().sort_values(ascending=False)
print(test_missing_stats.head(10))

# 比较训练集和测试集的列差异
print("\n🔍 数据集结构比较:")
train_cols = set(train_df.columns)
test_cols = set(test_df.columns)
print(f"   📊 训练集独有列: {train_cols - test_cols}")
print(f"   📊 测试集独有列: {test_cols - train_cols}")
print(f"   📊 共同列数: {len(train_cols & test_cols)}")

# =============================================================================
# 2. 数据预处理和特征工程
# =============================================================================
print("\n" + "=" * 60)
print("🔧 开始数据预处理和特征工程")
print("=" * 60)

# 记录原始数据形状
print(f"\n📊 原始数据形状:")
print(f"   🏋️ 训练集: {train_df.shape[0]} 行 × {train_df.shape[1]} 列")
print(f"   🏋️ 测试集: {test_df.shape[0]} 行 × {test_df.shape[1]} 列")

# 步骤1: 缺失值处理
print("\n🔧 步骤1: 缺失值处理")
missing_cols = train_df.columns[train_df.isnull().any()].tolist()
print(f"   📍 包含缺失值的列: {missing_cols}")

# 对缺失值进行填充
train_df['authorities_contacted'] = train_df['authorities_contacted'].fillna('Unknown')
test_df['authorities_contacted'] = test_df['authorities_contacted'].fillna('Unknown')

# 删除无用的列（如_c39列，通常包含无意义的标识符）
if '_c39' in train_df.columns:
    train_df = train_df.drop('_c39', axis=1)
    print("   🗑️ 删除训练集中的_c39列")
if '_c39' in test_df.columns:
    test_df = test_df.drop('_c39', axis=1)
    print("   🗑️ 删除测试集中的_c39列")

print("✅ 缺失值处理完成")

# 步骤2: 特征编码 - 将分类变量转换为数值
print("\n🔧 步骤2: 特征编码")
print("   将分类变量转换为数值，以便机器学习算法处理")

# 定义需要编码的分类列
categorical_cols = [
    'incident_type', 'collision_type', 'incident_severity', 
    'authorities_contacted', 'incident_state', 'incident_city',
    'property_damage', 'police_report_available', 'policy_state',
    'insured_sex', 'insured_education_level', 'insured_occupation',
    'insured_hobbies', 'insured_relationship', 'auto_make', 'auto_model'
]

# 存储编码器以便后续使用
label_encoders = {}

# 使用LabelEncoder对分类特征进行编码
for col in categorical_cols:
    if col in train_df.columns:
        le = LabelEncoder()
        # 合并训练集和测试集的唯一值来训练编码器，确保一致性
        combined_values = pd.concat([train_df[col], test_df[col]]).astype(str).unique()
        le.fit(combined_values)
        
        # 应用编码
        train_df[col] = le.transform(train_df[col].astype(str))
        test_df[col] = le.transform(test_df[col].astype(str))
        
        # 保存编码器
        label_encoders[col] = le
        print(f"   ✅ {col}: {len(le.classes_)} 个类别")
    else:
        print(f"   ⚠️ {col}: 列不存在，跳过编码")

print("✅ 分类特征编码完成")

def create_features(df):
    """
    创建新的特征以增强模型的预测能力
    
    参数:
        df (DataFrame): 原始数据框
    
    返回:
        DataFrame: 包含新特征的数据框
    
    新特征包括:
    1. 索赔金额相关特征：每车索赔金额、各类索赔比例
    2. 客户特征：年龄分组、客户时长分组
    3. 保单特征：月保费、是否有伞形保险
    4. 事故特征：是否夜间事故、是否高额索赔
    5. 财务特征：净资本、是否有资本收益/损失
    """
    df = df.copy()
    
    # 1. 索赔金额相关特征
    df['claim_per_vehicle'] = df['total_claim_amount'] / (df['number_of_vehicles_involved'] + 1)
    df['injury_ratio'] = df['injury_claim'] / (df['total_claim_amount'] + 1)
    df['property_ratio'] = df['property_claim'] / (df['total_claim_amount'] + 1)
    df['vehicle_ratio'] = df['vehicle_claim'] / (df['total_claim_amount'] + 1)
    
    # 2. 客户特征 - 将连续变量分组
    df['customer_age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 100], labels=[0, 1, 2, 3])
    df['customer_tenure_group'] = pd.cut(df['months_as_customer'], bins=[0, 12, 60, 120, 1000], labels=[0, 1, 2, 3])
    
    # 3. 保单特征
    df['premium_per_month'] = df['policy_annual_premium'] / 12  # 月保费
    df['has_umbrella'] = (df['umbrella_limit'] > 0).astype(int)  # 是否有伞形保险
    
    # 4. 事故特征
    df['is_night_accident'] = ((df['incident_hour_of_the_day'] >= 22) | 
                               (df['incident_hour_of_the_day'] <= 6)).astype(int)
    df['high_claim_amount'] = (df['total_claim_amount'] > 
                               df['total_claim_amount'].quantile(0.75)).astype(int)
    
    # 5. 财务特征
    df['net_capital'] = df['capital-gains'] - df['capital-loss']
    df['has_capital_gains'] = (df['capital-gains'] > 0).astype(int)
    df['has_capital_loss'] = (df['capital-loss'] > 0).astype(int)
    
    return df

# 步骤3: 特征工程
print("\n🔧 步骤3: 特征工程")
print("   创建新的特征以增强模型的预测能力")

# 应用特征工程函数
train_df_engineered = create_features(train_df)
test_df_engineered = create_features(test_df)

# 统计新创建的特征数量
new_features_count = train_df_engineered.shape[1] - train_df.shape[1]
print(f"   ✅ 特征工程完成，新增 {new_features_count} 个特征")
print(f"   📊 训练集特征数: {train_df.shape[1]} → {train_df_engineered.shape[1]}")
print(f"   📊 测试集特征数: {test_df.shape[1]} → {test_df_engineered.shape[1]}")

# 步骤4: 特征选择
print("\n🔧 步骤4: 特征选择")
print("   选择数值特征用于模型训练")

# 定义需要排除的列（目标变量、标识符、日期等）
exclude_cols = [
    'fraud_reported',      # 目标变量
    'policy_number',       # 保单编号（标识符）
    'policy_bind_date',    # 保单生效日期
    'incident_date',       # 事故日期
    'incident_location'    # 事故地点
]

# 选择数值特征
numeric_features = [
    col for col in train_df_engineered.columns 
    if col not in exclude_cols and 
    train_df_engineered[col].dtype in ['int64', 'float64']
]

print(f"   📊 可用的数值特征数量: {len(numeric_features)}")

# 准备特征矩阵和目标变量
X_train_full = train_df_engineered[numeric_features]
y_train = train_df_engineered['fraud_reported']
X_test_full = test_df_engineered[numeric_features]

# 处理无穷大和NaN值
print("   🔧 处理异常值（无穷大和NaN）...")
X_train_full = X_train_full.replace([np.inf, -np.inf], np.nan)
X_test_full = X_test_full.replace([np.inf, -np.inf], np.nan)
X_train_full = X_train_full.fillna(0)
X_test_full = X_test_full.fillna(0)

# 显示最终数据形状
print(f"   📊 最终训练集形状: {X_train_full.shape}")
print(f"   📊 最终测试集形状: {X_test_full.shape}")
print(f"   🎯 欺诈案例数量: {y_train.sum()} 个 ({y_train.mean():.2%})")

print("✅ 数据预处理完成")

# =============================================================================
# 3. 模型训练和评估
# =============================================================================
print("\n" + "=" * 60)
print("🤖 开始模型训练和评估")
print("=" * 60)

# 步骤1: 数据标准化
print("\n🔧 步骤1: 数据标准化")
print("   将特征标准化到相同尺度，提高模型性能")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_full)
X_test_scaled = scaler.transform(X_test_full)
print("   ✅ 数据标准化完成")

# 步骤2: 数据划分
print("\n🔧 步骤2: 数据划分")
print("   将训练数据划分为训练集和验证集")

X_train_split, X_val, y_train_split, y_val = train_test_split(
    X_train_scaled, y_train, 
    test_size=0.2,           # 20%作为验证集
    random_state=42,         # 固定随机种子，确保结果可重现
    stratify=y_train         # 分层抽样，保持欺诈比例一致
)

print(f"   📊 训练集大小: {X_train_split.shape[0]} 样本")
print(f"   📊 验证集大小: {X_val.shape[0]} 样本")
print(f"   📊 特征数量: {X_train_split.shape[1]} 个")
print(f"   🎯 训练集欺诈比例: {y_train_split.mean():.2%}")
print(f"   🎯 验证集欺诈比例: {y_val.mean():.2%}")

# 步骤3: 模型定义
print("\n🔧 步骤3: 模型定义")
print("   定义多个机器学习模型进行对比")

models = {
    'Random Forest': RandomForestClassifier(
        n_estimators=100,        # 100棵决策树
        max_depth=10,            # 最大深度10
        min_samples_leaf=5,      # 叶节点最小样本数5
        class_weight='balanced', # 处理类别不平衡
        random_state=42
    ),
    'Gradient Boosting': GradientBoostingClassifier(
        n_estimators=100,        # 100个弱学习器
        learning_rate=0.1,       # 学习率0.1
        max_depth=6,             # 最大深度6
        random_state=42
    ),
    'Logistic Regression': LogisticRegression(
        class_weight='balanced', # 处理类别不平衡
        random_state=42,
        max_iter=1000            # 最大迭代次数
    ),
    'SVM': SVC(
        class_weight='balanced', # 处理类别不平衡
        probability=True,        # 启用概率预测
        random_state=42
    )
}
# 步骤4: 模型训练和评估
print("\n🔧 步骤4: 模型训练和评估")
print("   训练多个模型并评估性能")

model_results = {}

for name, model in models.items():
    print(f"\n🤖 训练 {name}...")
    
    # 训练模型
    model.fit(X_train_split, y_train_split)
    
    # 在验证集上进行预测
    y_pred = model.predict(X_val)
    y_pred_proba = model.predict_proba(X_val)[:, 1]  # 欺诈概率
    
    # 计算评估指标
    accuracy = accuracy_score(y_val, y_pred)      # 准确率
    precision = precision_score(y_val, y_pred)    # 精确率（预测为欺诈中实际欺诈的比例）
    recall = recall_score(y_val, y_pred)          # 召回率（实际欺诈中被正确识别的比例）
    f1 = f1_score(y_val, y_pred)                  # F1分数（精确率和召回率的调和平均）
    auc = roc_auc_score(y_val, y_pred_proba)      # AUC（ROC曲线下面积）
    
    # 保存结果
    model_results[name] = {
        'model': model,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'auc': auc,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }
    
    # 显示训练结果
    print(f"   ✅ {name} 训练完成")
    print(f"      📊 准确率: {accuracy:.4f}")
    print(f"      🎯 精确率: {precision:.4f}")
    print(f"      🔍 召回率: {recall:.4f}")
    print(f"      ⚖️  F1分数: {f1:.4f}")
    print(f"      📈 AUC: {auc:.4f}")

# 步骤5: 模型性能对比
print("\n🔧 步骤5: 模型性能对比")
print("   比较不同模型的性能表现")

# 创建性能对比表
comparison_df = pd.DataFrame({
    'Model': list(model_results.keys()),
    'Accuracy': [results['accuracy'] for results in model_results.values()],
    'Precision': [results['precision'] for results in model_results.values()],
    'Recall': [results['recall'] for results in model_results.values()],
    'F1-Score': [results['f1'] for results in model_results.values()],
    'AUC': [results['auc'] for results in model_results.values()]
})

# 显示性能对比表
print("\n📊 模型性能对比表:")
print(comparison_df.round(4))

# 找出最佳模型（基于AUC指标）
best_model_name = comparison_df.loc[comparison_df['AUC'].idxmax(), 'Model']
best_model = model_results[best_model_name]['model']

print(f"\n🏆 最佳模型分析:")
print(f"   🥇 最佳模型: {best_model_name}")
print(f"   📈 最佳AUC: {model_results[best_model_name]['auc']:.4f}")
print(f"   📊 最佳准确率: {model_results[best_model_name]['accuracy']:.4f}")
print(f"   🎯 最佳精确率: {model_results[best_model_name]['precision']:.4f}")
print(f"   🔍 最佳召回率: {model_results[best_model_name]['recall']:.4f}")
print(f"   ⚖️  最佳F1分数: {model_results[best_model_name]['f1']:.4f}")

# =============================================================================
# 4. 结果分析和总结
# =============================================================================
print("\n" + "=" * 60)
print("📊 结果分析和总结")
print("=" * 60)

# 模型性能总结
print("\n📈 模型性能总结:")
print("   在保险欺诈检测任务中，我们训练了4个不同的机器学习模型：")
print("   • Random Forest (随机森林)")
print("   • Gradient Boosting (梯度提升)")
print("   • Logistic Regression (逻辑回归)")
print("   • SVM (支持向量机)")

print(f"\n🏆 最佳模型: {best_model_name}")
print(f"   • AUC: {model_results[best_model_name]['auc']:.4f} - 模型区分能力良好")
print(f"   • 准确率: {model_results[best_model_name]['accuracy']:.4f} - 整体预测准确度")
print(f"   • 精确率: {model_results[best_model_name]['precision']:.4f} - 预测为欺诈的准确性")
print(f"   • 召回率: {model_results[best_model_name]['recall']:.4f} - 欺诈案例的识别率")

# =============================================================================
# 5. 模型优化建议
# =============================================================================
print("\n" + "=" * 60)
print("💡 模型优化建议")
print("=" * 60)

print("\n🔧 技术优化建议:")
print("1. 📊 特征工程优化:")
print("   • 尝试更多的特征工程，如创建新特征或使用特征选择技术")
print("   • 考虑使用PCA降维或特征重要性筛选")
print("   • 探索特征交互项和多项式特征")

print("\n2. 🤖 算法优化:")
print("   • 尝试不同的机器学习算法，如XGBoost、LightGBM等")
print("   • 使用集成学习方法（Stacking、Blending）")
print("   • 考虑深度学习模型（神经网络）")

print("\n3. ⚙️ 超参数优化:")
print("   • 使用网格搜索或贝叶斯优化调整模型超参数")
print("   • 进行交叉验证以获得更稳定的性能评估")
print("   • 尝试不同的评估指标组合")

print("\n4. ⚖️ 类别不平衡处理:")
print("   • 使用过采样技术（SMOTE、ADASYN）")
print("   • 使用欠采样技术（RandomUnderSampler）")
print("   • 调整类别权重或使用代价敏感学习")

# =============================================================================
# 6. 大模型在保险反欺诈中的应用
# =============================================================================
print("\n" + "=" * 60)
print("🤖 大模型在保险反欺诈中的应用")
print("=" * 60)

print("\n📝 应用背景:")
print("传统机器学习方法在结构化数据上表现良好，但在处理非结构化数据")
print("（如事故描述、客户沟通记录等）方面存在局限性。大模型（如GPT）")
print("可以弥补这一不足，提供更全面的欺诈检测能力。")

print("\n🎯 大模型应用场景:")
print("1. 📄 非结构化文本分析:")
print("   • 分析索赔描述、事故报告和客户沟通中的异常")
print("   • 识别不一致或不合理的事故描述")
print("   • 检测语言模式和情感分析")

print("\n2. 🖼️ 跨模态信息整合:")
print("   • 结合图像（如事故照片）和文本信息")
print("   • 多模态欺诈检测")

print("\n3. 🧠 知识增强推理:")
print("   • 利用保险领域知识进行更深入的欺诈模式识别")
print("   • 基于规则的推理与机器学习结合")

# 示例：大模型分析索赔描述
print("\n📋 示例：索赔描述分析")
claim_descriptions = [
    "车辆在高速公路上行驶时，突然被前方车辆追尾，导致后保险杠损坏。",
    "停车场内，车辆被不明物体刮蹭，造成车身多处划痕。",
    "车辆在夜间行驶时，撞到路边的电线杆，前保险杠和引擎盖严重损坏。",
    "车辆在停车场被撞，导致车门凹陷，但车内物品神奇地消失了，包括一个全新的笔记本电脑和一个价值5000元的手表。",
    "车辆在正常行驶过程中，发动机突然起火，导致整车烧毁。事发前一周刚刚增加了保险额度。"
]

descriptions_df = pd.DataFrame({
    'claim_id': range(1, 6),
    'description': claim_descriptions
})

print("\n📄 索赔描述示例:")
print(descriptions_df)

print("\n🔍 大模型分析要点:")
print("• 描述1-3: 正常的事故描述，符合常见事故模式")
print("• 描述4: 可疑描述，'神奇地消失'等词汇暗示可能的欺诈")
print("• 描述5: 高度可疑，事故时机与保险额度增加时间吻合")

print("\n" + "=" * 60)
print("✅ 保险反欺诈案例研究完成")
print("=" * 60) 