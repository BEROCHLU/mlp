import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.ticker import AutoMinorLocator


# ファイルを読み込む
file_path = "./result/tf-batch.log"

with open(file_path, "r", encoding="utf-8") as file:
    # ファイルの内容を読み込む
    content = file.read()

# セクションを分割
sections = content.split("\n\n")

# セクションごとの最後の日付とNormの値を抽出
lstDt = []
norm_values = []

# 日付のパターン
date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

for section in sections:
    lines = section.split("\n")
    # 最初の行はタイムスタンプなのでスキップ
    lines = lines[1:]

    for line in reversed(lines):
        # 日付を検索
        date_match = date_pattern.search(line)
        if date_match:
            # 日付を解析しリストに追加
            date_str = date_match.group()
            date = datetime.strptime(date_str, "%Y-%m-%d")
            lstDt.append(date)
            break

    # Normの値を検索
    norm_line = [line for line in lines if line.startswith("Norm:")]
    if norm_line:
        norm_value = float(norm_line[0].split(":")[1].strip())
        norm_values.append(norm_value)

# グラフを描画
# plt.figure(figsize=(14, 7))
# 日付を0から始まる連続したインデックスに変換
arrInt = np.arange(len(lstDt))

fig, ax = plt.subplots(figsize=(12, 6))

# インデックスを使用してプロット
ax.plot(arrInt, norm_values, marker="o", markersize=4)
# X軸のラベルをインデックスに設定
ax.set_xticks(arrInt)
# インデックスをstring日付に置き換える
ax.set_xticklabels([date.strftime("%b%d") for date in lstDt], rotation=45, ha="right")
# X軸の範囲を調整
ax.set_xlim([0, len(lstDt) - 1])

# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=1, tz=None))
# plt.gcf().autofmt_xdate()  # X軸の日付ラベルを斜めにして重なりを防ぐ

plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))  # Y軸の補助メモリを2ずつに設定
plt.title("The Sakata Index", fontsize=10)
plt.xticks(fontsize=9)  # X軸の目盛りのフォントサイズを設定
plt.grid(which="both")
plt.tight_layout()
plt.savefig("./result/plot-single.png")  # showの前でないと機能しない
plt.show()
