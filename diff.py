import json
from functools import reduce
from pprint import pprint

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models, layers, optimizers
import matplotlib.pyplot as plt

# 乱数シードを固定
np.random.seed(42)
tf.random.set_seed(42)

# JSONファイルを読み込む
try:
    with open("./json/seikika.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("Config file not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error decoding JSON.")
    exit(1)

# 入力と出力のリストを初期化
inputs = []
outputs = []

# データをリストに格納
for entry in data["listdc"]:
    inputs.append(entry["input"])
    outputs.append(entry["output"][0])  # outputs を 1 次元に変更

# Numpy配列に変換
X = np.array(inputs)
y = np.array(outputs)

# モデルの構築
model = models.Sequential()
model.add(layers.Input(shape=(2,)))
model.add(layers.Dense(32, activation="relu", kernel_initializer="he_normal"))
model.add(layers.Dense(1))

# モデルのコンパイル
model.compile(optimizer=optimizers.Adam(learning_rate=0.001), loss="mean_squared_error")

differences_percentage = np.array([])


# コールバッククラスの定義
class FinalPredictionCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        global differences_percentage

        if epoch == self.params["epochs"] - 1:  # 最後のエポックの場合
            predictions = model.predict(X, verbose=0)
            scaled_predictions = predictions.flatten()
            # 差分をパーセントに直して表示
            differences_percentage = ((y - scaled_predictions) / scaled_predictions) * 100
            differences_percentage = np.round(differences_percentage, 2)
            pprint(differences_percentage)


# モデルのトレーニング
history = model.fit(
    X, y, epochs=200, batch_size=10, verbose=0, callbacks=[FinalPredictionCallback()]
)

# モデルの評価
loss = model.evaluate(X, y)
pprint(f"Final Loss: {loss:.6f}\n")

# 累積結果を格納するリストを初期化
cumulative_results = []

# reduceを使って蓄積しながら結果をリストに格納する関数
def accumulate_and_collect(accumulated, current):
    new_accumulated = accumulated + current
    new_accumulated = np.round(new_accumulated, 2)
    cumulative_results.append(new_accumulated)
    return new_accumulated

# 初期値0でreduceを実行
final_result = reduce(accumulate_and_collect, differences_percentage, 0)
print(cumulative_results)

# グラフをプロット
plt.figure(figsize=(10, 6))
plt.plot(cumulative_results, marker='o')
plt.title('Cumulative Differences in Percentage')
plt.xlabel('Index')
plt.ylabel('Cumulative Value')
plt.grid(True)
plt.savefig("./image/latest-acc.png")  # showの前でないと機能しない
plt.show()