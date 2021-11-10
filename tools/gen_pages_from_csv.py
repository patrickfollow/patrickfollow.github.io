# -*- coding: utf-8 -*-
# @Time    : 2021/11/10 10:21 AM
# @Author  : Patrick
# @Email   : patrickfollow@gmail.com
# @File    : gg.py
# @Software: metainfo.site
# @Description: gg

import os
from collections import OrderedDict
import pandas as pd

default_group = '未分类'
default_description = '暂无描述'
default_fontawesome = 'fas fa-tools'

data_dir = '../source/_data/'
config_template = '_config.webstack.template.yml'
config_target = '../_config.webstack.yml'


def load_settings(fn):
    pages_df = pd.read_excel(fn, sheet_name=0)
    group_df = pd.read_excel(fn, sheet_name=1)
    return pages_df, group_df


def get_icon(url):
    if not url.startswith('http'): url = 'http://' + url
    if url.endswith('/'): return '{}favicon.ico'.format(url)
    return '{}/favicon.ico'.format(url)


def get_page_settings(pages_df, group_df):
    pages = {}
    for i, row in pages_df.iterrows():
        if pd.isna(row['description']):
            row['description'] = default_description
        if pd.isna(row['group']):
            row['group'] = default_group
        if pd.isna(row['icon']):
            row['icon'] = get_icon(row['url'])

        if not row['group'] in pages: pages[row['group']] = []
        pages[row['group']].append(row.to_dict())
    return pages


def get_group_settings(pages, group_df):
    groups = OrderedDict()
    for i, row in group_df.iterrows():
        if pd.isna(row['group_name']): continue
        if pd.isna(row['FontAwesome']):
            row['FontAwesome'] = default_fontawesome
        groups[row['group_name']] = row.to_dict()
    pages_group = pages.keys()
    for group in pages_group:
        if not group in groups:
            groups[group] = {'FontAwesome': default_fontawesome}
    return groups


def write_pages(groupname, group_setting, pages):
    fn = os.path.join(data_dir, '{}.yml'.format(groupname))
    template = '''- name: {}\n  url: {}\n  img: {}\n  description: {}'''
    text = ''
    for page in pages:
        text += '\n' + template.format(page['name'], page['url'], page['icon'], page['description'])
    with open(fn, 'w') as f:
        f.write(text.strip())


def write_groups(groups):
    with open(config_template, 'r') as f:
        template = ''.join(f.readlines())
    menu = 'menu:\n'
    for k, v in groups.items():
        level = 1
        tab = ' ' * (level * 4 - 2)
        menu += '\n{tab}- name: {name}\n  {tab}icon: {icon}\n  {tab}config: {config}'.format(tab=tab, name=k, icon=v['FontAwesome'], config=k)
    text = template.replace('##menu##', menu.strip())
    with open(config_target, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    fn = 'page_list.xlsx'
    pages_df, group_df = load_settings(fn)

    pages = get_page_settings(pages_df, group_df)
    groups = get_group_settings(pages, group_df)

    for k, v in groups.items():
        write_pages(k, v, pages[k])

    write_groups(groups)
