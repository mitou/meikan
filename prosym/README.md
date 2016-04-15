# プロシン等データの未踏名鑑へのマージプロジェクト

プロシンの発表者の中には未踏関係者も多いので、過去のプロシンの発表者リストを作ってみました。 

## 結果

過去31年分の冬のプロシン発表者についてのデータ整形を行った。
5時間で、入力されたデータ1646行。それを西尾がスクリプトで未踏人材名簿と突き合せた結果、
未踏人材の講演に関する情報が336件、未踏人材の所属に関する情報が339件入手出来、151人の情報が増強された。

発表者と発表タイトルの対応がこちら https://github.com/nishio/mitou_meikan/blob/master/prosym_title.csv

発表者とプロシン時点での所属の対応がこちら https://github.com/nishio/mitou_meikan/blob/master/prosym_affiliation.csv

## 流れ

元データは「第25回,第27回 ～ 第44回(天海記録) 」とそれ以降のプログラム。 http://www.ipsj.or.jp/prosym/prosyncontents.html

元データを1つのテキストファイルにまとめたもの https://github.com/nishio/mitou_meikan/blob/master/prosym_raw.txt

機械的に扱えるように整形する際の手順書 https://github.com/nishio/mitou_meikan/blob/master/prosym_guide.txt

整形済みデータA https://github.com/nishio/mitou_meikan/blob/master/prosym_formatted.txt

変換スクリプトB https://github.com/nishio/mitou_meikan/blob/master/prosym_to_csv.py

A,Bから作られた所属データ https://github.com/nishio/mitou_meikan/blob/master/prosym_affiliation.csv

A,Bから作られた講演データ https://github.com/nishio/mitou_meikan/blob/master/prosym_title.csv

