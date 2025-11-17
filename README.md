# hyouon_bunsetsu
表音, 文節にする

* -tや-fなしで実行すると、`>>> `が出てきます。ここにテキストを入力するとhyouonの結果が出てきます
* -Hy, -Su, -Ka, -Pr, -P1, -P2を使うとその関数のみの出力が出ます。-aにすると全ての関数が出力されます
* -sは何の関数かが文章の最初に出てきます
* -shは各関数の出力ごとにハイフン50個が出てきます
* 以下は`python hyouon.py -h`の結果です
```
usage: hyouon.py [-h] [-t TEXT] [-f FILE] [-o OUTPUT] [-Hy] [-Su] [-Ka] [-Pr] [-P1] [-P2] [-a] [-s] [-sh]

表音(カタカナ限定)

options:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  テキスト
  -f FILE, --file FILE  ファイル
  -o OUTPUT, --output OUTPUT
                        出力ファイル
  -Hy, --hyouon         hyouon
  -Su, --surf           bunsetsu surface
  -Ka, --kana           bunsetsu kana
  -Pr, --pron           bunsetsu pron
  -P1, --pos1           bunsetsu pos1(hinshi)
  -P2, --pos2           bunsetsu pos2(hinshi)
  -a, --all             all(hyouon bunsetsu)
  -s, --split           output with func desc
  -sh, --splitTXT       output with split text('-'*50)

  ```
