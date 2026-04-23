const PAGE = document.body.dataset.page;

function normalize(value) {
  return String(value || "").trim().toLowerCase();
}

function formatPrice(value) {
  return `¥${Number(value).toFixed(2)}`;
}

function setupStaticPage() {
  const cards = Array.from(document.querySelectorAll(".product-card"));
  const categoryFilter = document.querySelector("#categoryFilter");
  const ratingFilter = document.querySelector("#ratingFilter");
  const inlineSearch = document.querySelector("#inlineSearch");
  const resultCount = document.querySelector("#staticResultCount");

  function update() {
    const category = categoryFilter.value;
    const minRating = Number(ratingFilter.value);
    const keyword = normalize(inlineSearch.value);
    let visible = 0;

    cards.forEach((card) => {
      const matchedCategory = category === "all" || card.dataset.category === category;
      const matchedRating = Number(card.dataset.rating) >= minRating;
      const matchedKeyword = !keyword || normalize(card.innerText).includes(keyword);
      const show = matchedCategory && matchedRating && matchedKeyword;

      card.classList.toggle("is-hidden", !show);
      if (show) {
        visible += 1;
      }
    });

    resultCount.textContent = `共 ${cards.length} 件商品，当前显示 ${visible} 件`;
  }

  [categoryFilter, ratingFilter, inlineSearch].forEach((element) => {
    element.addEventListener("input", update);
    element.addEventListener("change", update);
  });

  update();
}

function coverClass(category) {
  const map = {
    Python: "cover-python",
    Crawler: "cover-crawler",
    Data: "cover-data",
    HTML: "cover-html",
    Automation: "cover-auto",
    AI: "cover-ai",
    Database: "cover-database",
    Security: "cover-security",
  };
  return map[category] || "cover-crawler";
}

function initials(book) {
  const map = {
    Python: "Py",
    Crawler: "Cr",
    Data: "Da",
    HTML: "Ht",
    Automation: "Se",
    AI: "AI",
    Database: "DB",
    Security: "Sc",
  };
  return map[book.category] || book.title.slice(0, 2);
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function highlight(text, keyword) {
  if (!keyword) {
    return text;
  }
  const pattern = new RegExp(escapeRegExp(keyword), "gi");
  return String(text).replace(pattern, (matched) => `<mark>${matched}</mark>`);
}

function searchableText(book) {
  return normalize([
    book.id,
    book.isbn,
    book.title,
    book.subtitle,
    book.author.name,
    book.publisher.name,
    book.category,
    book.level,
    book.tags.join(" "),
    book.badges.join(" "),
  ].join(" "));
}

function renderBookCard(book, keyword) {
  const couponText = book.pricing.coupon
    ? `优惠券：${book.pricing.coupon} 可用`
    : "优惠券：暂无";
  const tagHtml = book.tags.map((tag) => `<span>${highlight(tag, keyword)}</span>`).join("");

  return `
    <article class="product-card" data-sku="${book.id}" data-category="${book.category}" data-level="${book.level}" data-price="${book.pricing.sale_price}" data-rating="${book.rating.score}" data-stock="${book.stock.quantity}" data-sales="${book.sales.total}">
      <div class="product-cover ${coverClass(book.category)}"><span>${initials(book)}</span></div>
      <div class="product-info">
        <p class="product-sku">SKU: ${book.id} | ISBN: ${book.isbn}</p>
        <h3 class="product-title">${highlight(book.title, keyword)}</h3>
        <p class="product-subtitle">${highlight(book.subtitle, keyword)}</p>
        <p class="product-meta">作者：<span class="author">${highlight(book.author.name, keyword)}</span> | 出版社：<span class="publisher">${book.publisher.name}</span></p>
        <p class="product-date">出版日期：<time datetime="${book.publisher.published_at}">${book.publisher.published_at}</time></p>
        <p class="price"><strong>${formatPrice(book.pricing.sale_price)}</strong><del>${formatPrice(book.pricing.list_price)}</del><span>${Math.round(book.pricing.discount * 100) / 10}折</span></p>
        <p class="rating">评分：<b>${book.rating.score}</b> / 5.0，评论 ${book.rating.count} 条</p>
        <p class="stock">库存：${book.stock.status}，${book.stock.warehouse}，${book.stock.quantity} 本</p>
        <p class="coupon">${couponText}</p>
        <div class="tags">${tagHtml}</div>
      </div>
    </article>
  `;
}

function renderDynamicResults(books, keyword) {
  const resultBox = document.querySelector("#dynamicResults");
  const status = document.querySelector("#dynamicStatus");
  const statTotal = document.querySelector("#statTotal");
  const statAvgPrice = document.querySelector("#statAvgPrice");
  const statBestRating = document.querySelector("#statBestRating");
  const statLowStock = document.querySelector("#statLowStock");

  resultBox.innerHTML = books.map((book) => renderBookCard(book, keyword)).join("");

  if (!books.length) {
    status.textContent = "没有找到匹配结果";
    statTotal.textContent = "结果：0";
    statAvgPrice.textContent = "均价：--";
    statBestRating.textContent = "最高评分：--";
    statLowStock.textContent = "低库存：--";
    return;
  }

  const totalPrice = books.reduce((sum, book) => sum + book.pricing.sale_price, 0);
  const bestRating = Math.max(...books.map((book) => book.rating.score));
  const lowStock = books.filter((book) => book.stock.quantity > 0 && book.stock.quantity <= 10).length;

  status.textContent = `已渲染 ${books.length} 条搜索结果`;
  statTotal.textContent = `结果：${books.length}`;
  statAvgPrice.textContent = `均价：${formatPrice(totalPrice / books.length)}`;
  statBestRating.textContent = `最高评分：${bestRating.toFixed(1)}`;
  statLowStock.textContent = `低库存：${lowStock}`;
}

function sortBooks(books, sortBy) {
  const sorted = [...books];
  sorted.sort((a, b) => {
    if (sortBy === "price_asc") return a.pricing.sale_price - b.pricing.sale_price;
    if (sortBy === "price_desc") return b.pricing.sale_price - a.pricing.sale_price;
    if (sortBy === "sales_desc") return b.sales.total - a.sales.total;
    if (sortBy === "newest") return b.publisher.published_at.localeCompare(a.publisher.published_at);
    return b.rating.score - a.rating.score;
  });
  return sorted;
}

function setupDynamicControls(data) {
  const books = data.books;
  const keywordInput = document.querySelector("#keyword");
  const categorySelect = document.querySelector("#dynamicCategory");
  const levelSelect = document.querySelector("#levelFilter");
  const maxPriceInput = document.querySelector("#maxPrice");
  const sortSelect = document.querySelector("#sortBy");
  const searchBtn = document.querySelector("#searchBtn");
  const resetBtn = document.querySelector("#resetBtn");
  const gridViewBtn = document.querySelector("#gridViewBtn");
  const listViewBtn = document.querySelector("#listViewBtn");
  const resultBox = document.querySelector("#dynamicResults");
  const heroTotal = document.querySelector("#heroTotal");

  heroTotal.textContent = books.length;

  data.filters.categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
  });

  data.filters.levels.forEach((level) => {
    const option = document.createElement("option");
    option.value = level;
    option.textContent = level;
    levelSelect.appendChild(option);
  });

  const params = new URLSearchParams(window.location.search);
  const keywordFromUrl = params.get("keyword");
  if (keywordFromUrl) {
    keywordInput.value = keywordFromUrl;
  }

  function runSearch() {
    const keyword = normalize(keywordInput.value);
    const category = categorySelect.value;
    const level = levelSelect.value;
    const maxPrice = Number(maxPriceInput.value || 0);
    const sortBy = sortSelect.value;

    const filtered = books.filter((book) => {
      const matchedKeyword = !keyword || searchableText(book).includes(keyword);
      const matchedCategory = category === "all" || book.category === category;
      const matchedLevel = level === "all" || book.level === level;
      const matchedPrice = !maxPrice || book.pricing.sale_price <= maxPrice;
      return matchedKeyword && matchedCategory && matchedLevel && matchedPrice;
    });

    renderDynamicResults(sortBooks(filtered, sortBy), keyword);
  }

  searchBtn.addEventListener("click", runSearch);
  keywordInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      runSearch();
    }
  });
  [categorySelect, levelSelect, maxPriceInput, sortSelect].forEach((element) => {
    element.addEventListener("input", runSearch);
    element.addEventListener("change", runSearch);
  });

  resetBtn.addEventListener("click", () => {
    keywordInput.value = "";
    categorySelect.value = "all";
    levelSelect.value = "all";
    maxPriceInput.value = "";
    sortSelect.value = data.filters.default_sort;
    runSearch();
  });

  gridViewBtn.addEventListener("click", () => {
    resultBox.classList.remove("is-list");
    gridViewBtn.classList.add("is-active");
    listViewBtn.classList.remove("is-active");
  });

  listViewBtn.addEventListener("click", () => {
    resultBox.classList.add("is-list");
    listViewBtn.classList.add("is-active");
    gridViewBtn.classList.remove("is-active");
  });

  runSearch();
}

async function setupDynamicPage() {
  const status = document.querySelector("#dynamicStatus");
  try {
    const response = await fetch("./sample_books.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    setupDynamicControls(data);
  } catch (error) {
    status.textContent = `数据加载失败：${error.message}`;
  }
}

if (PAGE === "static-books") {
  setupStaticPage();
}

if (PAGE === "dynamic-search") {
  setupDynamicPage();
}
