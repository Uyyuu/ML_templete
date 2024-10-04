# ML_templete

研究で使う python のデータ分析環境

## ディレクトリ構成

```
.
├── README.md
├── data
│   ├── processed       #前処理済みのデータ
│   └── raw             #生データ
├── docker
│   └── Dockerfile
├── docker-compose.yaml
├── models              #学習済みのモデルやモデルのアーキテクチャ
├── notebooks           #Jupyter notebook
│   └── sample.ipynb
├── outputs             #アウトプット
│   ├── figures         #図や表
│   └── images          #画像
├── poetry.lock
├── pyproject.toml
└── src
    ├── __init__.py
    ├── data            #データ生成やダウンロード
    ├── features        #特徴量エンジニアリング
    ├── models          #学習・推論
    └── visualization   #可視化
```

## セットアップ

- .env ファイルを作成(.env.sample を参考にする．)
- .env ファイルの `COMPOSE_PROJECT_NAME` を設定する．
  - この時の設定名がコンテナの名前になります．
- VSCode のコマンドパレットを開き，`Dev Containers: Reopen Container`を選択．
  - コマンドパレットのショートカット（［Command］＋［Shift］＋［P］キー）

## 参考サイト

- [ディレクトリ構成](https://zenn.dev/pluck/articles/63413cdd51f790)
