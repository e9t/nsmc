# Naver sentiment movie corpus v1.0

This is a movie review dataset in the Korean language.
Reviews were scraped from [Naver Movies](http://movie.naver.com/movie/point/af/list.nhn).

The dataset construction is based on the method noted in [Large movie review dataset](http://ai.stanford.edu/~amaas/data/sentiment/) from Maas et al., 2011.


## Data description

- Each file is consisted of three columns: `id`, `document`, `label`
    - `id`: The review id, provieded by Naver
    - `document`: The actual review
    - `label`: The sentiment class of the review. (0: negative, 1: positive)
    - Columns are delimited with tabs (i.e., `.tsv` format; but the file extension is `.txt` for easy access for novices)
- 200K reviews in total
    - `ratings.txt`: All 200K reviews
    - `ratings_test.txt`: 50K reviews held out for testing
    - `ratings_train.txt`: 150K reviews for training

## Characteristics

- All reviews are shorter than 140 characters
- Each sentiment class is sampled equally (i.e., random guess yields 50% accuracy)
    - 100K negative reviews (originally reviews of ratings 1-4)
    - 100K positive reviews (originally reviews of ratings 9-10)
    - Neutral reviews (originally reviews of ratings 5-8) are excluded

## Quick peek

    $ head ratings_train.txt
    id      document        label
    9976970 아 더빙.. 진짜 짜증나네요 목소리        0
    3819312 흠...포스터보고 초딩영화줄....오버연기조차 가볍지 않구나        1
    10265843        너무재밓었다그래서보는것을추천한다      0
    9045019 교도소 이야기구먼 ..솔직히 재미는 없다..평점 조정       0
    6483659 사이몬페그의 익살스런 연기가 돋보였던 영화!스파이더맨에서 늙어보이기만 했던 커스틴 던스트가 너무나도 이뻐보였다  1
    5403919 막 걸음마 뗀 3세부터 초등학교 1학년생인 8살용영화.ㅋㅋㅋ...별반개도 아까움.     0
    7797314 원작의 긴장감을 제대로 살려내지못했다.  0
    9443947 별 반개도 아깝다 욕나온다 이응경 길용우 연기생활이몇년인지..정말 발로해도 그것보단 낫겟다 납치.감금만반복반복..이드라마는 가족도없다 연기못하는사람만모엿네       0
    7156791 액션이 없는데도 재미 있는 몇안되는 영화 1

## License

<p xmlns:dct="http://purl.org/dc/terms/">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/">
    <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
  </a>
</p>
