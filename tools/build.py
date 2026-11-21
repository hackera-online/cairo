#!/usr/bin/env python3
"""Генерира index.html, parfyumi.html, kontakti.html, sitemap.xml, robots.txt.
Хедърът/футърът са статични в HTML (по-добре за SEO). Пускане: python3 tools/build.py"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://cairo-perfumes.com"
NAME = "Cairo Perfumes"
ADDR = {"street": 'бул. "Свети Наум" 7-9', "city": "София", "zip": "1421", "country": "BG"}
MAPS = "https://www.google.com/maps/search/?api=1&query=" + "bul.+Sveti+Naum+7-9,+Sofia+1421,+Bulgaria"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">')

ICO = {
 "bag": '<path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 016 0v2"/>',
 "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A15 15 0 013 6a2 2 0 012-2z"/>',
 "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.5-7 10-7 10z"/>',
}
def ico(n):
    return f'<svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.3">{ICO[n]}</svg>'

NAV = [("new", "Нови", "parfyumi.html#new"), ("women", "За нея", "parfyumi.html#women"), ("men", "За него", "parfyumi.html#men"),
       ("unisex", "Унисекс", "parfyumi.html#unisex"), ("gifts", "Подаръци", "parfyumi.html"),
       ("about", "За нас", "index.html#about"), ("contact", "Контакти", "kontakti.html")]

FAM = [("Цветни", "floral"), ("Свежи", "fresh"), ("Ориенталски", "oriental"), ("Дървесни", "woody")]
def fam_col(g): return ("Ароматни семейства", [(n, f"{g}-{k}") for n, k in FAM])
MEGA = {
 "new": [("Последно", [("Нови аромати", "new"), ("Бестселъри", "best")]), ("Сезонно", [("Есен/Зима", "oriental"), ("Пролет/Лято", "fresh")]), ("В фокус", [("Ориенталски", "oriental"), ("Дървесни", "woody")])],
 "women": [("Парфюми за нея", [("Виж всички", "women")]), fam_col("women")],
 "men": [("Парфюми за него", [("Виж всички", "men")]), fam_col("men")],
 "unisex": [("Унисекс парфюми", [("Виж всички", "unisex")]), fam_col("unisex")],
 "gifts": [("Подаръци", [("За нея", "women"), ("За него", "men"), ("Унисекс", "unisex")])],
}
MEGA_ART = {"new": ("#7a3b1d", 1, "#6b3a1c"), "women": ("#a3283f", 2, "#4a1626"), "men": ("#4d6b45", 0, "#1d2a1f"),
            "unisex": ("#c9a47c", 1, "#3a2a1c"), "gifts": ("#0f5a49", 2, "#0f3d34")}

def header(page):
    nav = "".join(f'<a href="{h}" data-menu="{k}" class="{"active" if k == page else ""}">{t}</a>' for k, t, h in NAV)
    mega = ""
    for k, cols in MEGA.items():
        c = "".join(f'<div class="mega-col"><h4>{t}</h4><ul>' + "".join(f'<li><a href="parfyumi.html#{a}">{n}</a></li>' for n, a in ls) + "</ul></div>" for t, ls in cols)
        col, shape, bg = MEGA_ART[k]
        mega += f'<div class="mega" data-panel="{k}" hidden><div class="mega-inner">{c}<div class="mega-img" style="--a:{bg}" data-bottle="{col},{shape}"></div></div></div>'
    over = "is-over" if page == "home" else "is-solid"
    return f'''<div class="announce"><button class="ann-arrow" aria-label="Назад">‹</button><button class="ann-arrow" aria-label="Напред">›</button><p>Персонална консултация в магазина &nbsp;|&nbsp; <a href="kontakti.html">Как да ни намерите</a></p><button class="ann-close" aria-label="Затвори">×</button></div>
<header class="site-header {over}" id="header">
  <div class="hdr-row">
    <a class="logo" href="index.html" aria-label="{NAME} – начало"><img src="assets/img/logo.svg" alt="" width="43" height="56"><span class="logo-text"><span class="logo-main">Cairo</span><span class="logo-sub">PERFUMES</span></span></a>
    <nav class="main-nav" aria-label="Главно меню">{nav}</nav>
    <div class="hdr-icons">
      <button aria-label="Търсене">{ico("search")}</button>
      <a href="kontakti.html" aria-label="Контакти">{ico("phone")}</a>
      <button aria-label="Любими">{ico("heart")}</button>
      <button aria-label="Количка" id="cartBtn">{ico("bag")}<span class="cart-count" id="cartCount"></span></button>
      <button class="burger" id="burger" aria-label="Меню" aria-expanded="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
  <div class="mega-wrap">{mega}</div>
</header>'''

FOOT = [("Нужда от помощ?", ["Консултация в магазина", "Как да ни намерите", "Контакти", "ЧЗВ", "Карта на сайта"]),
        ("Услуги", ["Грижа за клиента", "Връщане и замяна", "Доставка", "Плащане", "Подаръчно опаковане"]),
        ("Компанията", ["За нас", "Марки", "Кариери", "Корпоративна информация"]),
        ("Правна информация", ["Общи условия", "Поверителност", "Политика за бисквитки", "Настройки на бисквитки"])]
FOOT_HREF = {"Консултация в магазина": "kontakti.html", "Как да ни намерите": "kontakti.html", "Контакти": "kontakti.html", "За нас": "index.html#about"}

def footer():
    cols = "".join(f'<div><h5>{h}</h5><ul>' + "".join(f'<li><a href="{FOOT_HREF.get(l, "#")}">{l}</a></li>' for l in ls) + "</ul></div>" for h, ls in FOOT)
    return f'''<footer class="site-footer">
  <div class="foot-top"><a href="#" class="to-top" id="toTop">Към началото ↑</a></div>
  <div class="foot-news"><label for="nl">Абонирай се за бюлетина</label>
    <input id="nl" type="email" placeholder="Имейл" autocomplete="email">
    <div class="country"><span>Държава</span><small>България / Български</small></div></div>
  <div class="foot-cols">
    {cols}
    <div><h5>Последвай ни</h5><div class="socials"><a href="#" aria-label="Instagram">IG</a><a href="#" aria-label="Facebook">FB</a><a href="#" aria-label="TikTok">TT</a></div>
      <h5 style="margin-top:32px">Магазин</h5><address style="font-style:normal;font-size:14px;color:#cfc8b8">{ADDR["street"]}<br>{ADDR["zip"]} {ADDR["city"]}</address></div>
  </div>
  <div class="foot-bottom">Powered by <a href="https://hackera.online" rel="noopener">Hackera Online</a> &nbsp; © 2026 {NAME}. Всички права запазени.</div>
</footer>
<aside class="cart-drawer" id="drawer" aria-hidden="true">
  <div class="cd-head"><h3>Количка</h3><button id="cdClose" aria-label="Затвори">×</button></div>
  <div class="cd-items" id="cdItems"></div>
  <div class="cd-foot"><div class="cd-total"><span>Общо</span><strong id="cdTotal">0 €</strong></div><button class="btn btn-gold">Към поръчката</button></div>
</aside><div class="scrim" id="scrim"></div>'''

def schema():
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": NAME, "inLanguage": "bg-BG"},
        {"@type": "PerfumeStore" if False else "Store", "@id": DOMAIN + "/#store", "name": NAME, "alternateName": "Cairo парфюми",
         "url": DOMAIN + "/", "image": DOMAIN + "/assets/img/hero.jpg", "logo": DOMAIN + "/assets/img/logo.svg",
         "description": "Парфюмерия в София – аромати от световноизвестни марки и персонални консултации.",
         "priceRange": "€€",
         "address": {"@type": "PostalAddress", "streetAddress": ADDR["street"], "addressLocality": ADDR["city"],
                     "addressRegion": "София-град", "postalCode": ADDR["zip"], "addressCountry": ADDR["country"]},
         "hasMap": MAPS}]}

def page(file, key, title, desc, body, h1_img=None, extra_ld=None):
    url = DOMAIN + "/" + ("" if file == "index.html" else file)
    ld = json.dumps(schema(), ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="bg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0a0d0c">
<meta property="og:type" content="website">
<meta property="og:locale" content="bg_BG">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/img/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body data-page="{key}">
{header(key)}
{body}
{footer()}
<script src="assets/js/data.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

HOME = f'''<main>
  <section class="hero" aria-roledescription="carousel" aria-label="Акценти">
    <div class="hero-stage">
      <div class="slide on">
        <div class="hero-copy">
          <p class="eyebrow">Парфюмерия · София</p>
          <h1 class="h-xl">Аромат, който <em>разказва</em> вашата история</h1>
          <p class="lead">Селекция от световноизвестни марки, персонални консултации и аромати за всеки повод и бюджет – на бул. „Свети Наум“ 7-9.</p>
          <div class="btns"><a href="parfyumi.html" class="btn btn-gold">Разгледай парфюмите</a><a href="kontakti.html" class="btn btn-line">Посети магазина</a></div>
        </div>
        <div class="hero-img"><img src="assets/img/hero.jpg" alt="Луксозен зелен парфюм със златен орнамент, шафран и розови листенца" width="738" height="739" fetchpriority="high"></div>
      </div>
      <div class="slide">
        <div class="hero-copy">
          <p class="eyebrow">Ориенталски аромати</p>
          <h2 class="h-xl">Уд, амбра и <em>шафран</em></h2>
          <p class="lead">Наситени, топли композиции за вечерите и специалните поводи.</p>
          <div class="btns"><a href="parfyumi.html#oriental" class="btn btn-gold">Виж ароматите</a></div>
        </div>
        <div class="hero-img"><div class="art" style="--a:#6b3a1c" data-bottle="#7a3b1d,1"></div></div>
      </div>
      <div class="slide">
        <div class="hero-copy">
          <p class="eyebrow">Персонална консултация</p>
          <h2 class="h-xl">Намерете своя <em>перфектен</em> аромат</h2>
          <p class="lead">Специалистите в магазина ще ви помогнат да изберете според вкуса, повода и бюджета ви.</p>
          <div class="btns"><a href="kontakti.html" class="btn btn-gold">Свържете се с нас</a></div>
        </div>
        <div class="hero-img"><div class="art" style="--a:#1b6a58" data-bottle="#0f5a49,2"></div></div>
      </div>
    </div>
    <div class="hero-ctrl"><button class="hero-pause" id="heroPause" aria-label="Пауза"><i></i><i></i></button><div class="hero-dots" id="heroDots"></div></div>
  </section>

  <section class="sec">
    <div class="sec-head"><p class="eyebrow">Колекции</p><h2>Ароматни семейства</h2><div class="orn"><i></i></div></div>
    <div class="fam-grid" id="families"></div>
  </section>

  <section class="sec" style="padding-top:0">
    <div class="sec-head"><p class="eyebrow">Избрано от нас</p><h2>Най-търсени аромати</h2><div class="orn"><i></i></div></div>
    <div class="prod-row" id="bestsellers"></div>
    <p class="demo-note" style="text-align:center">Демонстративни продукти и цени.</p>
  </section>

  <section class="split" id="about">
    <div class="split-art"><div id="splitBottle" style="display:contents"></div></div>
    <div class="split-text">
      <p class="eyebrow">За нас</p>
      <h2>Намерете своя перфектен аромат</h2>
      <p>Cairo Perfumes предлага уникален асортимент от парфюми, които задоволяват вкусовете на клиентите в София. Всеки аромат е внимателно подбран, а специалистите в магазина предлагат персонални консултации – за да откриете парфюма, който отива на вашия стил и повод.</p>
      <div class="btns"><a href="kontakti.html" class="btn btn-line">Свържете се с нас</a></div>
    </div>
  </section>

  <section class="sec"><div class="usp" id="usp"></div></section>

  <section class="visit">
    <p class="eyebrow">Магазин в София</p>
    <h2>{ADDR["street"]}</h2>
    <p>{ADDR["zip"]} {ADDR["city"]}, България. Приятна атмосфера, нови аромати и екип, който ще ви помогне да изберете.</p>
    <a href="{MAPS}" target="_blank" rel="noopener" class="btn btn-gold">Виж на картата</a>
  </section>
</main>'''

SHOP = '''<main>
  <header class="page-head"><p class="eyebrow">Каталог</p><h1>Парфюми</h1><p>Аромати за нея, за него и унисекс – ориенталски, дървесни, цветни и свежи.</p></header>
  <div class="catalog">
    <nav class="side-nav" id="sideNav" aria-label="Филтри"></nav>
    <div><div class="cat-top"><span id="count"></span><span>Цени за 100 мл EDP</span></div><div class="product-grid" id="productGrid"></div><p class="demo-note">Демонстративни продукти и цени – ще бъдат заменени с реалния асортимент.</p></div>
  </div>
</main>'''

CONTACT = f'''<main>
  <header class="page-head"><p class="eyebrow">Свържете се с нас</p><h1>Контакти</h1><p>Заповядайте в магазина за персонална консултация или ни пишете.</p></header>
  <div class="contact">
    <div>
      <h2>Магазин София</h2>
      <ul class="info">
        <li><small>Адрес</small><address>{ADDR["street"]}<br>{ADDR["zip"]} {ADDR["city"]}, България</address></li>
        <li><small>Услуга</small>Персонални консултации за избор на аромат</li>
      </ul>
      <div class="map-card"><div><strong>{ADDR["street"]}, {ADDR["city"]}</strong><a href="{MAPS}" target="_blank" rel="noopener" class="btn btn-gold">Отвори в Google Maps</a></div></div>
    </div>
    <div>
      <h2>Изпратете запитване</h2>
      <form id="contactForm">
        <div><label for="n">Име</label><input id="n" required autocomplete="name"></div>
        <div><label for="e">Имейл</label><input id="e" type="email" required autocomplete="email"></div>
        <div><label for="m">Съобщение</label><textarea id="m" required></textarea></div>
        <button class="btn btn-gold" type="submit">Изпрати</button>
        <p class="ok" id="formOk" hidden>Благодарим! Това е демо форма – съобщението не се изпраща.</p>
      </form>
    </div>
  </div>
</main>'''

pages = [
 ("index.html", "home", "Cairo Perfumes – парфюмерия в София | cairo-perfumes.com",
  "Cairo Perfumes – парфюмерия на бул. Свети Наум 7-9, София. Парфюми от световноизвестни марки, персонални консултации и достъпни цени.", HOME),
 ("parfyumi.html", "shop", "Парфюми за нея, за него и унисекс | Cairo Perfumes София",
  "Разгледайте парфюми – ориенталски, дървесни, цветни и свежи аромати за жени, мъже и унисекс. Cairo Perfumes, София.", SHOP),
 ("kontakti.html", "contact", "Контакти и адрес – Cairo Perfumes, бул. Свети Наум 7-9, София",
  "Адрес: бул. Свети Наум 7-9, 1421 София. Посетете Cairo Perfumes за персонална консултация и избор на аромат.", CONTACT),
]
for f, k, t, d, b in pages:
    (ROOT / f).write_text(page(f, k, t, d, b), encoding="utf-8")

urls = "".join(f"  <url><loc>{DOMAIN}/{'' if f == 'index.html' else f}</loc><lastmod>2026-11-21</lastmod></url>\n" for f, *_ in pages)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
print("ok")
