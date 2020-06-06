#!/bin/bash
set +x

download_category=false  ## 如果为 true, 就需要指定 catetory 的 url; 否则需要指定文章的 url

category_url='https://blog.csdn.net/<sp>/category_123.html'
# article_url='https://blog.csdn.net/<sp>/article/details/123456789'
article_url='https://blog.csdn.net/hbuxiaofei/article/details/106568805'

start_page=1
page_num=100
markdown_dir='markdown'
pdf_dir='pdf'

if ${download_category}; then
    python3 -u main.py \
        --category_url ${category_url} \
        --start_page ${start_page} \
        --page_num ${page_num} \
        --markdown_dir ${markdown_dir} \
        --combine_together \
        # --to_pdf \
        # --pdf_dir ${pdf_dir} \
        # --with_title \
        # --rm_cache \ ## dangerous option, remove all caches
else
    python3 -u main.py \
        --article_url ${article_url} \
        --markdown_dir ${markdown_dir} \
        # --to_pdf \
        # --pdf_dir ${pdf_dir} \
        # --with_title \
        # --rm_cache \ ## dangerous option, remove all caches
        # --combine_together \
fi
