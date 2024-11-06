from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# 讀取 Excel 檔案並準備數據
df = pd.read_excel("C:\\Users\\chen\\Desktop\\台灣樂團資料.xlsx")
features = ['danceability', 'energy', 'valence', 'tempo']

# 確保數據沒有缺失值
df = df.dropna(subset=features)

# 標準化數據
scaler = StandardScaler()
X = scaler.fit_transform(df[features])

# 設置 KNN 模型
knn = NearestNeighbors(n_neighbors=5)
knn.fit(X)

# 心情與音樂特徵對應表
MOOD_MAPPING = {
    "開心": [0.8, 0.8, 0.9, 120],
    "悲傷": [0.4, 0.3, 0.2, 70],
    "放鬆": [0.5, 0.4, 0.6, 80],
    "激昂": [0.9, 0.9, 0.8, 130],
    "懷舊": [0.6, 0.5, 0.5, 100],
    "憤怒": [0.7, 0.9, 0.2, 140],
    "愛戀": [0.7, 0.6, 0.7, 110],
    "驚奇": [0.8, 0.8, 0.8, 120],
    "興奮": [0.85, 0.85, 0.85, 125],
    "孤獨": [0.3, 0.3, 0.2, 60],
    "安慰": [0.5, 0.4, 0.6, 75],
    "迷茫": [0.4, 0.4, 0.3, 80],
    "熱情": [0.9, 0.8, 0.7, 135],
    "輕鬆": [0.6, 0.5, 0.7, 85],
    "幸福": [0.8, 0.7, 0.9, 115],
    "感傷": [0.4, 0.3, 0.3, 70],
    "困惑": [0.4, 0.5, 0.4, 90],
    "愉悅": [0.8, 0.7, 0.8, 120],
    "振奮": [0.7, 0.8, 0.8, 110],
    "平靜": [0.5, 0.4, 0.7, 75]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    mood = data.get('mood', '').strip()

    if mood not in MOOD_MAPPING:
        return jsonify({"error": "未知的心情，請輸入有效的心情。"})

    # 根據心情獲取音樂特徵
    mood_features = MOOD_MAPPING[mood]
    mood_features_scaled = scaler.transform([mood_features])

    # 使用 KNN 模型找到最近的歌曲
    distances, indices = knn.kneighbors(mood_features_scaled)
    recommendations = df.iloc[indices[0]][['歌曲名稱', '樂團名稱']].to_dict(orient='records')

    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
