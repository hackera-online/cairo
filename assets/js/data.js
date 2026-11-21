/* Съдържание на Cairo Perfumes – цените и продуктите са демонстративни */
window.SHOP = {
  brand: "Cairo Perfumes",
  domain: "https://cairo-perfumes.com",
  genders: [["women", "За нея"], ["men", "За него"], ["unisex", "Унисекс"]],
  families: [["oriental", "Ориенталски"], ["woody", "Дървесни"], ["floral", "Цветни"], ["fresh", "Свежи"]],
  // shape: 0 правоъгълен, 1 арка (ориенталски), 2 заоблен; c = цвят на течността
  products: [
    { id: 1, name: "Oud Nile", g: "unisex", f: "oriental", notes: "уд · шафран · амбра", price: 189, c: "#7a3b1d", shape: 1, tag: "Бестселър" },
    { id: 2, name: "Khan el-Khalili", g: "unisex", f: "oriental", notes: "канела · ванилия · мускус", price: 129, c: "#a8561f", shape: 0 },
    { id: 3, name: "Amber Sahara", g: "men", f: "oriental", notes: "амбра · тамян · кожа", price: 149, c: "#b9812b", shape: 1, tag: "Ново" },
    { id: 4, name: "Rose de Giza", g: "women", f: "floral", notes: "дамаскинска роза · малина · пачули", price: 139, c: "#a3283f", shape: 2, tag: "Бестселър" },
    { id: 5, name: "Jasmin Luxor", g: "women", f: "floral", notes: "жасмин · ябълков цвят · бял мускус", price: 119, c: "#d8c27a", shape: 2 },
    { id: 6, name: "Saffron Pharaoh", g: "men", f: "oriental", notes: "шафран · кардамон · кедър", price: 159, c: "#c4571c", shape: 0 },
    { id: 7, name: "Sandal Aswan", g: "unisex", f: "woody", notes: "сандалово дърво · кокос · ирис", price: 135, c: "#c9a47c", shape: 1 },
    { id: 8, name: "Vetiver Delta", g: "men", f: "woody", notes: "ветивер · грейпфрут · мъх", price: 99, c: "#4d6b45", shape: 0 },
    { id: 9, name: "Bergamot Cairo", g: "men", f: "fresh", notes: "бергамот · мента · морска сол", price: 89, c: "#6fa17c", shape: 0, tag: "Ново" },
    { id: 10, name: "Iris Papyrus", g: "women", f: "floral", notes: "ирис · пудра · бяло дърво", price: 145, c: "#8d7fb0", shape: 2 },
    { id: 11, name: "Noir Sphinx", g: "unisex", f: "woody", notes: "черен уд · пипер · тютюн", price: 175, c: "#2a2220", shape: 1 },
    { id: 12, name: "Citrus Corniche", g: "women", f: "fresh", notes: "мандарина · зелен чай · портокалов цвят", price: 79, c: "#e0a63a", shape: 2 }
  ],
  usp: [
    ["Световни марки", "Внимателно подбрана селекция от световноизвестни парфюмни марки – качество и стил."],
    ["Персонална консултация", "Специалистите в магазина ви помагат да откриете аромата, който отива на вашия вкус и повод."],
    ["Достъпни цени", "Богат ценови диапазон за различни бюджети – от свежи ежедневни до наситени вечерни аромати."]
  ]
};
