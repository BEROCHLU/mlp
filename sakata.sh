#!/bin/bash

rm ./result/output.log
# batchフォルダ内の全ての.jsonファイルに対してループ
for file in ./batch/*.json; do
    # ファイルの内容をapp.pyに渡す
    cat "$file" | python inputstd.py >> ./result/output.log
done
