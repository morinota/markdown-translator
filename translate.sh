# !/bin/bash

# poetry run python -m src.markdown_translator.app --input-md-path {引数}を実行する
# 引数: markdownファイルの絶対

# 引数の数が1でない場合はstatus code 1で終了
if [ $# -ne 1 ]; then
  echo "エラー: 引数は1つのmarkdownファイルの絶対パスを指定してください"
  exit 1
fi

# 引数を変数に代入
input_md_path=$1

# アプリを実行
poetry run python -m src.markdown_translator.app --input-md-path "$input_md_path"

# 終了ステータスを返す
exit 0
