# 令和6年能登半島地震 石川県七尾市避難所開設情報GISデータ

## 概要
このリポジトリでは、令和6年能登半島地震に関連して石川県七尾市のWebサイトにて公開されていた[開設中の避難所情報](https://www.city.nanao.lg.jp/bosai/mail/202401021200.html)を石川県および七尾市が公開しているオープンデータをもとに位置情報などを付加して、GISデータ化したデータを公開しています。  
~データ作成処理の定期実行（3時間毎）により、七尾市のWebサイト更新があった際に最新情報に更新される見込みです。~  
2024年9月8日正午に、石川県七尾市に開設されていた避難所が全て閉鎖されたため、データ作成処理の定期実行機能を停止いたしました。  

以下のリンクより、最新のデータにアクセス可能です。  
※ 最新のデータは、2024年9月2日午後6時時点のデータが最後です。  
- GeoJSON形式  
[https://raokiey.github.io/R06-Noto-Peninsula-EQ-open-shelter-Nanao/data/latest/open_shelter_Nanao-shi.geojson](https://raokiey.github.io/R06-Noto-Peninsula-EQ-open-shelter-Nanao/data/latest/open_shelter_Nanao-shi.geojson)  

- FlatGeobuf形式  
[https://raokiey.github.io/R06-Noto-Peninsula-EQ-open-shelter-Nanao/data/latest/open_shelter_Nanao-shi.fgb](https://raokiey.github.io/R06-Noto-Peninsula-EQ-open-shelter-Nanao/data/latest/open_shelter_Nanao-shi.fgb)


また、[`./data/latest/`](https://github.com/raokiey/R06-Noto-Peninsula-EQ-open-shelter-Nanao/tree/main/data/latest/) にCSV形式のデータも公開しています。 
過去のデータを利用したい方は、[`./data/history/`](https://github.com/raokiey/R06-Noto-Peninsula-EQ-open-shelter-Nanao/tree/main/data/history/) にCSV形式のデータのみですが、保存しています。  
※ 公開当初は、2024年1月9日18時時点のデータのみを格納しています。  

## 更新情報
- 2024/01/13 16:10
    - 列名に関して、データを扱いやすいように変更いたしました。  
        + 人数_令和6年MM月YY日時点 → 人数  
        + 上の変更に伴い、「時点」を新しく列に付け加えました。  
    - 「名称_カナ」、「名称_英字」が七尾市のWebサイトにて公開されている開設中の避難所名称と対応関係がないため、削除しました。  
- 2024/06/23 16:15  
    - 七尾市のサイトに記載されている福祉避難所が指定緊急避難所のオープンデータに記載がなく反映されていなかったため、手動で追加しました。  
- 2024/06/23 16:50  
    - 石川県のオープンデータカタログサイトが新しくなったため、石川県および七尾市が公開していた「指定緊急避難所一覧」のURLおよびクレジット表記を更新
- 2024/09/10 05:20
    - 石川県七尾市に開設されていた避難所が全て閉鎖されたため、データ作成処理の定期実行機能を停止いたしました。

## 注意事項
- 避難所によっては集計時間が異なることがあります。（七尾市Webサイトより）  
- 個人が作成したものです。注意はしていますが間違いがある可能性もあります。  
    見つけた場合には、[Xのアカウント](https://twitter.com/ra0kley/)などへ教えていただけますと幸いです。

## ライセンスについて  
- 公開しているGeoJSON形式およびFlatGeobuf形式、CSV形式のデータ: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- ソースコード: [MIT](https://opensource.org/license/mit/)

## 出典
以下の著作物を改変して利用しています。  
- 七尾市「[避難所一覧/開設中の避難所状況](https://www.city.nanao.lg.jp/bosai/mail/202401021200.html)」  
- 七尾市「[指定福祉避難所](https://www.city.nanao.lg.jp/bosai/kurashi/bosai/hinan/documents/r040701_fukushihinanjo.pdf)」  
-  「[石川県指定緊急避難所一覧](https://ishikawa-datapf.jp/ckan/dataset/170003_evacuation_space)」（石川県）を加工して作成
- 「[七尾市指定緊急避難所施設一覧](https://ishikawa-datapf.jp/ckan/dataset/172022_evacuation_space)」（石川県）を加工して作成    
