import pandas as pd
import os
import json
import math

csv_data = pd.read_csv('data/proc.csv')
with open('data/conf-meta.json', "r", encoding="utf-8") as f:
    conf_meta = json.load(f)

print(conf_meta)

conf_id   = conf_meta["conf_id"]
conf_name = conf_meta["conf_name"] + "（" + conf_id + "）"
conf_url  = conf_meta["conf_url"]

start_date = conf_meta["start_date"] # yyyy, mm, dd
end_date   = conf_meta["end_date"] # yyyy, mm, dd (if one-day conference, keep empty)

venue_city_en = conf_meta["venue_city"]["en"]
venue_city_ja = conf_meta["venue_city"]["ja"]
conf_place_en = conf_meta["venue_place"]["en"] + ", " + venue_city_en
conf_place_ja = conf_meta["venue_place"]["ja"] + "（" + venue_city_ja + "）"

conjunction_conf_name = conf_meta["conjunction_conf"]["name"]
conjunction_conf_url = conf_meta["conjunction_conf"]["url"]

proceedings_urls = conf_meta["proceedings_urls"]

# do not change
issued_date = "/".join(start_date)
conf_month = ".".join(start_date[:2])
conf_date_ja = start_date[0] + "年" + start_date[1] + "月" + start_date[2] + "日" + ("〜" + end_date[1] + "月" + end_date[2] + "日" if len(end_date) > 2 else "")
pdf_url = "https://sig-bti.github.io/" + start_date[0] + start_date[1] + "/pdf/{proc_id}.pdf"

category_list = {
  "oral": "口頭発表（Oral Session）",
  "posterdemo": "ポスター・デモ発表（Poster/Demo Sesssion）"
}

def gen_paper_page_html(proc_id, author, title, category, start_page, end_page):
  html = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="DC.title" content="{title}"></meta>
  <meta name="citation_title" content="{title}"></meta>
  <meta name="DC.language" content="JA"></meta>{dc_creator}
  <meta name="citation_publication_date" content="{issued_date}"></meta>
  <meta name="DC.issued" content="{issued_date}"></meta>
  <meta name="citation_conference_title" content="{conf_name}"></meta>
  <meta name="DC.relation.ispartof" content="{conf_name}"></meta>
  <meta name="citation_firstpage" content="{start_page}"></meta>
  <meta name="DC.citation.spage" content="{start_page}"></meta>
  <meta name="citation_lastpage" content="{end_page}"></meta>
  <meta name="DC.citation.epage" content="{end_page}"></meta>
  <meta name="citation_pdf_url" content="{pdf_url}"></meta>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@100..900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../../style.css">
</head>
<body>
  <header>
    <h1>SIG-BTI DIGITAL LIBRARY</h1>
    <h2>Academy of Behavior Transformation by AIoT / AIoT行動変容学会（BTI）</h2>
  </header>
  <div class="main">
    <ul class="breadcrumb clearfix">
      <li><a href="../../../">Top</a></li>
      <li><a href="../../">{conf_id}</a></li>
      <li>{proc_id}</li>
    </ul>
    <h1><a href="{pdf_url}">{title}</a></h1>
    <dl class="proceedings-meta">
      <dt>Title</dt><dd>{title}</dd>
      <dt>Author</dt><dd>{author}</dd>
      <dt>Pages</dt><dd>{start_page}-{end_page}</dd>
      <dt>Abstract</dt><dd></dd>
      <dt>Conference</dt><dd><a href="../../">{conf_name}</a></dd>
      <dt>Paper ID</dt><dd>{proc_id}</dd>
      <dt>Category</dt><dd>{category}</dd>
      <dt>PDF URL</dt><dd><a href="{pdf_url}">{pdf_url}</a></dd>
    </dl>
  </div>
  <footer>
    <a href="http://www.sig-bti.jp/">
      AIoT行動変容学会（BTI）<br>
      Academy of Behavior Transformation by AIoT
      <small>http://www.sig-bti.jp/</small>
    </a>
  </footer>
</body>
</html>'''.format(conf_id = conf_id,
                  proc_id = proc_id,
                  title = title,
                  author = ", ".join(author),
                  dc_creator = gen_dc_creator(author),
                  issued_date = issued_date,
                  conf_name = conf_name,
                  start_page = start_page,
                  end_page = end_page,
                  category = category_list[category],
                  pdf_url = pdf_url.format(proc_id = proc_id))
  return html

def gen_dc_creator(author):
  s = ""
  for a in author:
    s += '''
    <meta name=\"DC.creator\" content=\"{author}\"></meta>
    <meta name=\"citation_author\" content=\"{author}\"></meta>'''.format(author = a)
  return s


def gen_index_page_html():
  html = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{conf_id} Proceedings | Academy of Behavior Transformation by AIoT (BTI)</title>
  <meta name="DC.title" content="{conf_id} Proceedings | Academy of Behavior Transformation by AIoT (BTI)"></meta>
  <meta name="citation_title" content="{conf_id} Proceedings | Academy of Behavior Transformation by AIoT (BTI)"></meta>
  <meta name="DC.language" content="JA"></meta>
  <meta name="citation_publication_date" content="{issued_date}"></meta>
  <meta name="DC.issued" content="{issued_date}"></meta>
  <meta name="citation_conference_title" content="{conf_name}"></meta>
  <meta name="DC.relation.ispartof" content="{conf_name}"></meta>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@100..900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header>
    <h1>SIG-BTI DIGITAL LIBRARY</h1>
    <h2>Academy of Behavior Transformation by AIoT / AIoT行動変容学会（BTI）</h2>
  </header>
  <div class="main">
    <ul class="breadcrumb clearfix">
      <li><a href="../">Top</a></li>
      <li>{conf_id}</li>
    </ul>
    <h1>{conf_id} in {venue_city_en} ({conf_month})</h1>
    <dl class="conf-meta clearfix">
      <dt>名称</dt><dd>{conf_name}</dd>
      {conjunction_conf_info}
      <dt>日程</dt><dd>{conf_date_ja}</dd>
      <dt>会場</dt><dd>{conf_place_ja}</dd>
                  <dd>{conf_place_en}</dd>
      <dt>URL</dt><dd><a href="{conf_url}">{conf_url}</a></dd>
    </dl>
    {proceedings_pdf_list}
    {oral_session_list}
    {posterdemo_session_list}
  </div>
  <footer>
    <a href="http://www.sig-bti.jp/">
      AIoT行動変容学会（BTI）<br>
      Academy of Behavior Transformation by AIoT
      <small>http://www.sig-bti.jp/</small>
    </a>
  </footer>
</body>
</html>'''.format(conf_id = conf_id,
                  venue_city_en = venue_city_en,
                  conf_place_ja = conf_place_ja,
                  conf_place_en = conf_place_en,
                  conf_month = conf_month,
                  conf_date_ja = conf_date_ja,
                  conf_name = conf_name,
                  conf_url = conf_url,
                  issued_date = issued_date,
                  conjunction_conf_info = get_conjunction_conf_info(),
                  proceedings_pdf_list = gen_proceedings_pdf_list(),
                  oral_session_list = gen_paper_list("oral"),
                  posterdemo_session_list = gen_paper_list("posterdemo"))
  return html

def get_conjunction_conf_info():

  html = ""

  if conjunction_conf_name != "" and conjunction_conf_url != "":
    html = "<dt>連携学会</dt><dd><a href=\"" + conjunction_conf_url + "\">" + conjunction_conf_name + "</a></dd>"

  return html 

def gen_proceedings_pdf_list():

  html = ""

  for k, v in proceedings_urls.items():
    html += "<li><a href=\"" + v + "\">" + k + "</a></li>"

  if html != "":
    html = "<h2>Proceedings</h2><ul>" + html + "</ul>"

  return html


def gen_paper_list(target_category):
  html = ""
  for i, row in csv_data.iterrows():
    proc_id = conf_id.lower() + "_" + str(row['id']).zfill(2)
    author = row['author'].split(';')
    title = row['title']
    category = row['category']

    if category == target_category:
      html += "<li>" \
              + "<a href=\"proc/"+proc_id+"/\" class=\"page-link\">" \
                + ", ".join(author) + "<br><strong>" + title + "</strong></a>" \
              + "<a href=\"pdf/"+proc_id+".pdf\" class=\"pdf-link\">[PDF]</a>" \
            + "</li>"

  if html != "":
    html = "<h2>" + category_list[target_category] + "</h2><ol>" + html + "</ol>"

  return html


def gen_index_page():
  print("1. generate index page")

  with open('index.html', mode='w') as f:
    html = gen_index_page_html()
    f.write(html)

  return

def gen_paper_page():

  print("2. generate paper page")
  if not os.path.exists("proc"):
    print("make dir 'proc'")
    os.mkdir("proc")

  for i, row in csv_data.iterrows():
    proc_id = conf_id.lower() + "_" + str(row['id']).zfill(2)
    author = row['author'].split(';')
    title = row['title']
    category = row['category']
    start_page = "" if math.isnan(row['start_page']) else row['start_page']
    end_page = "" if math.isnan(row['end_page']) else row['end_page']

    target_dir = "proc/" + proc_id

    if not os.path.exists(target_dir):
      print("make dir '" + target_dir + "'")
      os.mkdir(target_dir)

    with open(target_dir + '/index.html', mode='w') as f:
      html = gen_paper_page_html(proc_id, author, title, category, start_page, end_page)
      f.write(html)

    # break

print("\n------------------\nProceedings Page Generator\n------------------\n")
gen_index_page()
gen_paper_page()
