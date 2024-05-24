import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models, layers, optimizers

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

scaled_predictions = []


# コールバッククラスの定義
class FinalPredictionCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        global scaled_predictions
        if epoch == self.params["epochs"] - 1:  # 最後のエポックの場合
            predictions = model.predict(X, verbose=0)
            scaled_predictions = predictions.flatten()
            # print(f"Final Scaled Predictions = {scaled_predictions}")

            # 差分をパーセントに直して表示
            differences_percentage = ((y - scaled_predictions) / scaled_predictions) * 100
            print(
                f"Differences between scaled predictions and actual outputs (in percentage):\n"
            )
            print(differences_percentage)


# モデルのトレーニング
history = model.fit(
    X, y, epochs=100, batch_size=10, verbose=1, callbacks=[FinalPredictionCallback()]
)

# モデルの評価
loss = model.evaluate(X, y)
print(f"Final Loss: {loss:.6f}")
