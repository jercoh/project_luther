import os, sys, json, locale
import requests
import lxml.html

locale.setlocale(locale.LC_ALL, 'en_US')

def main(id):
    requested_id = id
    if requested_id is not None and requested_id.startswith('tt'):
        hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + requested_id).content)
        movie = {}
        try:
            movie['title'] = hxs.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0].strip()
        except IndexError:
            movie['title']
        try:
            movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[2]/a/text()')[0].strip()
        except IndexError:
            try:
                movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[3]/a/text()')[0].strip()
            except IndexError:
                movie['year'] = ""
        try:
            movie['certification'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[1]/@title')[0].strip()
        except IndexError:
            movie['certification'] = ""
        try:
            movie['running_time'] = hxs.xpath('//*[@id="overview-top"]/div[2]/time/text()')[0].strip()
        except IndexError:
            movie['running_time'] = ""
        try:
            movie['genre'] = hxs.xpath('//*[@id="overview-top"]/div[2]/a/span/text()')
        except IndexError:
            movie['genre'] = []
        try:
            movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[3]/a/text()')[0].strip()
        except IndexError:
            try:
                movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[4]/a/text()')[0].strip()
            except Exception:
                movie['release_date'] = ""
        try:
            movie['rating'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/strong/span/text()')[0]
        except IndexError:
            movie['rating'] = ""
        try:
            movie['metascore'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[2]/text()')[0].strip().split('/')[0]
        except IndexError:
            movie['metascore'] = 0
        try:
            movie['description'] = hxs.xpath('//*[@id="overview-top"]/p[2]/text()')[0].strip()
        except IndexError:
            movie['description'] = ""
        try:
            movie['director'] = hxs.xpath('//*[@id="overview-top"]/div[4]/a/span/text()')[0].strip()
        except IndexError:
            movie['director'] = ""
        try:
            movie['stars'] = hxs.xpath('//*[@id="overview-top"]/div[6]/a/span/text()')
        except IndexError:
            movie['stars'] = ""
        try:
            movie['writers'] = hxs.xpath('//*[@id="overview-top"]/div[5]/a/span/text()')
        except IndexError:
            movie['writers'] = ""
        try:
            movie['poster'] = hxs.xpath('//*[@id="img_primary"]/div/a/img/@src')[0]
        except IndexError:
            movie['poster'] = ""
        try:
            movie['gallery'] = hxs.xpath('//*[@id="combined-photos"]/div/a/img/@src')
        except IndexError:
            movie['gallery'] = ""
        try:
            movie['storyline'] = hxs.xpath('//*[@id="titleStoryLine"]/div[1]/p/text()')[0].strip()
        except IndexError:
            movie['storyline'] = ""
        try:
            movie['votes'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[1]/span/text()')[0].strip()
        except IndexError:
            movie['votes'] = ""
        try:
            budget = hxs.xpath('//*[@id="titleDetails"]/div[h4/text()="Budget:"]/h4//following::text()')[0].strip()
            movie['budget'] = locale.atoi(budget.strip('$'))
        except:
            movie['budget'] = ""
        try:
            gross = hxs.xpath('//*[@id="titleDetails"]/div[h4/text()="Gross:"]/h4//following::text()')[0].strip()
            movie['domestic_total_gross'] = locale.atoi(gross.strip('$'))
        except:
            movie['domestic_total_gross'] = ""
        try:
            opening_weekend = hxs.xpath('//*[@id="titleDetails"]/div[h4/text()="Opening Weekend:"]/h4//following::text()')[0]
            opening_weekend = opening_weekend.split()[0]
            movie['opening_weekend'] = locale.atoi(opening_weekend.strip('$'))
        except:
            movie['opening_weekend'] = ""
        try:
            movie['production_companies'] = hxs.xpath('//*[@id="titleDetails"]/div[h4/text()="Production Co:"]/span/a/span/text()')
        except:
            movie['production_companies'] = ""
        try:
            movie['awards'] = {}
            hxs_awards = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + requested_id+"/awards?ref_=tt_awd").content)
            award_list = hxs_awards.xpath('//*[@class="article listo"]/div[@class="header"]//div[@class="nav"]/div/text()')[0].split()
            movie['awards']['wins'] = award_list[2]
            movie['awards']['nominations'] = award_list[5]
        except:
            movie['awards'] = {}
            movie['awards']['wins'] = ""
            movie['awards']['nominations'] = ""
        print json.dumps(movie)
    else:
        print "invalid id"


if __name__ == '__main__':
    main(sys.argv[1])