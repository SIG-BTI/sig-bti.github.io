import pandas as pd
import os

csv_data = pd.read_csv('_proc.csv')

c_date = ["2023", "12", "22"] # yyyy, mm, dd
conf_place_en = "Tokyo"
conf_place_ja = "東京大学大学院 情報学環ダイワユビキタス学術研究館（東京都文京区）"
conf_id = "BTI06"
conf_name = "AIoT行動変容学会第６回研究会（" + conf_id + "）"
conf_url = "https://www.sig-bti.jp/event/bti06-report.html"

proceedings_urls = {
  "Proceedings (all)": "pdf/Proceedings_BTI06.pdf"
}

# do not change
issued_date = "/".join(c_date)
conf_month = ".".join(c_date[:1])
conf_date_ja = c_date[0] + "年" + c_date[1] + "月" + c_date[2] + "日"
pdf_url = "https://sig-bti.github.io/" + c_date[0] + c_date[1] + "/pdf/{proc_id}.pdf"

category_list = {
  "oral": "口頭発表（Oral）",
  "posterdemo": "ポスター・デモ発表（Poster/Demo）"
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
  <link rel="stylesheet" href="../../../style.css">
</head>
<body>
  <header>
    <h1>SIG-BTI DIGITAL LIBRARY</h1>
    <h2>Academy of Behavior Transformation by AIoT / AIoT行動変容学会（BTI）</h2>
  </header>
  <div class="main">
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
      Behavior Transformation by IoT
      <small>http://www.sig-bti.jp/</small>
    </a>
  </footer>
</body>
</html>'''.format(proc_id = proc_id,
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
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header>
    <h1>SIG-BTI DIGITAL LIBRARY</h1>
    <h2>Academy of Behavior Transformation by AIoT / AIoT行動変容学会（BTI）</h2>
  </header>
  <div class="main">
    <h2><a href="../">Top</a> / {conf_id} in {conf_place_en} ({conf_month})</h2>
    <p>
      {conf_name}, {conf_date_ja}, {conf_place_ja}<br>
      <a href="{conf_url}">{conf_url}</a>
    </p>
    <ul>
      <li>
        <h3>Combined</h3>
        <ul>
          {proceedings_pdf_list}
        </ul>
      </li>
      <li>
        <h3>Oral Session</h3>
        <ol>
          {oral_session_list}
        </ol>
      </li>
      <li>
        <h3>Poster/Demo Session</h3>
        <ol>
          {posterdemo_session_list}
        </ol>
      </li>
    </ul>
  </div>
  <footer>
    <a href="http://www.sig-bti.jp/">
      AIoT行動変容学会（BTI）<br>
      Behavior Transformation by IoT
      <small>http://www.sig-bti.jp/</small>
    </a>
  </footer>
</body>
</html>'''.format(conf_id = conf_id,
                  conf_place_en = conf_place_en,
                  conf_place_ja = conf_place_ja,
                  conf_month = conf_month,
                  conf_date_ja = conf_date_ja,
                  conf_name = conf_name,
                  conf_url = conf_url,
                  issued_date = issued_date,
                  proceedings_pdf_list = gen_proceedings_pdf_list(),
                  oral_session_list = gen_paper_list("oral"),
                  posterdemo_session_list = gen_paper_list("posterdemo"))
  return html

def gen_proceedings_pdf_list():

  html = ""
  for k, v in proceedings_urls.items():
    html += "<li><a href=\"" + v + "\">" + k + "</a></li>"

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
                + ", ".join(author) + "：「" + title + "」</a>" \
              + "<a href=\"pdf/"+proc_id+".pdf\" class=\"pdf-link\">[PDF]</a>" \
            + "</li>"

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
    start_page = row['start_page']
    end_page = row['end_page']

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
