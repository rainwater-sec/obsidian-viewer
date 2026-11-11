# re は、決まった形の文字（例：[[ と ]] で囲まれた部分）を探して置き換えるための、Python に最初から入っている部品
import re
from pathlib import Path

from flask import Flask
# 名前は markdown だが、Markdown の文字を「読んで」、HTML の文字を「返す」関数
from markdown import markdown

app = Flask(__name__)


@app.route("/")
def 一覧():
    ノートの場所 = Path("ノート")
    表示する文字 = ""
    # rglob("*.md") は、フォルダの中を下の階層（legacy など）まで全部探して、名前が .md で終わるファイルを1つずつ返す
    for ノートファイル in ノートの場所.rglob("*.md"):
        リンク先 = "/note/" + ノートファイル.stem
        # <a href='行き先'>名前</a> は、押すと行き先へ移動する文字
        リンク = "<a href='" + リンク先 + "'>" + ノートファイル.name + "</a>"
        表示する文字 = 表示する文字 + リンク + "<br>"
    return 表示する文字


@app.route("/note/<name>")
def ノートの中身を表示(name):
    指定されたノート名 = name
    ノートの場所 = Path("ノート")
    # 上と同じ。フォルダの中を下の階層まで探して、.md ファイルを1つずつ返す
    for ノートファイル in ノートの場所.rglob("*.md"):
        if ノートファイル.stem == 指定されたノート名:
            ノートの中身 = ノートファイル.read_text(encoding="utf-8")
            # [[ノート名]] を探して、<a href='/note/ノート名'>ノート名</a> に置き換えた文字を返す
            # (.+?) は間の文字で、置き換え先の \1 にその文字が入る
            リンクに置き換えた中身 = re.sub(r"\[\[(.+?)\]\]", r"<a href='/note/\1'>\1</a>", ノートの中身)
            # Markdown の文字を、HTML の文字に変換する（例：「# 見出し」→「<h1>見出し</h1>」）
            # extensions=["tables"] は、表（| で区切った行）も HTML の表（<table>）に変換させる指定
            変換したHTML = markdown(リンクに置き換えた中身, extensions=["tables"])
            # スマホの画面の幅に合わせて表示させる指定。これがないと、スマホは全体を縮めて表示するので文字がとても小さくなる
            画面幅の指定 = "<meta name='viewport' content='width=device-width'>"
            # 見た目の指定（CSS）。font-size は文字の大きさ、max-width は横幅の上限、margin: auto は左右の余白を同じにして真ん中に置く
            見た目の指定 = "<style>body { font-size: 18px; max-width: 40em; margin: auto; }</style>"
            return 画面幅の指定 + 見た目の指定 + 変換したHTML
    return "ノートが見つかりません", 404

@app.route("/ping")
def ping():
    return "ok"