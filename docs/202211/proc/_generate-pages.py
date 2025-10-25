import pandas as pd
import os

data = pd.read_csv('_proc.csv')

issued_date = "2022/11/21"
conf_name = "AIoT行動変容学会第２回研究会（BTI2）"
pdf_url = "https://sig-bti.github.io/202211/pdf/{proc_id}.pdf"
last_page = ""
first_page = ""

def gen_html(proc_id, author, title):
  html = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="DC.title" content="{title}"></meta>
  <meta name="citation_title" content="{title}"></meta>
  <meta name="DC.language" content="JA"></meta>{dc_creator}
  <meta name="citation_publication_date" content="{issued_date}"></meta>
  <meta name="DC.issued" content="{issued_date}"></meta>
  <meta name="citation_conference_title" content="{conf_name}"></meta>
  <meta name="DC.relation.ispartof" content="{conf_name}"></meta>
  <meta name="citation_firstpage" content="{first_page}"></meta>
  <meta name="DC.citation.spage" content="{first_page}"></meta>
  <meta name="citation_lastpage" content="{last_page}"></meta>
  <meta name="DC.citation.epage" content="{last_page}"></meta>
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
      <dt>Pages</dt><dd>{first_page}-{last_page}</dd>
      <dt>Abstract</dt><dd></dd>
      <dt>Conference</dt><dd><a href="../../">{conf_name}</a></dd>
      <dt>Paper ID</dt><dd>{proc_id}</dd>
      <dt>PDF Url</dt><dd><a href="{pdf_url}">{pdf_url}</a></dd>
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
                  first_page = first_page,
                  last_page = last_page,
                  pdf_url = pdf_url.format(proc_id = proc_id))
  return html

def gen_dc_creator(author):
  s = ""
  for a in author:
    s += '''
    <meta name=\"DC.creator\" content=\"{author}\"></meta>
    <meta name=\"citation_author\" content=\"{author}\"></meta>'''.format(author = a)
  return s

for i, row in data.iterrows():
  proc_id = row['id']
  author = row['author'].split(';')
  title = row['title']

  if not os.path.exists(proc_id):
    print("make dir " + proc_id)
    os.mkdir(proc_id)

  with open(proc_id + '/index.html', mode='w') as f:
    html = gen_html(proc_id, author, title)
    f.write(html)

  # break
