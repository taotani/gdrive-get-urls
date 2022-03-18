# Share Csv Files and List URLs on Google Drive 
## 役割
Google Driveの特定のフォルダ(namely <FOLDER_NAME>)の中のCSVファイルを一括で共有設定にしてURLを取得するものです。以下を実行すると、urls.csvというファイルが作られます。

```
pipenv run python -m main <FOLDER_NAME>
```

## 出力ファイル(urls.csv)

以下の表を表現します

| file_name | url          |
|-----------|--------------|
| test1.csv | https://.... |

## インストール方法
以下を実行してください。
```
pipenv install
```

## 利用のために
OAuth 2.0 クライアントIDを発行して認証情報のJSONファイルをダウンロードし、credentials.jsonとして README.md と同じディレクトリにおいてください。
https://developers.google.com/workspace/guides/configure-oauth-consent