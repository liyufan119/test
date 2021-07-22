import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
import re

worktime = pd.read_csv('_SELECT_e_DeliveryTime_e_PickEmpName_sumPickQty_sku_count_sum_re_202104211136.csv')
worktime['DeliveryTime'] = pd.to_datetime(worktime['DeliveryTime']).dt.normalize()
picking_product = pd.read_csv('pick_product.csv')


def list_str_to_float(name):
    return list(map(float, name))


def getWeight(product_name, sale_unit_qty, sale_stock_qty):
    weight = 0
    product_name = product_name.split(' 适合')[0]
    productList = product_name.split(' ')
    product_name = ''
    for i in range(2, len(productList)):
        product_name = product_name + productList[i]

    if 'kg' in product_name:
        reg = re.findall(r'\d+\.?\d*(?=kg)', product_name)
        if len(reg) > 0:
            reg = list_str_to_float(reg)
            weight = float(np.max(reg)) * 2
    elif 'KG' in product_name:
        reg = re.findall(r'\d+\.?\d*(?=kg)', product_name)
        if len(reg) > 0:
            reg = list_str_to_float(reg)
            weight = float(np.max(reg)) * 2
    elif '公斤' in product_name:
        reg = re.findall(r'\d+\.?\d*(?=公斤)', product_name)
        if len(reg) > 0:
            reg = list_str_to_float(reg)
            weight = float(np.max(reg)) * 2
    elif 'ml' in product_name:
        reg = re.findall(r'\d+\.?\d*(?=ml)', product_name)
        if len(reg) > 0:
            reg = list_str_to_float(reg)
            weight = float(np.max(reg)) / 500
    elif '斤' in product_name:
        reg = re.findall(r'\d+\.?\d*(?=斤)', product_name)
        if len(reg) > 0:
            reg = list_str_to_float(reg)
            weight = float(np.max(reg))
    elif 'g' in product_name:
        reg = re.findall(r'\d+\.?\d*(?=g)', product_name)
        if len(reg) > 0:
            reg = list_str_to_float(reg)
            weight = float(np.max(reg)) / 500
    elif 'L' in product_name:
        reg = re.findall(r'\d+\.?\d*(?=L)', product_name)
        if len(reg) > 0:
            reg = list_str_to_float(reg)
            weight = float(np.max(reg)) * 2
    weight = weight * sale_unit_qty * sale_stock_qty
    return weight




picking_product['weight'] = picking_product.apply(
    lambda picking_product: getWeight(picking_product['product_name'],
                                              picking_product['sale_unit_qty'], picking_product['sale_stock_qty']),
    axis=1)
print(picking_product.loc[picking_product.weight==0])
print(picking_product.describe())
print(picking_product.head())
print(picking_product.loc[picking_product.sku==1228646])
