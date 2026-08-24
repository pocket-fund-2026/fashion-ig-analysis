"""Shared post-categorization logic used by build_outputs.py and generate_content_ideas.py."""

BRANDS = ['chanel','gucci','saint laurent','ysl','dior','chrome hearts','casablanca','dsquared2','versace',
          'coach','prada','bottega','valentino','balenciaga','balmain','toteme','cos ','vogue','miu miu',
          'loewe','jimmy choo','marc jacobs','mcqueen','philip treacy','acne studios']

THEMES = [
    ('Death/tragedy', ['passed away','death','died','rip ','r.i.p','tragic','obituary']),
    ('Scandal/lawsuit/controversy', ['lawsuit','sued','accused','scandal','controvers','backlash','fired','cancel','ended their','claims that']),
    ('Celebrity/pop-culture gossip (off-fashion)', ['trump','white house','press secretary','senator','mcconnell','election','proof of life','mulvaney','dating','not hiding','speculation','kardashian']),
    ('Creative director/designer appointment or exit', ['creative director','appointed','debut collection','named ceo','steps down','departure','first collection','new era','new creative']),
    ('Runway/show/collection recap', ['runway','collection','fashion week','show','couture','resort 20','ready-to-wear','aw26','ss27','ss26']),
    ('Celebrity styling/endorsement/campaign', ['wore','red carpet','premiere','met gala','rocking','campaign','ambassador','face of','shot by','new face']),
    ('Brand launch/drop/store/pop-up', ['launch','drop','out now','out today','collab','pop-up','unveiled','opening','new store','expansion','teamed up']),
    ('Trend & data analysis', ['data on','data insights','popularity of','sentiment','search data','trend report','resurgence','hemline index','color palette','color of','colour of','pendulum','data backs','data ']),
    ('Style tips & trend commentary', ['styling','style','wear this','wardrobe','capsule','layer','silhouette','outfit','tailoring']),
    ('Accessory/beauty product spotlight', ['bag','handbag','shoe','heel','sneaker','jewellery','jewelry','watch','makeup','beauty','fragrance','perfume','lipstick','eyeshadow','glitter','contour']),
    ('Fashion history/archive/designer profile/museum', ['archive','history','vintage','retrospective','museum','exhibit','iconic','legacy','founder','founded','interview','profile','fun fact']),
    ('Nostalgia/throwback/pop-culture callback', ['2000s','90s','y2k','remember when','throwback','before ','2010s','early 2000']),
    ('Community engagement/interactive prompt', ['comment ur','comment your','caption this','tell me your','no gatekeeping','pls illustrate','reccos','tell your']),
    ('Culture/lifestyle crossover (art, music, festival, pride)', ['festival','concert','pride','art ','painting','sofa','porsche','pop girls']),
    ('Humor/meme/relatable lifestyle', ['monday scaries','lol','sksksk','toxic ex','aux','butter chicken','independence day','jowar','impulse purchase','investment']),
    ("Creator personal update/behind-the-scenes", ['coming soon','new series','thank u','working on','dm us','stylist @']),
    ('Brand feature/editorial spotlight', BRANDS),
]

def categorize(caption):
    c = (caption or '').lower()
    for name, kws in THEMES:
        if any(k in c for k in kws):
            return name
    if len(c.strip()) < 60:
        return 'Humor/meme/relatable lifestyle'
    return 'Uncategorized/other'
