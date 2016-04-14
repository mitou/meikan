# meikan
未踏名鑑プロジェクト

公開ページ http://www.mitou.org/people/

議論スペース https://mitou.cybozu.com/k/#/space/17

---

- secret.pyを作成し、APIトークンを配置する。 https://mitou.cybozu.com/k/#/space/17/thread/179
- cache.pyを実行→kintoneから最新のデータがダウンロードされ、ローカルにall_dataという名前でキャッシュされる
  (たぶん必要なライブラリの説明が欠けている)
- 機械的更新をするならupdater.pyのconvert関数を適切に実装するなり、オプションで指定するなりして、
  dry-runして確認した後、--realオプションをつけて実際にkitnoneに変更を掛ける
- renderer.pyでoutputにHTMLが出力される