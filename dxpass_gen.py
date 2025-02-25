import argparse
import logging
import os
import math
from datetime import datetime


import colorsys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
import json
import re
import random
import time

RES_PATH = os.path.join(os.path.dirname(__file__), "res")
FONT_PATH = os.path.join(RES_PATH, "fonts", "SEGA_MARUGOTHICDB.ttf")
JSON_PATH = os.path.join(RES_PATH, "MAI", "Data")
CN_FONT_PATH = os.path.join(RES_PATH, "fonts", "zh_cn.ttf")
DEF_VAL = 15  # 默认有效期为15天
logging.basicConfig(level=logging.INFO)


def call_pass_pic(rating=15000, friendcode=123456789, qr=None, cardchara="000602",bgnum="None", charaname="avatar", datets="1740323711", aime="12345678912345678912", virsion="1.00-0001", nickname="maimai", dxtype="freedom"): 
    img = Image.new("RGBA", (768, 1052), color=(0, 0, 0, 0))
    """charadata"""
    if os.path.exists(os.path.join(JSON_PATH, "A000", "cardChara", f"cardChara0{cardchara}.json")): 
        with open(os.path.join(JSON_PATH, "A000", "cardChara", f"cardChara0{cardchara}.json"), "r", encoding="utf-8") as f: 
            chara_data = json.load(f)
            charaname = chara_data["CardCharaData"]["name"]["str"]
            logging.info(f"找到以下对应角色: {charaname}")
    else:  
        return logging.error(f"未找到对应角色，请检查角色ID是否正确")
    """bg"""
    base_id = str(chara_data["CardCharaData"]["mapId"]["id"]).zfill(6)
    cardbase_path = os.path.join(RES_PATH, "cardbase")
    base_files = [f for f in os.listdir(cardbase_path) if re.match(
        f"UI_CardBase_.*_{base_id}\\.png", f)]  # 使用正则匹配角色背景
    logging.info(f"找到以下对应角色的背景: {base_files}")
    if base_files: 
        if not bgnum:
            base_file = random.choice(base_files)
            logging.info(f"即将随机选择: {base_file}")
        else:
            base_file = base_files[bgnum-1]
            logging.info(f"即将选择第{bgnum}个: {base_file}")
        base_img = Image.open(os.path.join(cardbase_path, base_file))
        img.paste(base_img, (0, 0), base_img)

    """chara"""
    cardchara_mask = Image.open(os.path.join(
        RES_PATH, "charapic", f"UI_CardCharaMask_{cardchara}.png"))
    cardchara_img = Image.open(os.path.join(
        RES_PATH, "charapic", f"UI_CardChara_{cardchara}.png"))
    img.paste(cardchara_mask, (0, 0), cardchara_mask)
    img.paste(cardchara_img, (0, 0), cardchara_img)

    """type"""
    type_bg = Image.open(os.path.join(RES_PATH, "type", f"{dxtype}.png"))
    img.paste(type_bg, (0, 0), type_bg)
    """static"""
    chara_name_bg = Image.open(os.path.join(
        RES_PATH, "static", "chara_name_bg.png"))
    nickname_bg = Image.open(os.path.join(
        RES_PATH, "static", "nickname_bg.png"))
    number_bg = Image.open(os.path.join(RES_PATH, "static", "number_bg.png"))
    img.paste(chara_name_bg, (0, 797), chara_name_bg)
    img.paste(nickname_bg, (462, 110), nickname_bg)
    img.paste(number_bg, (140, 999), number_bg)

    """optional"""
    if friendcode: 
        logging.info(f"玩家好友码为: {friendcode}")
        frend_bg = Image.open(os.path.join(RES_PATH, "static", "frend_bg.png"))
        img.paste(frend_bg, (460, 149), frend_bg)
        # 好友码
        font = ImageFont.truetype(FONT_PATH, 18)
        draw = ImageDraw.Draw(img)
        text_bbox = draw.textbbox((0, 0), str(friendcode), font=font)
        text_width = text_bbox[2] - text_bbox[0]
        x_position = 531 + (728 - 531 - text_width) // 2
        draw.text((x_position, 156), str(friendcode),
                  font=font, fill=(0, 0, 0, 255))

    """text"""
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 21)
    date = datetime.fromtimestamp(
        datets + DEF_VAL * 24 * 60 * 60).strftime("%Y/%m/%d")
    logging.info(f"dxpass有效期至: {date}")
    draw.text((152, 837), str(date), font=font, fill=(101, 68, 5, 255))

    font = ImageFont.truetype(FONT_PATH, 17)
    draw.text((41, 839), "ブ一スト期限", font=font, fill=(101, 68, 5, 255))
    # 角色名
    text_bbox = draw.textbbox((0, 0), charaname, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    offset = 10  # 设置居中偏移
    x_position = offset + (258 - text_width) // 2
    draw.text((x_position, 810), charaname, font=font, fill=(101, 68, 5, 255))
    # 卡号及版本
    logging.info(f"玩家aime卡号为: {aime}")
    formatted_aime = " ".join(aime[i: i+4]
                              for i in range(0, len(aime), 4))  # 卡号间加入空格
    formatted_virsion = "[maimaiDX]"+virsion
    logging.info(f"版本号为: {formatted_virsion}")
    formatted_all = formatted_aime + "    " + formatted_virsion
    draw.text((156, 1005), formatted_all, font=font, fill=(255, 255, 255, 255))
    # 昵称
    logging.info(f"玩家昵称为: {nickname}")
    font = ImageFont.truetype(CN_FONT_PATH, 33.3)
    text_bbox = draw.textbbox((0, 0), nickname, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    x_position = 464 + (625 - 464 - text_width) // 2
    draw.text((x_position, 114), nickname, font=font, fill=(0, 0, 0, 255))

    # rating
    """bg"""
    rt_bg = Image.open(os.path.join(
        RES_PATH, "rating", "UI_CMN_DXRating_11.png"))
    dxrts = [0, 1000, 2000, 4000, 7000, 10000,
             12000, 13000, 14000, 14500, 15000]
    for i, dxrt in enumerate(dxrts): 
        if rating < dxrt: 
            rt_bg = Image.open(os.path.join(
                RES_PATH, "rating", f"UI_CMN_DXRating_{i}.png"))
            rt_bg.resize((268, rt_bg.height))
            break
    img.paste(rt_bg, (462, 34), rt_bg)
    """num"""
    logging.info(f"玩家dxrating为: {rating}")
    rating_list = [int(digit) for digit in str(rating)]
    num0 = 5 - len(rating_list)
    num_x = [574, 603, 632, 661, 689]
    i = 0
    num_y = 54
    num = Image.open(os.path.join(RES_PATH, "number", "UI_NUM_Drating_0.png"))
    num = num.resize((int(num.width * 0.95), int(num.height * 0.95)))
    for _ in range(num0): 
        img.paste(num, (num_x[i], num_y), num)
        i += 1
    for digit in rating_list: 
        num = Image.open(os.path.join(RES_PATH, "number",
                                      f"UI_NUM_Drating_{digit}.png"))
        num = num.resize((int(num.width * 0.95), int(num.height * 0.95)))
        img.paste(num, (num_x[i], num_y), num)
        i += 1

    # qrcode
    qr_bg = Image.open(os.path.join(RES_PATH, "qrcode", "qr_bg.png"))
    img.paste(qr_bg, (556, 841), qr_bg)
    qr_img = Image.open(os.path.join(RES_PATH, "qrcode", "default.png"))
    # 可选生成二维码
    if qr: 
        logging.info(f"二维码内容为: {qr}")
        qr_code = qrcode.QRCode(border=2)  # 边框宽度
        qr_code.add_data(str(qr))
        qr_code.make(fit=True)
        qr_img = qr_code.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((130, 130))
        img.paste(qr_img, (569, 854))
    else: 
        logging.info(f"未指定二维码值，使用默认迪拉熊二维码")
        img.paste(qr_img, (573, 857), qr_img)

    
    return img


# current_timestamp = datetime.now().timestamp()
# call_pass_pic(rating=15001, qr=114514, datets=current_timestamp)


def main(): 
    if os.path.exists(os.path.join(RES_PATH, "res.json")): 
        with open(os.path.join(RES_PATH, "res.json"), "r", encoding="utf-8") as f: 
            res_data = json.load(f)
            logging.info(f"资源文件夹加载成功，资源版本: {res_data["version"]}")
    else: 
        return logging.error(f"资源文件夹加载失败，请检查资源文件夹是否存在")
        
    parser = argparse.ArgumentParser(description="基于Python的dxpass生成器", formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
    parser.add_argument("--rating", type=int, default=15121, help="玩家dxrating")
    parser.add_argument("--friendcode", type=int, default=123456789, help="玩家好友码")
    parser.add_argument("--qr", type=str, default=None, help="根据字符串生成右下角二维码，留空则使用默认值")
    parser.add_argument("--cardchara", type=str, default="000601", help="dxpass人物ID")
    parser.add_argument("--bgnum", type=int, default=None, help="指定背景列表中的背景")
    parser.add_argument("--datets", type=int, default=1740323711, help="当前的时间戳，以生成dxpass有效期")
    parser.add_argument("--aime", type=str, default="12345678912345678912", help="下方的aime卡号，要求20位")
    parser.add_argument("--virsion", type=str, default="1.00-0001", help="下方的版本号，请按默认的格式填写")
    parser.add_argument("--nickname", type=str, default="maimai", help="玩家昵称，支持中文")
    parser.add_argument("--dxtype", type=str, default="freedom", help="dxpass类型")
    parser.add_argument("--output", type=str, default="./output.png", help="图片输出路径")
    args = parser.parse_args()  
    start_time = time.time()
    d = call_pass_pic(rating=args.rating, friendcode=args.friendcode, qr=args.qr, cardchara=args.cardchara, bgnum=args.bgnum,datets=args.datets, aime=args.aime, virsion=args.virsion, nickname=args.nickname, dxtype=args.dxtype)
    if d:
        d.save(args.output)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"生成成功，已保存至{args.output}，耗时{elapsed_time:.2f}秒")
    else:
        logging.error(f"生成失败")

if __name__ == "__main__": 
    main()
