#!/bin/bash

# 出力ファイルを事前にクリア
> ./result/output.log

# batchフォルダ内の全ての.jsonファイルに対してループ
for file in ./batch/*.json; do
    # ファイルの内容をapp.pyに渡し、結果を出力ファイルに追記
    python ./src/inlinestd.py < "$file" >> ./result/output.log
done
