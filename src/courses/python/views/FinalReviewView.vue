<script setup>
import { computed, onMounted, ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import circleCheckIcon from "../../../assets/lucide-icons/circle-check.svg";
import downloadIcon from "../../../assets/lucide-icons/download.svg";
import fileTextIcon from "../../../assets/lucide-icons/file-text.svg";
import idCardIcon from "../../../assets/lucide-icons/id-card.svg";
import keyRoundIcon from "../../../assets/lucide-icons/key-round.svg";
import shieldCheckIcon from "../../../assets/lucide-icons/shield-check.svg";
import {
  FINAL_REVIEW_PDF_DOWNLOAD_NAME,
  FINAL_REVIEW_PDF_PATH,
  FINAL_REVIEW_STUDENT_IDS_PATH,
  normalizeStudentId,
  parseAllowedStudentIds,
  validateStudentId,
} from "../finalReviewAccess";

const studentId = ref("");
const allowedIds = ref(new Set());
const isLoading = ref(true);
const loadError = ref("");
const validation = ref(null);

const studentIdsHref = encodeURI(FINAL_REVIEW_STUDENT_IDS_PATH);
const reviewPdfHref = encodeURI(FINAL_REVIEW_PDF_PATH);

const canSubmit = computed(() => !isLoading.value && !loadError.value);
const hasAccess = computed(() => validation.value?.ok === true);
const statusClass = computed(() => {
  if (!validation.value) {
    return "";
  }

  return hasAccess.value ? "is-success" : "is-error";
});

function handleStudentIdInput(event) {
  studentId.value = normalizeStudentId(event.target.value);

  if (validation.value && !validation.value.ok) {
    validation.value = null;
  }
}

function checkStudentId() {
  validation.value = validateStudentId(studentId.value, allowedIds.value);
}

onMounted(async () => {
  try {
    const response = await fetch(studentIdsHref, { cache: "no-cache" });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const studentIdText = await response.text();
    const parsedIds = parseAllowedStudentIds(studentIdText);

    if (parsedIds.size === 0) {
      throw new Error("empty student id list");
    }

    allowedIds.value = parsedIds;
  } catch (error) {
    loadError.value = "名单读取失败，请稍后刷新页面再试。";
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="course-page final-review-page">
    <div class="bg-grid" aria-hidden="true"></div>

    <header class="top-nav">
      <a class="brand" href="#top">
        <span class="brand-tag">Final</span>
        <strong>期末复习资料</strong>
      </a>
      <CourseSwitcher />
    </header>

    <main id="top" class="final-review-layout" aria-labelledby="final-review-title">
      <section class="final-review-copy">
        <p class="kicker">PYTHON FINAL REVIEW</p>
        <h1 id="final-review-title">期末复习资料下载</h1>
        <p class="final-review-intro">
          Python编程与科学计算课程复习资料已整理为 PDF。请输入本课程名单内的学号，验证通过后下载。
        </p>
        <ul class="final-review-notes">
          <li>学号只需要输入数字。</li>
          <li>请使用本人学号下载资料。</li>
          <li>如一直无法通过，请先检查学号是否输错。</li>
        </ul>
      </section>

      <section class="access-panel" aria-label="复习资料下载验证">
        <div class="access-panel-head">
          <span class="access-icon" aria-hidden="true">
            <img :src="shieldCheckIcon" alt="" />
          </span>
          <div>
            <p class="access-eyebrow">下载验证</p>
            <h2>输入学号</h2>
          </div>
        </div>

        <form class="student-id-form" @submit.prevent="checkStudentId">
          <label for="student-id-input">学号</label>
          <div class="student-id-control">
            <span class="student-id-icon" aria-hidden="true">
              <img :src="idCardIcon" alt="" />
            </span>
            <input
              id="student-id-input"
              :value="studentId"
              type="text"
              inputmode="numeric"
              autocomplete="off"
              placeholder="请输入学号"
              :disabled="!canSubmit"
              @input="handleStudentIdInput"
            />
          </div>

          <p v-if="isLoading" class="access-status is-muted">名单读取中...</p>
          <p v-else-if="loadError" class="access-status is-error">{{ loadError }}</p>
          <p v-else-if="validation" class="access-status" :class="statusClass">
            {{ validation.message }}
          </p>

          <button class="verify-button" type="submit" :disabled="!canSubmit">
            <img :src="keyRoundIcon" alt="" aria-hidden="true" />
            <span>验证学号</span>
          </button>
        </form>

        <div v-if="hasAccess" class="download-panel" aria-live="polite">
          <div class="download-file">
            <span class="download-file-icon" aria-hidden="true">
              <img :src="fileTextIcon" alt="" />
            </span>
            <div>
              <p>复习资料</p>
              <strong>{{ FINAL_REVIEW_PDF_DOWNLOAD_NAME }}</strong>
            </div>
            <img class="download-ok" :src="circleCheckIcon" alt="" aria-hidden="true" />
          </div>
          <a class="download-action" :href="reviewPdfHref" :download="FINAL_REVIEW_PDF_DOWNLOAD_NAME">
            <img :src="downloadIcon" alt="" aria-hidden="true" />
            <span>下载复习资料</span>
          </a>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.final-review-page {
  min-height: 100vh;
}

.final-review-layout {
  width: min(1080px, calc(100% - 28px));
  min-height: calc(100vh - 132px);
  margin: 32px auto 72px;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
  align-items: center;
  gap: clamp(22px, 4vw, 52px);
}

.final-review-copy {
  display: grid;
  gap: 18px;
}

.final-review-copy h1 {
  margin: 0;
  max-width: 9em;
  color: #10263b;
  font-family: var(--font-serif);
  font-size: 3.8rem;
  line-height: 1.08;
}

.final-review-intro {
  max-width: 680px;
  margin: 0;
  color: #315776;
  font-size: 1.16rem;
}

.final-review-notes {
  display: grid;
  gap: 10px;
  margin: 6px 0 0;
  padding: 0;
  list-style: none;
  color: #345b78;
}

.final-review-notes li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.final-review-notes li::before {
  content: "";
  width: 9px;
  height: 9px;
  margin-top: 10px;
  flex: 0 0 auto;
  border-radius: 999px;
  background: #0f9b6a;
  box-shadow: 0 0 0 5px rgba(15, 155, 106, 0.12);
}

.access-panel {
  width: 100%;
  padding: clamp(22px, 3vw, 34px);
  border: 1px solid rgba(13, 123, 232, 0.16);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-2);
}

.access-panel-head {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
}

.access-icon,
.student-id-icon,
.download-file-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  background: #e7f3ff;
  color: #0d66c2;
}

.access-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
}

.access-icon img,
.student-id-icon img,
.download-file-icon img,
.verify-button img,
.download-action img,
.download-ok {
  width: 20px;
  height: 20px;
}

.access-eyebrow {
  margin: 0;
  color: #0d66c2;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.access-panel h2 {
  margin: 2px 0 0;
  color: #13263a;
  font-size: 1.42rem;
  line-height: 1.24;
}

.student-id-form {
  display: grid;
  gap: 12px;
}

.student-id-form label {
  color: #243d54;
  font-weight: 800;
}

.student-id-control {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  align-items: center;
  min-height: 54px;
  overflow: hidden;
  border: 1px solid rgba(13, 123, 232, 0.2);
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 8px 20px rgba(13, 62, 108, 0.06);
}

.student-id-icon {
  width: 44px;
  height: 100%;
  border-right: 1px solid rgba(13, 123, 232, 0.13);
  border-radius: 0;
}

.student-id-control input {
  width: 100%;
  min-width: 0;
  height: 54px;
  border: 0;
  padding: 0 14px;
  color: #13263a;
  background: transparent;
  font: 800 1.08rem / 1.2 var(--font-sans);
  letter-spacing: 0;
  outline: 0;
}

.student-id-control input::placeholder {
  color: #7b93a9;
  font-weight: 600;
}

.student-id-control:focus-within {
  border-color: rgba(13, 123, 232, 0.55);
  box-shadow: 0 0 0 4px var(--ring);
}

.access-status {
  min-height: 28px;
  margin: 0;
  color: #345b78;
  font-weight: 700;
}

.access-status.is-muted {
  color: #587894;
}

.access-status.is-success {
  color: #0d8158;
}

.access-status.is-error {
  color: #c53232;
}

.verify-button,
.download-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 48px;
  border-radius: 8px;
  font-weight: 900;
  text-decoration: none;
  transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease;
}

.verify-button {
  border: 0;
  color: #ffffff;
  background: #0d7be8;
  box-shadow: 0 12px 24px rgba(13, 123, 232, 0.22);
  cursor: pointer;
}

.verify-button:hover:not(:disabled),
.download-action:hover {
  transform: translateY(-1px);
}

.verify-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.download-panel {
  display: grid;
  gap: 14px;
  margin-top: 22px;
  padding-top: 20px;
  border-top: 1px solid rgba(13, 123, 232, 0.13);
}

.download-file {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr) 24px;
  align-items: center;
  gap: 12px;
}

.download-file-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: #eef8f3;
}

.download-file p,
.download-file strong {
  margin: 0;
}

.download-file p {
  color: #587894;
  font-size: 0.86rem;
  font-weight: 800;
}

.download-file strong {
  display: block;
  overflow-wrap: anywhere;
  color: #13263a;
  line-height: 1.35;
}

.download-ok {
  color: #0f9b6a;
}

.download-action {
  color: #0c442f;
  background: #dff7ed;
  border: 1px solid rgba(15, 155, 106, 0.24);
  box-shadow: 0 12px 24px rgba(15, 155, 106, 0.12);
}

.verify-button:focus-visible,
.download-action:focus-visible {
  outline: 3px solid rgba(13, 123, 232, 0.32);
  outline-offset: 3px;
}

@media (max-width: 980px) {
  .final-review-layout {
    grid-template-columns: 1fr;
    align-items: start;
    min-height: auto;
  }

  .final-review-copy h1 {
    max-width: 100%;
    font-size: 3.2rem;
  }
}

@media (max-width: 560px) {
  .final-review-layout {
    width: min(100% - 20px, 1080px);
    margin-top: 20px;
    margin-bottom: 110px;
  }

  .access-panel {
    padding: 18px;
  }

  .final-review-copy h1 {
    font-size: 2.18rem;
  }
}
</style>
