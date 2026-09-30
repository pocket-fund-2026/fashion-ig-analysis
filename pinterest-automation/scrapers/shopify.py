"""Scrape bridal/couture collections from a Shopify storefront via public /collections/<h>/products.json."""
import json, sys, re, os, urllib.request, time
UA={"User-Agent":"Mozilla/5.0 (compatible; bombay-bride-pin-research)"}
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
def scrape(brand, domain, collections):
    out=[]
    for c in collections:
        page=1
        while True:
            d=get(f"https://{domain}/collections/{c}/products.json?limit=250&page={page}")['products']
            if not d: break
            for p in d:
                out.append(dict(brand=brand,domain=domain,collection=c,title=p['title'].title(),
                  page_url=f"https://{domain}/products/{p['handle']}",
                  tags=p.get('tags'),images=[i['src'] for i in p['images']]))
            page+=1; time.sleep(1)
    return out
if __name__=="__main__":
    brand,domain,*cols=sys.argv[1:]
    items=scrape(brand,domain,cols)
    seen=set(); uniq=[]
    for i in items:
        if i['page_url'] in seen: continue
        seen.add(i['page_url']); uniq.append(i)
    slug=re.sub(r'\W+','-',brand.lower())
    json.dump(uniq,open(f"../sources/{slug}.json","w"),indent=1)
    print(brand,len(uniq),"products",sum(len(i['images']) for i in uniq),"images")
