import re
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'django_fptree_recommend.settings')  # mysite用的是自己的project
import django

django.setup()
from store.models import Product


def read_rules():
    rules_data = []
    with open("log/rules.txt") as f:
        for line in f.readlines():
            rule = re.findall(r"\d+\.?\d*", line)
            rules_data.append(rule[2:])
    return rules_data


def predict(product_id, num):
    '''
    product_id : 传入商品id,以此为用户推荐
    num : 推荐商品的数量
    '''
    rule_list = []
    rules_data = read_rules()
    for rule in rules_data:
        if product_id in rule:
            rule.remove(product_id)  # 去掉规则中的 product_id
            rule_list.append(rule)
    data = [i for item in rule_list for i in item]  # 所有包含 product_id 的规则
    # 此处，想要去重，又不想打乱data的次序，因此引入一个字典类型
    result = {}
    for i in data:
        if i not in result:
            result[i] = 1
        if i in result:
            result[i] += 1
    result_list = list(result.keys())
    # print(result_list)
    if len(result_list) < num:  # 推荐的产品数量可能不够num的标准，增加  。。。。
        product_id = int(product_id)
        product = Product.objects.all().filter(id=product_id).values()
        department = product[0]['p_department']
        # 找到和商品同种类的产品，按照热度，从高到低推荐
        product_list = Product.objects.all().filter(p_department=department).order_by("-p_total_views").values()
        product_id_list = []
        for i in product_list:
            if str(i['id']) in result_list:
                continue
            else:
                product_id_list.append(i['id'])
        # print(product_id_list)
        shengyu_num = num - len(result_list)
        # 如果同类产品数量不够，就把所有产品中热度最高的推荐出去
        if len(product_id_list) < shengyu_num:
            product2 = Product.objects.all().order_by("-p_total_views").values()
            product_id_list2 = []
            # 防止热度最高的产品已经存在推荐的列表中
            for i in product2:
                if (str(i['id']) in product_id_list) or (str(i['id']) in result_list):
                    continue
                else:
                    product_id_list2.append(i['id'])
                if len(product_id_list2) == shengyu_num - len(product_id_list):
                    break
            for i in product_id_list2:
                product_id_list.append(i)
        # shengyu_result = random.sample(product_id_list, shengyu_num)
        shengyu_result = product_id_list[0:shengyu_num]
        for i in shengyu_result:
            result_list.append(i)
        return result_list
    else:
        return result_list[:num]


if __name__ == "__main__":
    product_id = "1"
    num = 8
    result = predict(product_id, num)
    print(result)  # [39854, 32945, 12758, 11017, 2815, 23533, 1245, 26639]
    recItems = []
    for res in result:
        p = Product.objects.all().get(id=int(res))
        recItems.append(p)
    print(recItems)