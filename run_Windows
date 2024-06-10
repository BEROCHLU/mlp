# result/output.log を削除
Remove-Item -Path ./result/output.log -ErrorAction Ignore

# batch フォルダ内の全ての .json ファイルに対してループ
Get-ChildItem -Path ./batch -Filter *.json | ForEach-Object {
    # ファイルの内容を app.py に渡す
    Get-Content $_.FullName | python inputstd.py >> ./result/output.log
}
