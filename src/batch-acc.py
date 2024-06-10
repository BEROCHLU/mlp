import json
from datetime import datetime
from functools import reduce
from glob import glob
from pprint import pprint

import numpy as np
import pandas as pd
import tensorflow as tf
from keras import layers, models, optimizers
from tensorflow import keras

# モデルの構築
model = models.Sequential()
model.add(layers.Input(shape=(2,)))
model.add(
    layers.Dense(
        16,
        activation="sigmoid",
        kernel_initializer=keras.initializers.Constant(0.5),  # he_normal
        # kernel_regularizer=keras.regularizers.l2(0.01),
    )
)
model.add(layers.Dense(1))
model.compile(optimizer=optimizers.Adam(learning_rate=0.001), loss="mean_squared_error")


# コールバッククラスの定義
class FinalPredictionCallback(keras.callbacks.Callback):
    def on_train_end(self, logs=None):
        global differences_percentage, dfPrint

        predictions = model.predict(X, verbose=0)
        scaled_predictions = predictions.flatten()
        # 差分をパーセントに直して表示
        differences_percentage = ((y - scaled_predictions) / scaled_predictions) * 100
        differences_percentage = np.round(differences_percentage, 2)

        dfPrint["Predict"] = np.round(scaled_predictions * DIV, 2)
        dfPrint["True"] = np.round(y * DIV, 2)
        # pprint(differences_percentage)


# EarlyStoppingコールバックの設定
early_stopping = keras.callbacks.EarlyStopping(
    monitor="loss", min_delta=0.0001, patience=300, verbose=0, mode="min"
)

path_list = glob("./batch/seikika*.json")

for file_path in path_list:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
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
    dates = []
    shortdates = []

    # データをリストに格納
    for entry in data["listdc"]:
        inputs.append(entry["input"])
        outputs.append(entry["output"][0])  # outputs を 1 次元に変更
        dates.append(entry["date"])

    for strDate in dates:
        date = datetime.strptime(strDate, "%Y-%m-%d")
        shortdates.append(date)

    dfPrint = pd.DataFrame()
    dfPrint["date"] = shortdates
    DIV = data["div"]

    len_size = len(outputs)
    # Numpy配列に変換
    X = np.array(inputs)
    y = np.array(outputs)

    differences_percentage = np.array([])

    # モデルのトレーニング
    history = model.fit(
        X,
        y,
        epochs=1000,
        batch_size=len_size,
        verbose=0,
        callbacks=[FinalPredictionCallback(), early_stopping],
    )

    # モデルの評価
    loss = model.evaluate(X, y, verbose=0)
    strLoss = f"{loss:.6f}"

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
    # pprint(np.array(cumulative_results))

    arrNorm = cumulative_results[:-1]  # 最大最小個超えもあるため最後の値だけを削除
    min_val = min(arrNorm)
    max_val = max(arrNorm)
    norm = ((final_result - min_val) / (max_val - min_val)) * 100
    strNorm = f"{norm:.2f}"

    dfPrint["diff"] = differences_percentage
    dfPrint["acc"] = cumulative_results

    pprint(dfPrint)
    print(f"Mean Absolute Error: {np.mean(np.abs(differences_percentage)):.2f}%")
    print(f"Epoch: {early_stopping.stopped_epoch}, Final Loss: {strLoss}")
    print(f"Norm: {strNorm}\n")
