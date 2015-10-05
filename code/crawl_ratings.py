#! /usr/bin/python3
# -*- coding: utf-8 -*-


from collections import defaultdict
from glob import glob
import os
import re
import time

from lxml import html
import numpy as np
import pandas as pd
import requests

import utils


BASEURL     = 'http://movie.naver.com/movie/point/af/list.nhn'
RATINGURL   = BASEURL + '?&page=%s'
MOVIEURL    = BASEURL + '?st=mcode&target=after&sword=%s&page=%s'

DATADIR     = 'data/ratings'
INDEXFILE   = 'index.txt'
TMPFILE     = 'data/ratings_all.txt'
RATINGSFILE = 'data/ratings.txt'
SEED        = 1234
SLEEP       = 600
NDOCS       = 200000


extract_nums = lambda s: re.search('\d+', s).group(0)
sanitize_str = lambda s: s.strip()


def parse_item(item):
    try:
        return {'review_id': item.xpath('./td[@class="ac num"]/text()')[0],     # num
                'rating': item.xpath('./td[@class="point"]/text()')[0],         # point
                'movie_id': extract_nums(item.xpath('./td[@class="title"]/a/@href')[0]),
                'review': sanitize_str(' '.join(item.xpath('./td[@class="title"]/text()'))),
                'author': item.xpath('./td[@class="num"]/a/text()')[0],
                'date': item.xpath('./td[@class="num"]/text()')[0]
        }
    except (IndexError, AttributeError) as e:
        print(e, item.xpath('.//text()'))
        return None
    except (AssertionError) as e:
        print(e, 'Sleep for %s' % SLEEP)
        time.sleep(SLEEP)
    except Exception as e:
        print(e, '음 여기까진 생각을 못했는데...')


def crawl_rating_page(url):
    resp = requests.get(url)
    root = html.fromstring(resp.text)
    items = root.xpath('//body//table[@class="list_netizen"]//tr')[1:]
    npages = max(map(int, ([0] + root.xpath('//div[@class="paging"]//a/span/text()'))))
    return list(filter(None, [parse_item(item) for item in items])), npages


def crawl_movie(movie_id):
    items = []
    for page_num in range(10):  # limit to 100 recent ratings per movie
        url = MOVIEURL % (movie_id, page_num + 1)
        page_items, npages = crawl_rating_page(url)
        items.extend(page_items)
        if len(items)==0:
            return []
        if page_num >= npages - 1:
            break
    if items:
        utils.write_json(items, '%s/%s.json' % (DATADIR, movie_id))
        return items
    else:
        return []


def get_index(filename):
    if os.path.exists(filename):
        movie_id, total = map(int, utils.read_txt(filename).split('\n')[0].split(','))
    else:
        movie_id, total = 129406, 0
    print(movie_id, total)
    return [movie_id, total]


def put_index(movie_id, total, filename):
    utils.write_txt('%s,%s' % (movie_id, total), filename)


def merge_ratings():

    def balance_classes(df, ndocs_per_class):
        df_pos = df[df['label']==1][:int(ndocs_per_class)]
        df_neg = df[df['label']==0][:int(ndocs_per_class)]
        return df_pos.append(df_neg)


    sub_space = lambda s: re.sub('\s+', ' ', s)
    write_row = lambda l, f: f.write('\t'.join(l) + '\n')

    filenames = glob('%s/*' % DATADIR)
    with open(TMPFILE, 'w') as f:
        write_row('id document label'.split(), f)
        for filename in filenames:
            for review in utils.read_json(filename):
                rating = int(review['rating'])
                if rating > 8:      # positive 9 10
                    write_row([review['review_id'], sub_space(review['review']), '1'], f)
                elif rating < 5:    # negative 1 2 3 4
                    write_row([review['review_id'], sub_space(review['review']), '0'], f)
                else:               # neutral
                    pass
    print('Ratings merged to %s' % TMPFILE)

    df = pd.read_csv(TMPFILE, sep='\t', quoting=3)
    df = df.fillna('')
    np.random.seed(SEED)
    df = df.iloc[np.random.permutation(len(df))]
    df = balance_classes(df, NDOCS/2)
    df.to_csv(RATINGSFILE, sep='\t', index=False)
    print('Ratings written to %s' % RATINGSFILE)


if __name__=='__main__':
    movie_id, total = get_index(INDEXFILE)
    while total < 1000000 and movie_id > 0:
        items = crawl_movie(movie_id)
        total += len(items)
        put_index(movie_id, total, INDEXFILE)
        print(MOVIEURL % (movie_id, 1), len(items), total)
        movie_id -= 1
    merge_ratings()
