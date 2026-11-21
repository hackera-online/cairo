# Cairo Perfumes – демо (cairo-perfumes.com)

Статичен сайт (HTML/CSS/JS), без зависимости. Деплой в GitHub Pages чрез Actions.

## Деплой (първи път)
1. Създай празно репо в GitHub (напр. `cairo-perfumes`) и качи съдържанието на тази папка в клон `main`:
   ```
   git init -b main && git add . && git commit -m "Cairo Perfumes demo"
   git remote add origin git@github.com:<акаунт>/cairo-perfumes.git && git push -u origin main
   ```
2. В репото: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Workflow-ът `.github/workflows/pages.yml` се пуска при всеки push в `main`. Адресът е
   `https://<акаунт>.github.io/cairo-perfumes/` (виж таба Actions).

## Собствен домейн
- Създай файл `CNAME` в корена с един ред, напр. `cairo-perfumes.com` (или поддомейн за демото).
- DNS: за поддомейн – CNAME запис към `<акаунт>.github.io`; за apex домейн – A записи към
  185.199.108.153 / 109.153 / 110.153 / 111.153.
- В Settings → Pages включи **Enforce HTTPS**.

## Структура
- `index.html`, `parfyumi.html`, `kontakti.html`, `404.html` – страници (първите три се генерират от `tools/build.py`)
- `assets/css/style.css` – дизайн (токени най-горе: `--gold`, `--emerald`, 8px мрежа)
- `assets/js/data.js` – продукти, семейства, текстове (демо цени); `assets/js/main.js` – менюта, слайдер, каталог, количка
- `assets/img/` – `logo.svg` (прерисувано лого), `hero.jpg`
- `sitemap.xml`, `robots.txt` – базово SEO; canonical/OG са към `https://cairo-perfumes.com`

## Промени
Съдържание: `assets/js/data.js`. Хедър/футър/SEO мета: `python3 tools/build.py` (пренаписва трите HTML файла, sitemap и robots).
Всички пътища са относителни, затова сайтът работи и в подпапка (`github.io/<репо>/`).
