# TensorFlowを用いた回帰モデルの実装

このプロジェクトは、JSONファイルから読み込んだデータを用いてTensorFlowとKerasを使用した回帰モデルのトレーニングを行い、モデルの性能を評価するものです。

## 必要条件

- Python 3.x
- TensorFlow
- NumPy
- Matplotlib

必要なパッケージは以下のコマンドでインストールできます。

```bash
pip install tensorflow numpy matplotlib
```

## プロジェクト構成

- `seikika.json`: 入力データを含むJSONファイル
- `diff.py`: データの読み込み、モデルのトレーニング、結果のプロットを行うメインスクリプト
- `./image/latest-acc.png`: 結果の累積プロットの出力画像

## 使用方法

1. JSONファイルを `./json/` ディレクトリに配置し、 `seikika.json` と名前を付けます。
2. `diff.py` スクリプトを実行します。

```bash
python diff.py
```

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細はLICENSEファイルをご覧ください。
