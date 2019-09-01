import os
import bs4                                                                                                                                    
import requests                
import fire


def get_site_url(url):
  site_url_parts = url.split('/')[:-1]
  return '/'.join(site_url_parts)


def get_links(html):
  soup = bs4.BeautifulSoup(html, features='lxml')
  return [link.get("href") for link in soup("a")]


def maybe_add_full_links(links, site_url):
  def maybe_add_site_url(link):
    if link.startswith('http') or link.startswith('www'):
      return link
    else:
      return site_url + '/' + link
  return [maybe_add_site_url(link) for link in links]


def download_from_link(link):
  filename = os.path.basename(link)
  file_content = requests.get(link).content
  with open(filename, 'wb') as f:
    f.write(file_content)


def download_pdfs_from_site(url):

    url = 'http://www.ii.uni.wroc.pl/~lipinski/lectureAE2019.html'
    site_url = get_site_url(url)
    html = requests.get(url).text


    all_links = get_links(html)
    pdf_links = [link for link in all_links if link.endswith('pdf')]
    pdf_links = maybe_add_full_links(pdf_links, site_url)

    for link in pdf_links:
        download_from_link(link)


if __name__ == '__main__':
  fire.Fire(download_pdfs_from_site)
