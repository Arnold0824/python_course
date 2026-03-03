import hljs from "highlight.js/lib/core";
import python from "highlight.js/lib/languages/python";
import javascript from "highlight.js/lib/languages/javascript";
import typescript from "highlight.js/lib/languages/typescript";
import bash from "highlight.js/lib/languages/bash";
import json from "highlight.js/lib/languages/json";
import xml from "highlight.js/lib/languages/xml";
import css from "highlight.js/lib/languages/css";
import sql from "highlight.js/lib/languages/sql";
import yaml from "highlight.js/lib/languages/yaml";
import { nextTick, onMounted, onUnmounted, ref } from "vue";

hljs.registerLanguage("python", python);
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("typescript", typescript);
hljs.registerLanguage("bash", bash);
hljs.registerLanguage("json", json);
hljs.registerLanguage("html", xml);
hljs.registerLanguage("xml", xml);
hljs.registerLanguage("css", css);
hljs.registerLanguage("sql", sql);
hljs.registerLanguage("yaml", yaml);

const CONFIG = {
  copyButtonSelector: ".copy-btn",
  copySourceAttribute: "data-copy",
  toastSelector: "#copyToast",
  progressSelector: "#scrollProgress",
  revealSelector: ".reveal",
  navLinkSelector: ".nav-links a",
  osButtonSelector: ".os-btn",
  osPanelSelector: ".os-panel",
  osTargetAttribute: "data-os-target",
  osPanelAttribute: "data-os-panel",
  activeClass: "is-active",
  revealClass: "is-visible",
  toastDurationMs: 1200,
  navOffset: 140,
  revealThreshold: 0.18,
  copiedMessage: "命令已复制",
  copyFailedMessage: "复制失败，请手动复制",
  slideModeBodyClass: "lesson-slide-mode",
  sidebarBodyClass: "lesson-sidebar-enabled",
  slideDeckSelector: ".page.is-slide-deck",
  slideTransitionLockMs: 700,
  codeSelector: "pre > code",
  codeCopyButtonText: "复制代码",
  codeCopiedMessage: "代码已复制",
  fragmentSelector: ".fragment",
  fragmentVisibleClass: "is-fragment-visible",
  autoTipClass: "auto-knowledge-tip",
  autoTipTitle: "知识提示",
  autoTipTextLengthThreshold: 180,
  autoTipBlockThreshold: 7,
};

function normalizeCodeSource(raw) {
  const normalized = String(raw || "")
    .replace(/^\uFEFF/, "")
    .replace(/[\u200B-\u200D]/g, "")
    .replace(/\u00A0/g, " ")
    .replace(/\r\n?/g, "\n");
  const lines = normalized.split("\n");

  const isBlank = (line) => line.replace(/\uFEFF/g, "").trim() === "";
  while (lines.length && isBlank(lines[0])) lines.shift();
  while (lines.length && isBlank(lines[lines.length - 1])) lines.pop();
  if (!lines.length) return "";

  const indents = lines
    .filter((line) => line.trim() !== "")
    .map((line) => {
      const match = line.match(/^[\t ]+/);
      return match ? match[0].length : 0;
    });
  const minIndent = indents.length ? Math.min(...indents) : 0;
  if (!minIndent) return lines.join("\n");

  return lines.map((line) => line.slice(Math.min(minIndent, line.length))).join("\n");
}

function normalizeCodeLanguage(codeEl) {
  const aliases = {
    py: "python",
    python: "python",
    js: "javascript",
    ts: "typescript",
    sh: "bash",
    shell: "bash",
    yml: "yaml",
    txt: "text",
  };
  const classes = Array.from(codeEl.classList);
  let detected = "";
  for (const cls of classes) {
    if (cls.startsWith("language-")) {
      detected = cls.slice(9).toLowerCase();
      break;
    }
    if (cls.startsWith("lang-")) {
      detected = cls.slice(5).toLowerCase();
      break;
    }
    if (/^[a-z][a-z0-9_-]*$/i.test(cls) && aliases[cls.toLowerCase()]) {
      detected = aliases[cls.toLowerCase()];
      break;
    }
  }
  detected = aliases[detected] || detected || "text";
  if (!codeEl.classList.contains(`language-${detected}`)) {
    codeEl.classList.add(`language-${detected}`);
  }
  return detected;
}

function languageLabel(lang) {
  if (lang === "python") return "Python";
  if (lang === "javascript") return "JavaScript";
  if (lang === "typescript") return "TypeScript";
  if (lang === "bash") return "Bash";
  if (lang === "html") return "HTML";
  if (lang === "css") return "CSS";
  if (lang === "json") return "JSON";
  if (lang === "yaml") return "YAML";
  if (lang === "sql") return "SQL";
  if (lang === "text") return "Text";
  return lang.toUpperCase();
}

function renderCodeHighlight(codeEl, lang, source) {
  const targetLang = lang && lang !== "text" ? lang : "";

  if (targetLang && hljs.getLanguage(targetLang)) {
    const rendered = hljs.highlight(source, {
      language: targetLang,
      ignoreIllegals: true,
    }).value;
    codeEl.innerHTML = rendered;
    codeEl.classList.add("hljs");
    return;
  }

  codeEl.textContent = source;
  codeEl.classList.remove("hljs");
}

function inferAutoTipMessage(label) {
  if (/实战演练/.test(label)) {
    return "先用“输入-处理-输出”三步写草稿，再对照答案检查变量名和输出格式。";
  }
  if (/^任务\s*\d+/.test(label)) {
    return "记住本任务的核心语句与输出模板，至少独立敲一遍再继续下一页。";
  }
  if (/最终挑战|完整代码预览/.test(label)) {
    return "先分步骤运行，再总结每种数据结构在完整程序里的职责。";
  }
  return "用一句话记住定义，并能写出一个最小可运行示例。";
}

export function useLessonDeck(rootRef) {
  const outlineItems = ref([]);
  const activeOutlineIndex = ref(0);

  let cleanupFns = [];
  let revealObserver = null;
  let toastTimer = null;
  let slideLockTimer = null;
  let slideLocked = false;
  let sections = [];
  let topNavEl = null;
  let progressEl = null;
  let navLinks = [];
  let sectionTargets = [];
  let sectionFragments = new Map();

  function addCleanup(fn) {
    cleanupFns.push(fn);
  }

  function addListener(target, type, handler, options) {
    target.addEventListener(type, handler, options);
    addCleanup(() => target.removeEventListener(type, handler, options));
  }

  function showToast(root, text) {
    const toast = root.querySelector(CONFIG.toastSelector);
    if (!toast) return;
    toast.textContent = text;
    toast.classList.add("show");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => {
      toast.classList.remove("show");
    }, CONFIG.toastDurationMs);
  }

  async function copyText(root, text, successMessage = CONFIG.copiedMessage) {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const temp = document.createElement("textarea");
        temp.value = text;
        temp.style.position = "fixed";
        temp.style.opacity = "0";
        document.body.appendChild(temp);
        temp.focus();
        temp.select();
        document.execCommand("copy");
        temp.remove();
      }
      showToast(root, successMessage);
    } catch (error) {
      showToast(root, CONFIG.copyFailedMessage);
    }
  }

  function enhanceCodeBlocks(root) {
    const blocks = root.querySelectorAll(CONFIG.codeSelector);
    blocks.forEach((codeEl) => {
      if (codeEl.dataset.codeEnhanced === "1") return;
      const pre = codeEl.closest("pre");
      if (!pre || !pre.parentElement) return;
      if (pre.parentElement.classList.contains("code-shell")) return;

      const lang = normalizeCodeLanguage(codeEl);
      const source = normalizeCodeSource(codeEl.textContent || "").replace(/^\n+/, "");
      codeEl.textContent = source;
      codeEl.dataset.rawCode = source;
      const shell = document.createElement("div");
      shell.className = "code-shell";

      const toolbar = document.createElement("div");
      toolbar.className = "code-toolbar";

      const langEl = document.createElement("span");
      langEl.className = "code-lang";
      langEl.textContent = languageLabel(lang);

      const copyBtn = document.createElement("button");
      copyBtn.type = "button";
      copyBtn.className = "code-copy-btn";
      copyBtn.textContent = CONFIG.codeCopyButtonText;
      copyBtn.addEventListener("click", () => {
        copyText(root, codeEl.dataset.rawCode || "", CONFIG.codeCopiedMessage);
      });

      toolbar.appendChild(langEl);
      toolbar.appendChild(copyBtn);

      pre.classList.add("code-pre");
      pre.parentElement.insertBefore(shell, pre);
      shell.appendChild(toolbar);
      shell.appendChild(pre);

      renderCodeHighlight(codeEl, lang, source);

      codeEl.dataset.codeEnhanced = "1";
    });
  }

  function bindCopyButtons(root) {
    const buttons = root.querySelectorAll(CONFIG.copyButtonSelector);
    buttons.forEach((button) => {
      const handler = () => {
        const text = button.getAttribute(CONFIG.copySourceAttribute);
        if (text) copyText(root, text);
      };
      button.addEventListener("click", handler);
      addCleanup(() => button.removeEventListener("click", handler));
    });
  }

  function bindOsTabs(root) {
    const osButtons = root.querySelectorAll(CONFIG.osButtonSelector);
    const osPanels = root.querySelectorAll(CONFIG.osPanelSelector);
    osButtons.forEach((button) => {
      const handler = () => {
        const target = button.getAttribute(CONFIG.osTargetAttribute);
        osButtons.forEach((btn) => {
          const isCurrent = btn === button;
          btn.classList.toggle(CONFIG.activeClass, isCurrent);
          btn.setAttribute("aria-selected", String(isCurrent));
        });
        osPanels.forEach((panel) => {
          panel.classList.toggle(CONFIG.activeClass, panel.getAttribute(CONFIG.osPanelAttribute) === target);
        });
      };
      button.addEventListener("click", handler);
      addCleanup(() => button.removeEventListener("click", handler));
    });
  }

  function initReveal(root) {
    const revealItems = root.querySelectorAll(CONFIG.revealSelector);
    if (!revealItems.length) return;

    if ("IntersectionObserver" in window) {
      revealObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add(CONFIG.revealClass);
              revealObserver.unobserve(entry.target);
            }
          });
        },
        { threshold: CONFIG.revealThreshold }
      );
      revealItems.forEach((item) => revealObserver.observe(item));
      addCleanup(() => revealObserver && revealObserver.disconnect());
      return;
    }
    revealItems.forEach((item) => item.classList.add(CONFIG.revealClass));
  }

  function initAutoTips(root) {
    const richSelectors =
      "pre, .code-shell, table, .concept-grid, .command-layout, .mirror-grid, .pitfall-grid, .timeline, .goal-cards, .ops-table";
    const sectionNodes = root.querySelectorAll(".page.is-slide-deck > .hero, .page.is-slide-deck > .section");
    sectionNodes.forEach((section, index) => {
      if (section.classList.contains("hero")) return;
      if (section.getAttribute("data-auto-tip") === "off") return;
      const body = section.querySelector(".slide-card-body") || section;
      if (!body) return;
      if (body.querySelector(`.${CONFIG.autoTipClass}`)) return;
      if (body.querySelector(richSelectors)) return;

      const textLength = (body.textContent || "").replace(/\s+/g, "").length;
      const blockCount = body.querySelectorAll("p, li, ol, ul, blockquote").length;
      if (textLength > CONFIG.autoTipTextLengthThreshold) return;
      if (blockCount > CONFIG.autoTipBlockThreshold) return;

      const rawLabel = section.getAttribute("data-outline-label") || "";
      const heading = section.querySelector("h1, h2, h3");
      const label = (rawLabel || (heading && heading.textContent) || `卡片 ${index + 1}`).trim();

      const tip = document.createElement("div");
      tip.className = CONFIG.autoTipClass;
      tip.setAttribute("role", "note");

      const title = document.createElement("span");
      title.className = "label";
      title.textContent = CONFIG.autoTipTitle;

      const text = document.createElement("p");
      text.textContent = inferAutoTipMessage(label);

      tip.appendChild(title);
      tip.appendChild(text);
      body.appendChild(tip);
    });
  }

  function ensureSlideBodies() {
    sections.forEach((section) => {
      const first = section.firstElementChild;
      if (first && first.classList.contains("slide-card-body")) return;

      const body = document.createElement("div");
      body.className = "slide-card-body";
      while (section.firstChild) {
        body.appendChild(section.firstChild);
      }
      section.appendChild(body);
    });
  }

  function initFragments() {
    sectionFragments = new Map();
    sections.forEach((section, index) => {
      const fragments = Array.from(section.querySelectorAll(CONFIG.fragmentSelector));
      if (!fragments.length) return;
      fragments.forEach((frag) => {
        frag.classList.remove("visible");
        frag.classList.remove("current-fragment");
        frag.classList.remove(CONFIG.fragmentVisibleClass);
      });
      sectionFragments.set(index, fragments);
    });
  }

  function parseOutlineLevel(section) {
    const raw = Number(section.getAttribute("data-outline-level") || "1");
    if (!Number.isFinite(raw)) return 1;
    return Math.min(6, Math.max(1, Math.round(raw)));
  }

  function resolveOutlineLabel(section, index) {
    const custom = section.getAttribute("data-outline-label");
    if (custom && custom.trim()) return custom.trim();
    const heading = section.querySelector("h2, h1, h3");
    if (heading && heading.textContent) return heading.textContent.trim();
    return `卡片 ${index + 1}`;
  }

  function buildOutline() {
    const counters = [];
    outlineItems.value = sections.map((section, index) => {
      const level = parseOutlineLevel(section);
      counters[level - 1] = (counters[level - 1] || 0) + 1;
      counters.length = level;
      return {
        index,
        level,
        number: counters.join("."),
        label: resolveOutlineLabel(section, index),
      };
    });
  }

  function syncSlideNavOffset() {
    if (!topNavEl) return;
    const offset = topNavEl.offsetHeight + 10;
    document.documentElement.style.setProperty("--slide-nav-offset", `${offset}px`);
  }

  function updateProgress() {
    if (!progressEl) return;
    const scrollTop = window.scrollY;
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    const rate = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    progressEl.style.width = `${rate}%`;
  }

  function activateTopNav() {
    if (!navLinks.length || !sectionTargets.length) return;
    const marker = window.scrollY + CONFIG.navOffset;
    let activeId = "";
    sectionTargets.forEach((section) => {
      if (section.offsetTop <= marker) activeId = `#${section.id}`;
    });
    navLinks.forEach((link) => {
      link.classList.toggle(CONFIG.activeClass, link.getAttribute("href") === activeId);
    });
  }

  function getClosestSlideIndex() {
    const marker = window.scrollY + (topNavEl ? topNavEl.offsetHeight + 12 : CONFIG.navOffset);
    let closestIndex = 0;
    let closestDistance = Number.POSITIVE_INFINITY;
    sections.forEach((section, index) => {
      const distance = Math.abs(section.offsetTop - marker);
      if (distance < closestDistance) {
        closestDistance = distance;
        closestIndex = index;
      }
    });
    return closestIndex;
  }

  function updateActiveOutline() {
    activeOutlineIndex.value = getClosestSlideIndex();
  }

  function resetSlideCardScroll(index) {
    const section = sections[index];
    if (!section) return;
    const body = section.querySelector(".slide-card-body");
    if (body) body.scrollTop = 0;
  }

  function canScrollInsideCard(target, deltaY) {
    const root = rootRef.value;
    if (!root || !(target instanceof Element)) return false;
    let node = target;
    while (node && node !== root && node !== document.body) {
      if (node.classList && node.classList.contains("slide-card-body")) {
        const maxScroll = node.scrollHeight - node.clientHeight;
        if (maxScroll <= 1) return false;
        if (deltaY > 0) return node.scrollTop < maxScroll - 1;
        return node.scrollTop > 1;
      }
      node = node.parentElement;
    }
    return false;
  }

  function jumpToSlide(index) {
    if (!sections.length) return;
    const safe = Math.max(0, Math.min(index, sections.length - 1));
    resetSlideCardScroll(safe);
    sections[safe].scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function jumpSlide(direction) {
    if (slideLocked || !sections.length) return;
    const current = getClosestSlideIndex();
    const fragments = sectionFragments.get(current) || [];

    if (direction > 0 && fragments.length) {
      const next = fragments.find((item) => !item.classList.contains(CONFIG.fragmentVisibleClass));
      if (next) {
        next.classList.add(CONFIG.fragmentVisibleClass);
        return;
      }
    }
    if (direction < 0 && fragments.length) {
      const visible = fragments.filter((item) => item.classList.contains(CONFIG.fragmentVisibleClass));
      if (visible.length) {
        visible[visible.length - 1].classList.remove(CONFIG.fragmentVisibleClass);
        return;
      }
    }

    slideLocked = true;
    const target =
      direction > 0 ? Math.min(current + 1, sections.length - 1) : Math.max(current - 1, 0);
    if (target !== current) {
      resetSlideCardScroll(target);
      sections[target].scrollIntoView({ behavior: "smooth", block: "start" });
    }
    window.clearTimeout(slideLockTimer);
    slideLockTimer = window.setTimeout(() => {
      slideLocked = false;
    }, CONFIG.slideTransitionLockMs);
  }

  function initSlideDeck(root) {
    const slideDeck = root.querySelector(CONFIG.slideDeckSelector);
    if (!slideDeck) return false;

    sections = Array.from(slideDeck.children).filter((item) => item.matches(".hero, .section"));
    if (!sections.length) return false;

    document.body.classList.add(CONFIG.slideModeBodyClass, CONFIG.sidebarBodyClass);
    topNavEl = root.querySelector(".top-nav");
    progressEl = root.querySelector(CONFIG.progressSelector);
    navLinks = Array.from(root.querySelectorAll(CONFIG.navLinkSelector));
    sectionTargets = navLinks
      .map((link) => {
        const target = link.getAttribute("href");
        return target ? root.querySelector(target) : null;
      })
      .filter(Boolean);

    ensureSlideBodies();
    enhanceCodeBlocks(slideDeck);
    initAutoTips(root);
    initFragments();
    buildOutline();
    syncSlideNavOffset();
    updateProgress();
    activateTopNav();
    updateActiveOutline();

    addListener(window, "resize", syncSlideNavOffset, { passive: true });
    addListener(
      window,
      "scroll",
      () => {
        updateProgress();
        activateTopNav();
        updateActiveOutline();
      },
      { passive: true }
    );
    addListener(
      window,
      "wheel",
      (event) => {
        if (Math.abs(event.deltaY) < 24) return;
        if (canScrollInsideCard(event.target, event.deltaY)) return;
        event.preventDefault();
        jumpSlide(event.deltaY > 0 ? 1 : -1);
      },
      { passive: false }
    );
    addListener(window, "keydown", (event) => {
      if (event.defaultPrevented) return;
      const tag = (event.target && event.target.tagName) || "";
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (event.key === "ArrowDown" || event.key === "PageDown" || event.key === " ") {
        event.preventDefault();
        jumpSlide(1);
      }
      if (event.key === "ArrowUp" || event.key === "PageUp") {
        event.preventDefault();
        jumpSlide(-1);
      }
    });
    return true;
  }

  function cleanup() {
    cleanupFns.forEach((fn) => {
      try {
        fn();
      } catch (error) {
        // ignore
      }
    });
    cleanupFns = [];
    if (revealObserver) {
      revealObserver.disconnect();
      revealObserver = null;
    }
    window.clearTimeout(toastTimer);
    window.clearTimeout(slideLockTimer);
    toastTimer = null;
    slideLockTimer = null;
    slideLocked = false;
    sections = [];
    sectionFragments = new Map();
    outlineItems.value = [];
    activeOutlineIndex.value = 0;
    document.body.classList.remove(CONFIG.slideModeBodyClass, CONFIG.sidebarBodyClass);
  }

  onMounted(async () => {
    await nextTick();
    const root = rootRef.value;
    if (!root) return;
    bindCopyButtons(root);
    bindOsTabs(root);
    initReveal(root);
    const hasSlideDeck = initSlideDeck(root);
    if (!hasSlideDeck) {
      enhanceCodeBlocks(root);
    }
  });

  onUnmounted(() => {
    cleanup();
  });

  return {
    outlineItems,
    activeOutlineIndex,
    jumpToSlide,
  };
}
