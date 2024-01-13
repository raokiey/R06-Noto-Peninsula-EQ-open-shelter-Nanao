import os
import shutil
from datetime import datetime
from glob import glob
from typing import Tuple

import geopandas as gpd
import pandas as pd
import requests
from bs4 import BeautifulSoup
from thefuzz import process


def get_update_datetime(url: str) -> Tuple[str, str]:
    """データの更新日時を取得する

    Args:
        url (str): 七尾市の避難所一覧サイトのURL

    Returns:
        str: 更新日時をYYYYMMDDhhmm形式に変換した文字列
    """
    # Webページの内容を取得
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Webページのh1タグ部分に記載されているので更新日時にあたる箇所を抽出
    h1_tags = soup.find_all('h1')
    update_datetime_ja = h1_tags[0].get_text().split('（')[1].split('）')[0][:-2]

    # 令和6年以降の文字列を取得
    datetime_part = update_datetime_ja.split('年')[1]

    # 午前/午後の処理
    # 午後の場合は時間に12を加える
    if '午後' in datetime_part:
        hour = int(datetime_part.split('午後')[1].split('時')[0])
        if hour < 12:
            hour += 12
        datetime_part = datetime_part.split('日')[0] + '日' + str(hour) + '時'
    # 午前の場合は'午前'を取り除く
    else:
        datetime_part = datetime_part.replace('午前', '')
    datetime_str = f'2024年{datetime_part}'
    # YYYYmmddHHMM形式にフォーマット
    update_datetime = datetime.strptime(datetime_str, '%Y年%m月%d日%H時').strftime('%Y-%m-%d-%H%M')

    return update_datetime, update_datetime_ja


def merge_reference_data(matching_df: pd.DataFrame, update_datetime_ja: str) -> pd.DataFrame:
    """参照用データとマージし、緯度経度等の情報を付加する

    Args:
        matching_df (pd.DataFrame): マージ対象の開設中の避難所情報のDataFrame
        update_datetime_ja (str): 開設中の避難所情報を日本語で記載した文字列

    Returns:
        pd.DataFrame: 開設中の避難所情報と参照用データをマージしたDataFrame
    """
    # 参照用データを読み込む
    reference_df = pd.read_csv('./data/reference_data.csv')
    # Webサイト上の避難所名称と参照用データの避難所名称でマッチングを行う
    # 完全一致するケースは少ないので、レーベンシュタイン距離を用いて類似度を算出し、80以上のものを一致とみなす
    matching_df['マッチング用名称'] = matching_df['名称'].apply(lambda x: process.extractOne(x, reference_df['名称'])[0])
    matching_df['類似度'] = matching_df['名称'].apply(lambda x: process.extractOne(x, reference_df['名称'])[1])
    matching_df['source_order'] = list(range(0, len(matching_df)))

    match_df = matching_df[matching_df['類似度'] >= 80].reset_index(drop=True)
    non_match_df = matching_df[matching_df['類似度'] < 80].reset_index(drop=True)

    # 参照データにマッチングする内容がない場合の表示処理
    if len(non_match_df) > 0:
        for name in non_match_df['名称']:
            print(f'{name}の位置情報が取得できませんでした。')

    # Webサイト上の開設中の避難所情報と参照用データの情報をマージし、整理
    merged_df = pd.merge(match_df, reference_df, left_on='マッチング用名称', right_on='名称', how='left', suffixes=('', '_ref'))
    merged_df = merged_df.sort_values(by='source_order').reset_index(drop=True)

    export_df = merged_df[[
        'ID', '地区', '名称', '人数', '名称_カナ', '名称_英字', '町字ID', '所在地_連結表記', '所在地_都道府県',
        '所在地_市区町村', '所在地_町字', '所在地_番地以下', '建物名等(方書)', '緯度', '経度', '標高', '電話番号',
        '災害種別_洪水', '災害種別_崖崩れ、土石流及び地滑り', '災害種別_高潮', '災害種別_地震', '災害種別_津波',
        '災害種別_大規模な火事', '災害種別_内水氾濫', '災害種別_火山現象', '想定収容人数', '対象となる町会・自治会'
       ]]
    export_df = export_df.rename(columns={'人数': f'人数_{update_datetime_ja}時点'})

    return export_df


def convert_gis_data(export_df: pd.DataFrame, dst_epsg: int = 6668) -> gpd.GeoDataFrame:
    """_summary_

    Args:
        export_df (pd.DataFrame): X座標、Y座標の情報を含むDataFrame
        dst_epsg (int): 出力時のEPSGコード。デフォルトは6668

    Returns:
        gpd.GeoDataFrame: _description_
    """
    export_gdf = gpd.GeoDataFrame(
        export_df, geometry=gpd.points_from_xy(export_df['経度'], export_df['緯度']), crs="EPSG:6668"
    )

    if dst_epsg != 6668:
        export_gdf.to_crs(epsg=dst_epsg, inplace=True)

    return export_gdf


def main():
    # 七尾市の開設中避難所情報のURL
    open_shelter_url = 'https://www.city.nanao.lg.jp/bosai/mail/202401021200.html'

    # 更新日時を取得
    update_datetime, update_datetime_ja = get_update_datetime(open_shelter_url)

    # CSVのファイル名から更新日時が新しくなっているか確認
    current_csv_path = glob('./data/latest/open_shelter_Nanao-shi_*.csv')[0]
    current_update_datetime = os.path.basename(current_csv_path).split('_')[-1].split('.')[0]

    # 更新がある場合
    if update_datetime != current_update_datetime:
        # 現在`latest`にあるCSVファイルを`history`に移動
        _ = shutil.move(current_csv_path, './data/history/')

        # 上のページから開設中の避難所情報をDataFrame形式で取得
        raw_df = pd.read_html(open_shelter_url)
        open_shelter_df = raw_df[0].set_axis(['地区', '名称', '人数'], axis='columns')

        # 開設中の避難所情報と参照用データをマージ
        export_df = merge_reference_data(open_shelter_df, update_datetime_ja)

        # マージしたデータをGISデータに変換
        export_gdf = convert_gis_data(export_df, dst_epsg=6675)

        # 保存
        export_df.to_csv(f'./data/latest/open_shelter_Nanao-shi_{update_datetime}.csv', index=False)
        export_gdf.to_file('./data/latest/open_shelter_Nanao-shi.geojson')
        export_gdf.to_file('./data/latest/open_shelter_Nanao-shi.fgb', index=False, driver="FlatGeobuf", spatial_index="NO")

        print(f'{update_datetime}時点のデータに更新しました。')

    # 更新がない場合
    else:
        print('データの更新はありませんでした。')


if __name__ == "__main__":
    main()
