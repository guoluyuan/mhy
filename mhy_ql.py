# @Author: 郭盖
# @FileName: spider.py
# @DateTime: 2022/8/17 15:56
# @SoftWare:  PyCharm
import datetime
import json
import multiprocessing
import sys
import time
import requests
import os


# 获取商品信息
def get_goods_info(goods_id):
    """
    :param goods_id: 商品id
    :return:左到右，依次，商品信息，商品开始兑换标志，商品类别
    """
    result = "获取信息失败检查ck"
    url = goods_info_url + goods_id
    res = requests.get(url=url, headers=headers).json()
    if (res['message'] == 'OK'):
        res = res['data']
        # print(res)
        # 商品id
        goodsid = res['goods_id']
        # 商品名
        goods_name = res['goods_name']
        # 商品类型type 1为实物，2为虚拟产品(不需要收货地址)
        goods_type = res['type']-1
        goods_type_list = ["实物", "虚拟产品"]
        # 兑换价格
        price = res['price']
        # 获取账户米游币余额
        accountInfo = str(get_account_info())
        # 库存
        next_num = res['next_num']
        # 当前时间
        now_time = custom_time(int(res['now_time']))
        # 商品最近一次兑换时间
        next_time = custom_time(int(res['next_time']))
        # 商品上架时间
        start_time = custom_time(int(res['start']))
        # 商品下架时间
        end_time = custom_time(int(res['end']))
        result = "商品id:" + goodsid + "\n" \
                 + "商品类型:" + goods_type_list[goods_type] + "\n" \
                 + "商品名:" + goods_name + "\n" \
                 + "库存:" + str(next_num) + "\n" \
                 + "商品兑换价格:" + str(price) + "米游币" + "\n" \
                 + "当前账户剩余米游币数:" + accountInfo + "米游币" "\n" \
                 + "当前时间:" + now_time + "\n" \
                 + "最近一次开放兑换时间:" + next_time + "\n" \
                 + "商品上架时间:" + start_time + "\n" \
                 + "商品下架时间:" + end_time + "\n"
    return result, now_time >= next_time, goods_type - 1


# 获取当前ck账户信息
def get_account_info():
    res = requests.get(url=user_account_info_url, headers=headers).json()
    if (res['message'] == 'OK'):
        return res['data']['points']
    else:
        return "获取个人信息失败，请重新获取ck"


# 获取地址代号，后面的兑换实物需要写在data中提交
def get_address_num():
    res = requests.get(url=address_url, headers=headers).json()
    res = res['data']['list'][0]
    address = ""
    address_id = ""
    for k, v in res.items():
        if (k in ['connect_name', 'connect_areacode', 'connect_mobile']):
            address += v
        if (k in ["province_name", "city_name", "county_name", "addr_ext"]):
            address += v
        if k == "id":
            address_id = v
    print(address, address_id)
    return address, address_id


# 时间戳(秒级)转时间
def custom_time(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def exchange_goods(goods_id, address_id, goods_type, uid=None):
    # 这里data[0]为实物提交数据，data[1]为虚拟产品提交数据
    data = [{
        "app_id": 1,
        "point_sn": "myb",
        "goods_id": goods_id,
        "exchange_num": 1,
        "address_id": address_id
    }, {
        "app_id": 1,
        "point_sn": "myb",
        "goods_id": goods_id,
        "exchange_num": 1,
        "uid": uid,
        "region": "cn_gf01",
        "game_biz": "hk4e_cn",
        "address_id": address_id
    }
    ]
    # print(data[goods_type])
    res = requests.post(url=exchange_goods_url, headers=headers, data=json.dumps(data[goods_type])).json()
    print(res)



if __name__ == '__main__':
    # 商品id
    # 使用ql面板时可使用，在环境变量中添加变量名mhy_duihuan
    # 每个值用@@隔开
    # 例子goods_id@@uid@@ck
    mhy_duihuan = os.getenv("mhy_duihuan")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if (mhy_duihuan != None):
        mhy_duihuan=mhy_duihuan.split("@@")
        goods_id = mhy_duihuan[0]
        # uid
        uid = mhy_duihuan[1]
        ck = mhy_duihuan[2]
    else:
        print("无环境变量，确认当前环境不是青龙面板开始使用自定义值")
        print("开始使用脚本内置变量")
        #必填3个参数，需要米游设抓包
        goods_id=""
        uid = ""
        ck = ""
    if(goods_id=="" or uid=="" or ck==""):
        print("当前未填写内置所需变量值，退出")
        sys.exit()
    # cookie
    print(goods_id,uid,ck)
    # ck = "_MHYUUID=7b208f19-3aa0-4420-86b1-f060aa1be54a; aliyungf_tc=86cceb6836e54dfecd96d118de72543fc8651f5414755e93393db0d793e419d0; mi18nLang=zh-cn; _ga_6ZKT513CTT=GS1.1.1647679149.1.1.1647679185.0; ltuid=188025722; login_ticket=VkVgE5LrxICLRm4DkA2ewGqZNVLrzdCUwlavUuKe; account_id=188025722; ltoken=LLNoWKt34Jtor9Nih5QusurhEovjxw5xk0o0NSEZ; cookie_token=GjTvb04kwDqlpe3kqXnxs9sMbT27BZGV2SzkMgNX; _ga_55SMHPM22L=GS1.1.1651403544.2.1.1651403833.0; _ga_BL22GL4FMD=GS1.1.1655246522.1.1.1655246564.0; UM_distinctid=181f12b096a10f-07e1b54c3bedc6-33194b23-53c31-181f12b096bed; _ga_9TTX3TE5YL=GS1.1.1658063713.3.1.1658063772.0; _ga_QYFFEX7F52=GS1.1.1659728618.5.1.1659728692.0; _ga_KJ6J9V9VZQ=GS1.1.1659932873.4.0.1659932878.0; _gid=GA1.2.97596165.1660601318; _ga=GA1.2.2046901947.1647246637; _ga_CXN1FSHKS4=GS1.1.1660663332.2.0.1660663347.0"
    # 商品信息api
    goods_info_url = "https://api-takumi.mihoyo.com/mall/v1/web/goods/detail?app_id=1&point_sn=myb&goods_id="
    # 个人信息api（账户的米游币余额）
    user_account_info_url = "https://api-takumi.mihoyo.com/common/homutreasure/v1/web/user/point?app_id=1&point_sn=myb"
    # 兑换api
    exchange_goods_url = "https://api-takumi.mihoyo.com/mall/v1/web/goods/exchange"
    # 收货信息api，兑换实物需要用到
    address_url = "https://api-takumi.mihoyo.com/account/address/list?point_sn=myb"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.5005.78 Mobile Safari/537.36 miHoYoBBS/2.31.1",
        "cookie": ck,
        "X-Requested-With": "com.mihoyo.hyperion",
        "Origin": "https://webstatic.mihoyo.com",
    }
    adress, adress_id = get_address_num()
    # 获取商品信息
    # saleflage表示当前是否开始售卖
    goodInfo, saleflage, goods_type = get_goods_info(goods_id)
    print(goodInfo)
    # 开启线程池开始兑换
    time1 = time.perf_counter()
    #线程数
    pool = multiprocessing.Pool(10)
    #一共跑几次
    task_number = 200
    for i in range(task_number):
        pool.apply_async(func=exchange_goods, args=(goods_id, adress_id, goods_type, uid))
    pool.close()
    pool.join()
    time2 = time.perf_counter()
    times = time2 - time1
    print(times / task_number)  # 每次请求用时
