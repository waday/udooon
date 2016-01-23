#coding: utf-8
pref_dict = {
    "北海":"hokkaido",
    "青森":"aomori",
    "岩手":"iwate",
    "宮城":"miyagi",
    "秋田":"akita",
    "山形":"yamagata",
    "福島":"fukushima",
    "茨城":"ibaraki",
    "栃木":"tochigi",
    "群馬":"gunma",
    "埼玉":"saitama",
    "千葉":"chiba",
    "東京":"tokyo",
    "神奈川":"kanagawa",
    "新潟":"niigata",
    "富山":"toyama",
    "石川":"ishikawa",
    "福井":"fukui",
    "山梨":"yamanashi",
    "長野":"nagano",
    "岐阜":"gifu",
    "静岡":"shizuoka",
    "愛知":"aichi",
    "三重":"mie",
    "滋賀":"shiga",
    "京都":"kyoto",
    "大阪":"osaka",
    "兵庫":"hyogo",
    "奈良":"nara",
    "和歌山":"wakayama",
    "鳥取":"tottori",
    "島根":"shimane",
    "岡山":"okayama",
    "広島":"hiroshima",
    "山口":"yamaguchi",
    "徳島":"tokushima",
    "香川":"kagawa",
    "愛媛":"ehime",
    "高知":"kochi",
    "福岡":"fukuoka",
    "佐賀":"saga",
    "長崎":"nagasaki",
    "熊本":"kumamoto",
    "大分":"oita",
    "宮崎":"miyazaki",
    "鹿児島":"kagoshima",
    "沖縄":"okinawa"
}

city_code_dict = {
    '東かがわ市': 'C37207',
    '綾歌郡宇多津町': 'C37386',
    '仲多度郡琴平町': 'C37403',
    '小豆島': 'C3705',
    'さぬき・東かがわ': 'C3704',
    'さぬき市': 'C37206',
    '観音寺・琴平周辺': 'C3703',
    '坂出市': 'C37203',
    '善通寺市': 'C37204',
    '丸亀市': 'C37202',
    '仲多度郡まんのう町': 'C37406',
    '木田郡三木町': 'C37341',
    '坂出・丸亀・塩飽諸島': 'C3702',
    '小豆郡小豆島町': 'C37324',
    '小豆郡土庄町': 'C37322',
    '綾歌郡綾川町': 'C37387',
    '高松': 'C3701',
    '高松市': 'C37201',
    '観音寺市': 'C37205',
    '仲多度郡多度津町': 'C37404',
    '三豊市': 'C37208'
}

def pref_kanji2roma(kanji):
    return pref_dict.get(kanji, None)

def city_kanji2code(city):
    city_code = city_code_dict.get(city, None)
    if city_code is None:
        for suffix in '市 区 町 村'.split():
            city_code = city_code_dict.get(city + suffix, None)
            if city_code is not None:
                break
    return city_code

if __name__ == '__main__':
    import udooonlib as udnlib
    print("> udnlib.pref_kanji2roma")
    print("香川ken:")
    romaji = udnlib.pref_kanji2roma("香川ken")
    print(romaji)
    print("香川:")
    romaji = udnlib.pref_kanji2roma("香川")
    print(romaji)
    print("--------------------------")
    print("> udnlib.city_kanji2code")
    print("さぬき:")
    city_code = udnlib.city_kanji2code("さぬき")
    print(city_code)

