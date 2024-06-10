# result/output.log を事前にクリア（存在しない場合は作成）
$null > ./result/output.log

# batch フォルダ内の全ての .json ファイルに対してループ
Get-ChildItem -Path ./batch -Filter *.json | ForEach-Object {
    # ファイルの内容を inlinestd.py に渡し、結果を出力ファイルに追記
    Get-Content $_.FullName | python ./src/inlinestd.py >> ./result/output.log
}
