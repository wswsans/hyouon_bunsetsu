# -*- coding: utf-8 -*-
import fugashi

def bunsetsu(text, output = "surf"):
    # 改行があるとTaggerで壊れるので分離していく
    if text == "":
        return ""
    if "\n" in text:
        temp = []
        for i in text.split("\n"):
            temp.append( bunsetsu(i, output) )
        return "\n".join(temp)
    if " " in text:
        temp = []
        for i in text.split(" "):
            temp.append( bunsetsu(i, output) )
        return " ".join(temp)

    tagger = fugashi.Tagger()
    # 前の単語の品詞が付属語(コメントアウト), 今の単語の品詞が自立語ならスペースで分離
    jiritsugo = [
        "名詞",
        "代名詞",
        "形状詞",
        "連体詞",
        "副詞",
        "接続詞",
        "感動詞",
        "動詞",
        "形容詞",
        # "助動詞",
        # "助詞",
        "接頭辞",
        # "接尾辞",
        # "記号",
        # "補助記号",
        "空白"
    ]
    # 前後どちらもスペースを入れない
    non_space = [
        "記号",
        "補助記号",
        "空白"
    ]
    word_data = [{
        "surf": word.surface,
        "kana": word.feature.kana,
        "pron": word.feature.pron,
        "pos1": word.feature.pos1,
        "pos2": word.feature.pos2
    } for word in tagger(text)]
    result = ""
    prev_word = dict.fromkeys(word_data[0])
    for i in word_data:
        # ここ相当ハードコードしまくって嫌な気持ち
        # result += "/"

        ### 文節切りする
        ## 直前の単語と今の単語の間にスペースを入れるかどうか
        # 入れるもの
        # * 付属語→自立語: スペース: and (not prev_word["pos1"] in jiritsugo)
        # * 名詞→名詞: not スペース: and not (prev_word["pos1"] == "名詞" and i["pos1"] == "名詞")
        # * 接頭辞→名詞: not スペース
        # * 数詞: not スペース
        # * 前後いずれかnon_space: not スペース
        if i["pos1"] in jiritsugo \
            and not (prev_word["pos1"] == "接頭辞" and i["pos1"] == "名詞") \
            and not prev_word["pos2"] == "数詞" \
            and not (prev_word["pos1"] in non_space or i["pos1"] in non_space):
            result += " "

        ### 追加するときの
        if i["kana"] == "ヲ":
            # ヲはヲで良い
            result += "ヲ"
        elif i[output] in ["", " ", None]:
            # 何も入ってないみたいなのはsurfそのまま追加しとく
            result += i["surf"]
        else:
            # 名詞だけpos2を見るのがコメントにあるもの
            if output == "pos2":# and i["pos1"] == "名詞":
                result += f"{i['pos1']}({i['pos2']})"
            else:
                result += i[output]
        prev_word = i

    return result.strip()

def hyouon(text):
    # カタカナ固定
    # text = kanji_to_katakana(text)
    text = bunsetsu(text, "pron")
    vowel_dict = {
        "": "", # 空文字対策
        "ア": "ア", "イ": "イ", "ウ": "ウ", "エ": "エ", "オ": "オ",
        "カ": "ア", "キ": "イ", "ク": "ウ", "ケ": "エ", "コ": "オ",
        "サ": "ア", "シ": "イ", "ス": "ウ", "セ": "エ", "ソ": "オ",
        "タ": "ア", "チ": "イ", "ツ": "ウ", "テ": "エ", "ト": "オ",
        "ナ": "ア", "ニ": "イ", "ヌ": "ウ", "ネ": "エ", "ノ": "オ",
        "ハ": "ア", "ヒ": "イ", "フ": "ウ", "ヘ": "エ", "ホ": "オ",
        "マ": "ア", "ミ": "イ", "ム": "ウ", "メ": "エ", "モ": "オ",
        "ヤ": "ア", "ユ": "ウ", "ヨ": "オ",
        "ラ": "ア", "リ": "イ", "ル": "ウ", "レ": "エ", "ロ": "オ",
        "ワ": "ア", "ヰ": "イ", "ヱ": "エ", "ヲ": "オ",
        "ン": "ン",

        # 濁音・半濁音
        "ガ": "ア", "ギ": "イ", "グ": "ウ", "ゲ": "エ", "ゴ": "オ",
        "ザ": "ア", "ジ": "イ", "ズ": "ウ", "ゼ": "エ", "ゾ": "オ",
        "ダ": "ア", "ヂ": "イ", "ヅ": "ウ", "デ": "エ", "ド": "オ",
        "バ": "ア", "ビ": "イ", "ブ": "ウ", "ベ": "エ", "ボ": "オ",
        "パ": "ア", "ピ": "イ", "プ": "ウ", "ペ": "エ", "ポ": "オ",

        # 小書きカタカナ
        "ャ": "ア", "ュ": "ウ", "ョ": "オ", "ァ": "ア", "ィ": "イ", "ゥ": "ウ", "ェ": "エ", "ォ": "オ",
    }
    result = ""
    prev_text = ""
    for i in text:
        temp = i
        try:
            # 伸ばし棒削除
            if temp == "ー":
                temp = vowel_dict[prev_text]
            # 表音... オ段の後ろの「う」を「お」に対応する文字 (Wikipedia ひので字)
            # これbunsetsu関数でできたので削除
            # if vowel_dict[prev_text] == "オ" and temp == "ウ":
            #     temp = "オ"
        except KeyError:
            # vowel_dictにない文字出てくるだろうけどもうそれは別に良いでしょの意
            pass
        
        result += temp
        prev_text = temp

    return result

if __name__ == '__main__':
    import argparse
    # argparse idea by GPT
    # パーサーを作成
    parser = argparse.ArgumentParser(description="表音(カタカナ限定)")
    # オプションを追加
    parser.add_argument("-t", "--text", help="テキスト")
    parser.add_argument("-f", "--file", help="ファイル")
    parser.add_argument("-o", "--output", help="出力ファイル")

    parser.add_argument("-Hy", "--hyouon", action="store_true", help="hyouon")
    parser.add_argument("-Su", "--surf", action="store_true", help="bunsetsu surface")
    parser.add_argument("-Ka", "--kana", action="store_true", help="bunsetsu kana")
    parser.add_argument("-Pr", "--pron", action="store_true", help="bunsetsu pron")
    parser.add_argument("-P1", "--pos1", action="store_true", help="bunsetsu pos1(hinshi)")
    parser.add_argument("-P2", "--pos2", action="store_true", help="bunsetsu pos2(hinshi)")
    
    parser.add_argument("-a", "--all", action="store_true", help="all(hyouon bunsetsu)")

    parser.add_argument("-s", "--split", action="store_true", help="output with func desc")
    parser.add_argument("-sh", "--splitTXT", action="store_true", help="output with split text('-'*50)")
    # パース
    parsed = parser.parse_args()

    inp_text = parsed.text
    inp_file = parsed.file
    out_file = parsed.output
    if inp_file != None:
        with open(inp_file, "r") as f:
            inp_text = f.read()
        # print(inp_text)

    if inp_text == None:
        while not inp_text:
            inp_text = input(">>> ")

    bunsetsu_tags = {"surf": parsed.surf, "kana": parsed.kana, "pron": parsed.pron, "pos1": parsed.pos1, "pos2": parsed.pos2}
    other_tags = {"hyouon": parsed.hyouon}
    out_type = {**bunsetsu_tags, **other_tags}
    
    if parsed.all:
        # 全てTrueの意味
        out_type = dict.fromkeys(out_type, True)
    # 一つもなければhyouon
    if not (True in out_type.values()):
        out_type["hyouon"] = True

    # 結果を入れる + 関数の解説(func: ...)を入れるかどうか
    temp = []
    if out_type["hyouon"]:
        temp.append(hyouon(inp_text))
        if parsed.split:
            temp[-1] = "hyouon:\n" + temp[-1]
    for v in bunsetsu_tags.keys():
        if out_type[v]:
            temp.append(bunsetsu(inp_text, v))
            if parsed.split:
                temp[-1] = f"bunsetsu({v}):\n" + temp[-1]

    # 結果分けに---...を入れるかどうか
    if parsed.splitTXT:
        split_text = "\n" + "-"*50 + "\n"
    else:
        split_text = "\n\n"
    # 直接print or ファイル
    if out_file == None:
        print( split_text.join(temp) )
    else:
        with open(out_file, "w") as f:
            f.write( split_text.join(temp) )