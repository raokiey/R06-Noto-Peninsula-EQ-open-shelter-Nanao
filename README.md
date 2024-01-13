# 令和6年能登半島地震 石川県七尾市避難所開設情報GISデータ

## 概要
このリポジトリでは、令和6年能登半島地震に関連して石川県七尾市のWebサイトにて公開されている[開設中の避難所情報](https://www.city.nanao.lg.jp/bosai/mail/202401021200.html)を石川県および七尾市が公開しているオープンデータをもとに位置情報などを付加して、GISデータ化したデータを公開しています。  
データ作成処理の定期実行（1時間毎）により、七尾市のWebサイト更新があった際に最新情報に更新される見込みです。  

以下のリンクより、最新のGeoJSON形式のデータがダウンロード可能です。
[https://raokiey.github.io/R06-Noto-Peninsula-EQ-open-shelter-Nanao/data/latest/open_shelter_Nanao-shi.geojson](https://raokiey.github.io/R06-Noto-Peninsula-EQ-open-shelter-Nanao/data/latest/open_shelter_Nanao-shi.geojson)  

また、[`./data/latest/`](./data/latest/) にCSV形式のデータも公開しています。 
過去のデータを利用したい方は、[`./data/history/`](./data/history/) にCSV形式のデータのみですが、保存しています。  
※ 公開当初は、2024年1月9日18時時点のデータのみを格納しています。  

## 注意事項
- 避難所によっては集計時間が異なることがあります。（七尾市Webサイトより）  
- 個人が作成したものです。注意はしていますが間違いがある可能性もあります。  
    見つけた場合には、[Xのアカウント](https://twitter.com/ra0kley/)などで教えていただけますと幸いです。

## ライセンスについて  
- 公開しているGeoJSON形式およびCSV形式のデータ: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- ソースコード: [MIT](https://opensource.org/license/mit/)

## 出典
以下の著作物を改変して利用しています。  
- 七尾市「[避難所一覧/開設中の避難所状況](https://www.city.nanao.lg.jp/bosai/mail/202401021200.html)」  
-  石川県「[指定緊急避難所一覧](https://www.pref.ishikawa.lg.jp/opendata/shakaikiban_index.html)」、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 
- 七尾市「[10_指定緊急避難所施設一覧](https://www.city.nanao.lg.jp/koho/shise/koho/opendata/index.html)」、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 
