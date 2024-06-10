# MLP Project

このプロジェクトは、JSONファイルから読み込んだデータを用いてTensorFlowとKerasを使用した回帰モデルのトレーニングを行い、モデルの性能を評価するものです。

## 概要

プロジェクトは、機械学習の回帰モデルを構築し、トレーニングするためのPythonスクリプトを含んでいます。データは`batch/`ディレクトリ内のJSONファイルから読み込まれ、結果は`result/`ディレクトリに保存されます。

## 使用技術

- Python
- TensorFlow
- Keras
- Pandas
- NumPy

## 主要スクリプト

- `src/inlinestd.py`: 標準入力からJSONデータを読み込み、モデルのトレーニングを行います。
- `src/daily-acc.py`: 日次でモデルの精度を計算し、結果を`result/daily-acc.txt`に保存します。
- `src/batch-acc.py`: バッチ処理によるモデルの精度を計算し、結果を`result/batch-acc.log`に保存します。
- `src/batch-accw.py`: 重み付けされたバッチ処理によるモデルの精度を計算し、結果を`result/batch-accw.log`に保存します。

## 実行方法

LinuxとWindowsの両方で実行スクリプトが用意されています。

- Linux: `run_Linux.sh`スクリプトを実行してください。
- Windows: `run_Windows.ps1`スクリプトを実行してください。

これらのスクリプトは、`batch/`ディレクトリ内の全てのJSONファイルに対して`src/inlinestd.py`を実行し、結果を`result/output.log`に追記します。
