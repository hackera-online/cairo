(function () {
  const S = window.SHOP;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const eur = n => new Intl.NumberFormat("bg-BG", { style: "currency", currency: "EUR", minimumFractionDigits: 0 }).format(n);
  let uid = 0;

  /* ---------- SVG шишенце ---------- */
  function bottle(c, shape) {
    const id = "b" + ++uid;
    const body = [
      '<rect x="30" y="64" width="60" height="78" rx="4"/>',
      '<path d="M30 142V98Q30 76 60 64Q90 76 90 98V142z"/>',
      '<rect x="28" y="64" width="64" height="78" rx="30"/>'
    ][shape || 0];
    const bodyClip = body.replace("<", `<`);
    return `<svg class="bottle" viewBox="0 0 120 170" aria-hidden="true">
      <defs>
        <linearGradient id="${id}g" x1="0" x2="1"><stop offset="0" stop-color="${c}" stop-opacity=".55"/><stop offset=".45" stop-color="${c}"/><stop offset="1" stop-color="${c}" stop-opacity=".6"/></linearGradient>
        <linearGradient id="${id}m" x1="0" x2="1"><stop offset="0" stop-color="#8a6a2c"/><stop offset=".5" stop-color="#f0d58a"/><stop offset="1" stop-color="#8a6a2c"/></linearGradient>
      </defs>
      <ellipse cx="60" cy="152" rx="40" ry="5" fill="#000" opacity=".35"/>
      <g fill="url(#${id}g)" stroke="#e7c97c" stroke-width="1.2">${bodyClip}</g>
      <g fill="none" stroke="#e7c97c" stroke-width=".8" opacity=".7"><path d="M44 78v56M76 78v56"/></g>
      <rect x="52" y="50" width="16" height="16" fill="url(#${id}m)"/>
      <rect x="46" y="22" width="28" height="30" rx="3" fill="url(#${id}m)" stroke="#6b5220" stroke-width=".6"/>
      <rect x="49" y="26" width="3" height="22" fill="#fff" opacity=".35"/>
    </svg>`;
  }
  window.cairoBottle = bottle;

  function productCard(p) {
    return `<article class="p-card">
      <a href="parfyumi.html" class="p-img" aria-label="${p.name}">${p.tag ? `<em class="tag">${p.tag}</em>` : ""}${bottle(p.c, p.shape)}</a>
      <div class="p-meta"><h3>${p.name}</h3><span class="notes">${p.notes}</span><span class="price">${eur(p.price)} <small>/ 100 мл EDP</small></span></div>
      <button class="p-add" onclick="addToCart(${p.id})">Добави в количката</button></article>`;
  }

  /* ---------- Mega меню ---------- */
  const hdr = $("#header");
  let closeT;
  $$(".main-nav a").forEach(a => a.addEventListener("mouseenter", () => {
    clearTimeout(closeT);
    if (!$(`.mega[data-panel="${a.dataset.menu}"]`)) return closeMega();
    $$(".mega").forEach(m => (m.hidden = m.dataset.panel !== a.dataset.menu));
    $$(".main-nav a").forEach(x => x.classList.toggle("hover", x === a));
    hdr.classList.add("mega-open");
  }));
  const closeMega = () => { $$(".mega").forEach(m => (m.hidden = true)); $$(".main-nav a").forEach(x => x.classList.remove("hover")); hdr.classList.remove("mega-open"); };
  hdr.addEventListener("mouseleave", () => { closeT = setTimeout(closeMega, 120); });
  addEventListener("scroll", () => hdr.classList.toggle("scrolled", scrollY > 40), { passive: true });
  hdr.classList.toggle("scrolled", scrollY > 40);
  const ann = $(".ann-close"); if (ann) ann.onclick = () => $(".announce").remove();
  const msgs = [["Персонална консултация в магазина", "Как да ни намерите", "kontakti.html"], ["Нови аромати в магазина", "Пазарувай", "parfyumi.html#new"]];
  let mi = 0;
  const annP = $(".announce p");
  const showMsg = d => { mi = (mi + d + msgs.length) % msgs.length; annP.innerHTML = `${msgs[mi][0]} &nbsp;|&nbsp; <a href="${msgs[mi][2]}">${msgs[mi][1]}</a>`; };
  $$(".ann-arrow").forEach((b, i) => b.addEventListener("click", () => showMsg(i ? 1 : -1)));
  $$("[data-bottle]").forEach(el => { const [c, sh] = el.dataset.bottle.split(","); el.innerHTML = bottle(c, +sh); });
  const burger = $("#burger");
  if (burger) burger.onclick = () => { const o = document.body.classList.toggle("menu-open"); burger.setAttribute("aria-expanded", String(o)); };
  const top = $("#toTop"); if (top) top.onclick = e => { e.preventDefault(); scrollTo({ top: 0, behavior: "smooth" }); };

  /* ---------- Количка (localStorage) ---------- */
  const load = () => { try { return JSON.parse(localStorage.getItem("cairo-cart")) || []; } catch (e) { return []; } };
  const save = c => { try { localStorage.setItem("cairo-cart", JSON.stringify(c)); } catch (e) {} };
  let cart = load();
  function renderCart() {
    $("#cartCount").textContent = cart.reduce((a, i) => a + i.qty, 0) || "";
    $("#cdItems").innerHTML = cart.length ? cart.map(i => `
      <div class="cd-item"><div class="cd-ph">${bottle(i.c, i.shape)}</div>
      <div><p>${i.name}</p><small>${eur(i.price)} × ${i.qty}</small></div>
      <button data-rm="${i.id}" aria-label="Премахни">×</button></div>`).join("") : "<p class='empty'>Количката е празна. Добавете аромат от каталога.</p>";
    $("#cdTotal").textContent = eur(cart.reduce((a, i) => a + i.price * i.qty, 0));
  }
  window.addToCart = id => {
    const p = S.products.find(x => x.id === id); if (!p) return;
    const ex = cart.find(i => i.id === id);
    ex ? ex.qty++ : cart.push({ id: p.id, name: p.name, price: p.price, c: p.c, shape: p.shape, qty: 1 });
    save(cart); renderCart(); drawer(true);
  };
  function drawer(open) {
    $("#drawer").classList.toggle("open", open); $("#scrim").classList.toggle("open", open);
    $("#drawer").setAttribute("aria-hidden", String(!open));
  }
  $("#cartBtn").onclick = () => drawer(true);
  $("#cdClose").onclick = $("#scrim").onclick = () => drawer(false);
  $("#cdItems").addEventListener("click", e => {
    const id = e.target.dataset.rm; if (!id) return;
    cart = cart.filter(i => i.id !== +id); save(cart); renderCart();
  });
  renderCart();

  /* ---------- Начална ---------- */
  const best = $("#bestsellers");
  if (best) best.innerHTML = S.products.filter(p => p.tag || [4, 7, 11, 8].includes(p.id)).slice(0, 4).map(productCard).join("");
  const fam = $("#families");
  if (fam) {
    const tones = { oriental: ["#3a1d0e", "#7a3b1d", 1], woody: ["#1d2a1f", "#4d6b45", 0], floral: ["#3a1220", "#a3283f", 2], fresh: ["#10302a", "#6fa17c", 0] };
    fam.innerHTML = S.families.map(([k, n]) => `<a href="parfyumi.html#${k}" class="fam-tile" style="--a:${tones[k][0]}">${bottle(tones[k][1], tones[k][2])}<span>${n}</span></a>`).join("");
  }
  const usp = $("#usp");
  if (usp) usp.innerHTML = S.usp.map((u, i) => `<div><b>0${i + 1}</b><h3>${u[0]}</h3><p>${u[1]}</p></div>`).join("");
  const sb = $("#splitBottle"); if (sb) sb.innerHTML = bottle("#0f5a49", 1);

  /* ---------- Hero слайдер ---------- */
  $$("[data-bottle]").forEach(el => { const [c, sh] = el.dataset.bottle.split(","); el.innerHTML = bottle(c, +sh); });
  const slides = $$(".slide");
  if (slides.length > 1) {
    const dots = $("#heroDots"), pauseBtn = $("#heroPause");
    let cur = 0, timer, paused = matchMedia("(prefers-reduced-motion:reduce)").matches;
    dots.innerHTML = slides.map((_, i) => `<button aria-label="Слайд ${i + 1}"></button>`).join("");
    const go = i => {
      cur = (i + slides.length) % slides.length;
      slides.forEach((s, k) => { s.classList.toggle("on", k === cur); s.setAttribute("aria-hidden", String(k !== cur)); });
      $$("button", dots).forEach((b, k) => b.classList.toggle("on", k === cur));
    };
    const run = () => { clearInterval(timer); if (!paused) timer = setInterval(() => go(cur + 1), 6000); };
    dots.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; go($$("button", dots).indexOf(b)); run(); });
    pauseBtn.classList.toggle("paused", paused);
    pauseBtn.onclick = () => { paused = !paused; pauseBtn.classList.toggle("paused", paused); pauseBtn.setAttribute("aria-label", paused ? "Пускане" : "Пауза"); run(); };
    go(0); run();
  }

  /* ---------- Каталог ---------- */
  const grid = $("#productGrid");
  if (grid) {
    const side = $("#sideNav");
    const G = S.genders.map(g => g[0]), F = S.families.map(f => f[0]), SP = ["new", "best"];
    let st = { g: "", f: "", s: "" };
    const parse = h => { st = { g: "", f: "", s: "" }; h.split("-").forEach(k => { if (G.includes(k)) st.g = k; else if (F.includes(k)) st.f = k; else if (SP.includes(k)) st.s = k; }); };
    const toHash = () => [st.s, st.g, st.f].filter(Boolean).join("-");
    parse(location.hash.slice(1));
    const btn = (k, n) => `<li><button data-k="${k}">${n}</button></li>`;
    side.innerHTML = `<h2>Парфюми</h2><ul>${btn("all", "Виж всички")}</ul>
      <h3>Подбрано</h3><ul>${btn("new", "Нови")}${btn("best", "Бестселъри")}</ul>
      <h3>За кого</h3><ul>${S.genders.map(g => btn(...g)).join("")}</ul>
      <h3>Аромат</h3><ul>${S.families.map(f => btn(...f)).join("")}</ul>`;
    const draw = () => {
      const list = S.products.filter(p => (!st.g || p.g === st.g || (p.g === "unisex" && st.g !== "unisex")) && (!st.f || p.f === st.f) && (st.s !== "new" || p.tag === "Ново") && (st.s !== "best" || p.tag === "Бестселър"));
      $$("button", side).forEach(b => { const k = b.dataset.k; b.classList.toggle("on", k === "all" ? !st.g && !st.f && !st.s : [st.g, st.f, st.s].includes(k)); });
      grid.innerHTML = list.map(productCard).join("") || "<p class='empty'>Няма продукти в тази комбинация.</p>";
      const c = $("#count"); if (c) c.textContent = list.length + " аромата";
    };
    side.addEventListener("click", e => {
      const k = e.target.dataset.k; if (!k) return;
      if (k === "all") st = { g: "", f: "", s: "" };
      else if (G.includes(k)) st.g = st.g === k ? "" : k;
      else if (F.includes(k)) st.f = st.f === k ? "" : k;
      else st.s = st.s === k ? "" : k;
      history.replaceState(null, "", "#" + toHash()); draw();
    });
    addEventListener("hashchange", () => { parse(location.hash.slice(1)); draw(); });
    draw();
  }

  /* ---------- Контакт форма (демо) ---------- */
  const form = $("#contactForm");
  if (form) form.addEventListener("submit", e => { e.preventDefault(); $("#formOk").hidden = false; form.reset(); });
})();
