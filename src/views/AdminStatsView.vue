<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import { fetchAnalyticsDashboard } from "../services/adminAnalytics";

const TOKEN_STORAGE_KEY = "python-course-admin-token";

const adminToken = ref("");
const days = ref(14);
const limit = ref(50);
const isLoading = ref(false);
const errorMessage = ref("");
const dashboard = ref(null);
const lastLoadedAt = ref("");

const totalViews = computed(() => Number(dashboard.value?.overview?.totalViews || 0));
const uniqueSessions = computed(() => Number(dashboard.value?.overview?.uniqueSessions || 0));
const recentViews = computed(() => dashboard.value?.recentViews || []);
const chapterViews = computed(() => dashboard.value?.overview?.chapters || []);
const pathViews = computed(() => dashboard.value?.overview?.paths || []);
const dailyViews = computed(() => dashboard.value?.dailyViews || []);
const maxDailyViews = computed(() => {
  const values = dailyViews.value.map((item) => Number(item.views || 0));
  return Math.max(1, ...values);
});

function loadStoredToken() {
  adminToken.value = localStorage.getItem(TOKEN_STORAGE_KEY) || "";
}

function persistToken() {
  const value = adminToken.value.trim();
  if (value) {
    localStorage.setItem(TOKEN_STORAGE_KEY, value);
    return;
  }

  localStorage.removeItem(TOKEN_STORAGE_KEY);
}

function formatDateTime(value) {
  if (!value) {
    return "-";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }

  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function formatShortDate(value) {
  if (!value) {
    return "-";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }

  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}

async function refreshDashboard() {
  errorMessage.value = "";
  persistToken();

  if (!adminToken.value.trim()) {
    errorMessage.value = "请输入管理员令牌后再加载统计数据。";
    dashboard.value = null;
    return;
  }

  isLoading.value = true;
  try {
    dashboard.value = await fetchAnalyticsDashboard({
      token: adminToken.value,
      days: days.value,
      limit: limit.value,
    });
    lastLoadedAt.value = formatDateTime(new Date().toISOString());
  } catch (error) {
    errorMessage.value = error.message || "加载统计数据失败。";
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  loadStoredToken();
  if (adminToken.value) {
    void refreshDashboard();
  }
});
</script>

<template>
  <div class="admin-page">
    <div class="bg-orb orb-a" aria-hidden="true"></div>
    <div class="bg-orb orb-b" aria-hidden="true"></div>
    <div class="bg-grid" aria-hidden="true"></div>

    <header class="admin-topbar">
      <div>
        <p class="admin-kicker">统计后台</p>
        <h1>访问流量与章节热度</h1>
        <p class="admin-intro">
          查看总访问量、独立会话、章节热度、页面排行和最近访问记录。
        </p>
      </div>
      <div class="admin-actions">
        <RouterLink class="ghost-link" to="/chapter/1">返回课程</RouterLink>
        <button class="primary-btn" type="button" :disabled="isLoading" @click="refreshDashboard">
          {{ isLoading ? "加载中..." : "刷新数据" }}
        </button>
      </div>
    </header>

    <main class="admin-main">
      <section class="panel control-panel">
        <div class="control-header">
          <div>
            <h2>连接设置</h2>
            <p>管理员令牌会保存在当前浏览器的本地存储中。</p>
          </div>
          <p class="sync-note">上次刷新：{{ lastLoadedAt || "尚未刷新" }}</p>
        </div>

        <div class="control-grid">
          <label class="field">
            <span>管理员令牌</span>
            <input
              v-model="adminToken"
              type="password"
              placeholder="输入 ADMIN_TOKEN"
              autocomplete="off"
            />
          </label>

          <label class="field">
            <span>统计天数</span>
            <select v-model.number="days">
              <option :value="7">最近 7 天</option>
              <option :value="14">最近 14 天</option>
              <option :value="30">最近 30 天</option>
              <option :value="60">最近 60 天</option>
            </select>
          </label>

          <label class="field">
            <span>最近记录条数</span>
            <select v-model.number="limit">
              <option :value="20">20 条</option>
              <option :value="50">50 条</option>
              <option :value="100">100 条</option>
            </select>
          </label>
        </div>

        <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>
      </section>

      <section class="stats-grid">
        <article class="stat-card">
          <span class="stat-label">总访问量</span>
          <strong>{{ totalViews }}</strong>
        </article>
        <article class="stat-card">
          <span class="stat-label">独立会话</span>
          <strong>{{ uniqueSessions }}</strong>
        </article>
        <article class="stat-card">
          <span class="stat-label">章节数</span>
          <strong>{{ chapterViews.length }}</strong>
        </article>
        <article class="stat-card">
          <span class="stat-label">已统计页面</span>
          <strong>{{ pathViews.length }}</strong>
        </article>
      </section>

      <section class="dashboard-grid">
        <article class="panel chart-panel">
          <div class="panel-head">
            <h2>最近访问走势</h2>
            <span>{{ days }} 天</span>
          </div>
          <div v-if="dailyViews.length" class="bar-chart">
            <div v-for="item in dailyViews" :key="item.viewDate" class="bar-row">
              <span class="bar-label">{{ formatShortDate(item.viewDate) }}</span>
              <div class="bar-track">
                <span
                  class="bar-fill"
                  :style="{ width: `${(Number(item.views || 0) / maxDailyViews) * 100}%` }"
                ></span>
              </div>
              <strong class="bar-value">{{ item.views }}</strong>
            </div>
          </div>
          <p v-else class="empty-state">暂无访问数据。</p>
        </article>

        <article class="panel ranking-panel">
          <div class="panel-head">
            <h2>章节热度</h2>
            <span>Top {{ chapterViews.length }}</span>
          </div>
          <ol v-if="chapterViews.length" class="ranking-list">
            <li v-for="item in chapterViews" :key="item.chapterId || 'unknown'">
              <span>{{ item.chapterId || "未标记章节" }}</span>
              <strong>{{ item.views }}</strong>
            </li>
          </ol>
          <p v-else class="empty-state">暂无章节统计。</p>
        </article>

        <article class="panel ranking-panel">
          <div class="panel-head">
            <h2>页面排行</h2>
            <span>Top {{ pathViews.length }}</span>
          </div>
          <ol v-if="pathViews.length" class="ranking-list path-list">
            <li v-for="item in pathViews" :key="item.path">
              <span>{{ item.path }}</span>
              <strong>{{ item.views }}</strong>
            </li>
          </ol>
          <p v-else class="empty-state">暂无页面排行。</p>
        </article>
      </section>

      <section class="panel table-panel">
        <div class="panel-head">
          <h2>最近访问记录</h2>
          <span>{{ recentViews.length }} 条</span>
        </div>
        <div v-if="recentViews.length" class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>时间</th>
                <th>章节</th>
                <th>页面</th>
                <th>来源</th>
                <th>会话</th>
                <th>IP</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in recentViews" :key="item.id">
                <td>{{ formatDateTime(item.createdAt) }}</td>
                <td>{{ item.chapterId || "-" }}</td>
                <td class="mono">{{ item.path }}</td>
                <td class="mono">{{ item.referrer || "-" }}</td>
                <td class="mono">{{ item.sessionId }}</td>
                <td class="mono">{{ item.ipAddress || "-" }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="empty-state">暂无最近访问记录。</p>
      </section>
    </main>
  </div>
</template>

<style scoped>
.admin-page {
  min-height: 100vh;
  padding: 28px 20px 72px;
}

.admin-topbar,
.admin-main {
  width: min(1180px, calc(100% - 8px));
  margin: 0 auto;
}

.admin-topbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 22px;
}

.admin-kicker {
  margin: 0 0 8px;
  color: #0a62be;
  font-size: 0.76rem;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.admin-topbar h1 {
  margin: 0;
  font-size: clamp(1.8rem, 3.6vw, 2.7rem);
}

.admin-intro {
  margin: 10px 0 0;
  max-width: 700px;
  color: var(--text-secondary);
}

.admin-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.ghost-link,
.primary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 16px;
  border-radius: 999px;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
}

.ghost-link {
  border: 1px solid rgba(13, 123, 232, 0.22);
  color: #0a62be;
  background: rgba(255, 255, 255, 0.92);
}

.primary-btn {
  border: 0;
  color: #fff;
  background: linear-gradient(135deg, #0d7be8, #11a982);
}

.primary-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

.ghost-link:hover,
.primary-btn:hover {
  transform: translateY(-1px);
}

.admin-main {
  display: grid;
  gap: 18px;
}

.panel {
  padding: 18px;
  border-radius: 18px;
  border: 1px solid rgba(13, 123, 232, 0.14);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-1);
}

.control-header,
.panel-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.control-header h2,
.panel-head h2 {
  margin: 0;
  font-size: 1.2rem;
}

.control-header p,
.sync-note {
  margin: 6px 0 0;
  color: var(--text-secondary);
}

.sync-note,
.panel-head span {
  color: #53708d;
  font-size: 0.9rem;
}

.control-grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 14px;
}

.field {
  display: grid;
  gap: 7px;
}

.field span {
  font-size: 0.9rem;
  font-weight: 700;
  color: #385a74;
}

.field input,
.field select {
  min-height: 44px;
  border-radius: 12px;
  border: 1px solid rgba(13, 123, 232, 0.18);
  padding: 0 14px;
  background: #fff;
  color: var(--text-primary);
  font: inherit;
}

.field input:focus,
.field select:focus {
  outline: 2px solid rgba(13, 123, 232, 0.18);
  border-color: rgba(13, 123, 232, 0.4);
}

.error-banner {
  margin: 14px 0 0;
  padding: 11px 14px;
  border-radius: 12px;
  color: #8d1f1f;
  background: rgba(214, 53, 53, 0.1);
  border: 1px solid rgba(214, 53, 53, 0.18);
}

.stats-grid,
.dashboard-grid {
  display: grid;
  gap: 18px;
}

.stats-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.stat-card {
  padding: 18px;
  border-radius: 16px;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.96), rgba(232, 244, 255, 0.92));
  border: 1px solid rgba(13, 123, 232, 0.14);
  box-shadow: var(--shadow-1);
}

.stat-label {
  display: block;
  margin-bottom: 8px;
  color: #5d7891;
  font-size: 0.88rem;
  font-weight: 700;
}

.stat-card strong {
  font-size: clamp(1.5rem, 2.2vw, 2rem);
  color: #0a62be;
}

.dashboard-grid {
  grid-template-columns: 1.6fr 1fr 1fr;
}

.bar-chart {
  margin-top: 14px;
  display: grid;
  gap: 12px;
}

.bar-row {
  display: grid;
  grid-template-columns: 62px 1fr 48px;
  gap: 12px;
  align-items: center;
}

.bar-label,
.bar-value {
  font-size: 0.9rem;
}

.bar-track {
  height: 12px;
  border-radius: 999px;
  background: rgba(13, 123, 232, 0.08);
  overflow: hidden;
}

.bar-fill {
  display: block;
  height: 100%;
  min-width: 6px;
  border-radius: inherit;
  background: linear-gradient(90deg, #0d7be8, #11a982);
}

.ranking-list {
  list-style: none;
  margin: 14px 0 0;
  padding: 0;
  display: grid;
  gap: 10px;
}

.ranking-list li {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 12px;
  background: rgba(13, 123, 232, 0.05);
}

.ranking-list span {
  color: var(--text-primary);
  word-break: break-word;
}

.ranking-list strong {
  color: #0a62be;
  flex-shrink: 0;
}

.path-list span {
  font-family: var(--font-mono);
  font-size: 0.84rem;
}

.table-wrap {
  margin-top: 14px;
  overflow: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 860px;
}

th,
td {
  padding: 12px 10px;
  border-bottom: 1px solid rgba(13, 123, 232, 0.1);
  text-align: left;
  vertical-align: top;
}

th {
  font-size: 0.84rem;
  color: #54708a;
}

td {
  font-size: 0.92rem;
}

.mono {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  word-break: break-all;
}

.empty-state {
  margin: 18px 0 0;
  color: var(--text-secondary);
}

@media (max-width: 1080px) {
  .stats-grid,
  .dashboard-grid,
  .control-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 720px) {
  .admin-page {
    padding: 18px 12px 72px;
  }

  .admin-topbar,
  .control-header,
  .panel-head,
  .stats-grid,
  .dashboard-grid,
  .control-grid {
    grid-template-columns: 1fr;
  }

  .admin-topbar,
  .control-header,
  .panel-head {
    display: grid;
  }

  .bar-row {
    grid-template-columns: 56px 1fr 42px;
    gap: 8px;
  }
}
</style>
