# プロシン等データの未踏名鑑へのマージプロジェクト

プロシンの発表者の中には未踏関係者も多いので、過去のプロシンの発表者リストを作ってみました。 

## 結果

過去31年分の冬のプロシン発表者についてのデータ整形を行った。
5時間で、入力されたデータ1646行。それを西尾がスクリプトで人と発表タイトルの対応付けCSVおよび人と所属の対応付けCSVに変換した。

発表者と発表タイトルの対応がこちら https://github.com/nishio/mitou_meikan/blob/master/prosym_title.csv

発表者とプロシン時点での所属の対応がこちら https://github.com/nishio/mitou_meikan/blob/master/prosym_affiliation.csv

その後、未踏名鑑と突き合せた結果、未踏人材の講演に関する情報が336件、未踏人材の所属に関する情報が339件入手出来、151人の情報が増強された。

## 流れ

元データは「第25回,第27回 ～ 第44回(天海記録) 」とそれ以降のプログラム。 http://www.ipsj.or.jp/prosym/prosyncontents.html

元データを1つのテキストファイルにまとめたもの https://github.com/nishio/mitou_meikan/blob/master/prosym_raw.txt

機械的に扱えるように整形する際の手順書 https://github.com/nishio/mitou_meikan/blob/master/prosym_guide.txt

整形済みデータA https://github.com/nishio/mitou_meikan/blob/master/prosym_formatted.txt

変換スクリプトB https://github.com/nishio/mitou_meikan/blob/master/prosym_to_csv.py

A,Bから作られた所属データ https://github.com/nishio/mitou_meikan/blob/master/prosym_affiliation.csv

A,Bから作られた講演データ https://github.com/nishio/mitou_meikan/blob/master/prosym_title.csv

## 続編

プロシンの結果が良好だったので、夏のプロシンと情報科学若手の会にも手を広げた。今回は幹事の情報も入力に含めた。データの整形には10時間かかった。

未踏卒業生との共通部分集合は、夏のプロシン 50人、190件、夏のプロシン幹事 12人、46件、若手の会 28人、128件、若手の会幹事 9人、32件。
合計で396件。夏のプロシンが5時間で339件だったのに比較すると、時間あたり成果は少ない。プロシンデータの質と密度が高かったのだろう。

Q: 若手の会には幹事がいるがプロシンにはいないのか？ A: プロシンにもいるが前回の入力ソースとして渡したプログラム一覧には載っていない。別途入力することが有益な可能性もある。

フィードバック: 情報科学若手の会には、特定の発表ではなく「みんなでこのテーマについて議論しました」という回があり、その回では参加者の一覧と、それが幹事であるかどうかのフラグがある

Q: 幹事が発表しないこともあり得るか A: 大いにあり得る。プロシンの座長と同様に、それ単体で活動とみなすのがよいと思う。

## その他の情報収集プラン

https://github.com/nishio/mitou_meikan/blob/master/plan.txt

高専カンファレンスはハンドルネームでの発表が意外と多くてDBとの突合せがうまく行かなさそうなので保留
