<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import { fetchCarlaLeaderboard } from "../../../services/carlaLeaderboard";

const reportTemplateHref =
  "/courses/carla/final/2%20%E5%AE%9E%E8%AE%AD%E8%AF%BE%E7%A8%8B%E6%8A%A5%E5%91%8A-%E5%AD%A6%E5%8F%B7%E5%A7%93%E5%90%8D-%E8%AF%BE%E7%A8%8B%E8%AE%BE%E8%AE%A1%E9%A1%B9%E7%9B%AE%E5%90%8D%E7%A7%B0-%E4%B8%AA%E4%BA%BA.docx";
const codePackageHref = "/courses/carla/final/carla_safety_race_template.zip";
const wpsSubmitHref = "https://f.wps.cn/g/zjfA9ogS/";

const limit = ref(50);
const isLoading = ref(false);
const errorMessage = ref("");
const entries = ref([]);
const lastLoadedAt = ref("");

const bestScore = computed(() => entries.value[0]?.finalScore ?? 0);
const completedCount = computed(() => entries.value.filter((entry) => entry.completed).length);
const bestDistance = computed(() => entries.value[0]?.distanceTraveledM ?? 0);
const submittedCount = computed(() =>
  entries.value.reduce((total, entry) => total + Number(entry.submissionCount || 0), 0),
);

function formatScore(value) {
  const number = Number(value || 0);
  return number.toFixed(Number.isInteger(number) ? 0 : 2);
}

function formatDistance(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  return `${Number(value).toFixed(1)} m`;
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
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

async function refreshLeaderboard() {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const data = await fetchCarlaLeaderboard({ limit: limit.value });
    entries.value = data.entries || [];
    lastLoadedAt.value = formatDateTime(new Date().toISOString());
  } catch (error) {
    entries.value = [];
    errorMessage.value = error.message || "排行榜加载失败。";
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  void refreshLeaderboard();
});
</script>

<template>
  <div class="leaderboard-page">
    <header class="leaderboard-topbar">
      <div>
        <p class="kicker">CARLA FINAL RACE</p>
        <h1>期末安全竞速排行榜</h1>
        <p class="intro">
          每个学号只展示最佳成绩。60 秒内沿固定路线推进越远分数越高，排序依次比较最终成绩、是否跑完全程、扣分和提交时间。
        </p>
      </div>
      <div class="topbar-actions">
        <CourseSwitcher />
        <RouterLink class="secondary-link" to="/carla/chapter/5">返回课程</RouterLink>
      </div>
    </header>

    <main class="leaderboard-main">
      <section class="download-strip" aria-label="期末材料下载">
        <div>
          <h2>期末材料</h2>
          <p>下载统一代码包和实训报告模板，完成后通过 WPS 链接提交。</p>
        </div>
        <div class="download-actions">
          <a
            class="download-link"
            :href="reportTemplateHref"
            download="2 实训课程报告-学号姓名-课程设计项目名称-个人.docx"
          >
            实训报告模板
          </a>
          <a
            class="download-link is-primary"
            :href="codePackageHref"
            download="carla_safety_race_template.zip"
          >
            代码包
          </a>
          <a
            class="download-link is-submit"
            :href="wpsSubmitHref"
            target="_blank"
            rel="noopener noreferrer"
          >
            WPS 提交
          </a>
        </div>
      </section>

      <section class="assignment-card" aria-label="期末大作业说明">
        <div class="assignment-header">
          <div>
            <p class="kicker">FINAL PROJECT</p>
            <h2>基于 CARLA 的自动驾驶安全竞速挑战</h2>
          </div>
          <p>
            在教师统一模板内改进自动驾驶策略，主程序会固定地图、路线、车辆、行人、随机种子、计时和扣分规则。主要修改 `src/student_policy.py`，不得修改固定地图、路线、车辆和行人数量，也不得绕过事件检测和评分接口。
          </p>
        </div>

        <div class="assignment-steps">
          <div>
            <h3>要做什么</h3>
            <ul>
              <li>让主车在固定路线中尽可能安全、稳定、连续推进。</li>
              <li>处理红灯、障碍物、弯道、偏航、停滞脱困和速度控制。</li>
              <li>保留自动输出的成绩页、事件日志、轨迹日志和成绩报告。</li>
            </ul>
          </div>
          <div>
            <h3>如何运行</h3>
            <ul>
              <li>下载代码包，启动 CARLA 后运行 `python src/run_challenge.py`。</li>
              <li>开场弹窗输入学号姓名，结束成绩会自动尝试提交排行榜。</li>
              <li>至少两次有效运行，对比距离、扣分、事件数量和最终成绩。</li>
            </ul>
          </div>
          <div>
            <h3>如何算分</h3>
            <ul>
              <li>脚本成绩采用 60 秒距离挑战，60 秒内有效路线距离越远越高。</li>
              <li>距离分按 1 m = 1 分计算，最终成绩为距离分减去安全扣分。</li>
              <li>碰撞、闯红灯、偏离路线、压线、超速和长时间停滞都会扣分。</li>
            </ul>
          </div>
        </div>

        <div class="rubric-grid" aria-label="课程评分表">
          <div>
            <strong>系统功能设计与实现</strong>
            <span>40 分</span>
            <p>策略有效、稳定运行、事件检测与成绩输出完整。</p>
          </div>
          <div>
            <strong>工程规范与模板扩展</strong>
            <span>30 分</span>
            <p>结构清晰，模板与个人改动边界明确，可复现、可维护。</p>
          </div>
          <div>
            <strong>报告与数据分析质量</strong>
            <span>20 分</span>
            <p>报告说明规则、关键代码、输出文件，并分析多次运行数据。</p>
          </div>
          <div>
            <strong>展示答辩与个人说明</strong>
            <span>10 分</span>
            <p>能现场演示并解释策略、扣分、结果和改进思路。</p>
          </div>
        </div>
      </section>

      <section class="summary-band" aria-label="排行榜概览">
        <div>
          <span>当前最高分</span>
          <strong>{{ formatScore(bestScore) }}</strong>
        </div>
        <div>
          <span>最高有效距离</span>
          <strong>{{ formatDistance(bestDistance) }}</strong>
        </div>
        <div>
          <span>跑完全程人数</span>
          <strong>{{ completedCount }}</strong>
        </div>
        <div>
          <span>总提交次数</span>
          <strong>{{ submittedCount }}</strong>
        </div>
      </section>

      <section class="toolbar" aria-label="排行榜操作">
        <div>
          <h2>成绩列表</h2>
          <p>上次刷新：{{ lastLoadedAt || "尚未刷新" }}</p>
        </div>
        <div class="toolbar-actions">
          <label>
            显示数量
            <select v-model.number="limit" :disabled="isLoading" @change="refreshLeaderboard">
              <option :value="20">前 20 名</option>
              <option :value="50">前 50 名</option>
              <option :value="100">前 100 名</option>
            </select>
          </label>
          <button type="button" :disabled="isLoading" @click="refreshLeaderboard">
            {{ isLoading ? "加载中..." : "刷新" }}
          </button>
        </div>
      </section>

      <p v-if="errorMessage" class="state-message is-error">{{ errorMessage }}</p>
      <p v-else-if="isLoading && !entries.length" class="state-message">正在加载排行榜...</p>
      <p v-else-if="!entries.length" class="state-message">暂无提交记录。</p>

      <section v-else class="table-wrap" aria-label="CARLA 成绩排行榜">
        <table>
          <thead>
            <tr>
              <th>名次</th>
              <th>学号</th>
              <th>姓名</th>
              <th>最终成绩</th>
              <th>有效距离</th>
              <th>扣分</th>
              <th>跑完全程</th>
              <th>提交次数</th>
              <th>最佳提交时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in entries" :key="entry.studentId">
              <td class="rank-cell">#{{ entry.rank }}</td>
              <td>{{ entry.studentId }}</td>
              <td>{{ entry.studentName }}</td>
              <td class="score-cell">{{ formatScore(entry.finalScore) }}</td>
              <td>{{ formatDistance(entry.distanceTraveledM) }}</td>
              <td>{{ formatScore(entry.penaltyPoints) }}</td>
              <td>
                <span class="status-pill" :class="{ 'is-complete': entry.completed }">
                  {{ entry.completed ? "完成" : "未完成" }}
                </span>
              </td>
              <td>{{ entry.submissionCount }}</td>
              <td>{{ formatDateTime(entry.bestSubmittedAt) }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </main>
  </div>
</template>

<style scoped>
.leaderboard-page {
  min-height: 100vh;
  padding: 32px min(5vw, 72px) calc(var(--beian-bar-height) + 48px);
  color: #172033;
  background: #f6f8fb;
}

.leaderboard-topbar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  max-width: 1180px;
  margin: 0 auto 28px;
}

.kicker {
  margin: 0 0 8px;
  color: #0f6ac5;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0;
}

h1 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3.2rem);
  line-height: 1.08;
}

.intro {
  max-width: 760px;
  margin: 14px 0 0;
  color: #52657a;
  line-height: 1.75;
}

.topbar-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 14px;
}

.secondary-link,
button {
  border: 1px solid rgba(13, 123, 232, 0.22);
  border-radius: 8px;
  padding: 10px 16px;
  background: #ffffff;
  color: #0f5ea8;
  font-weight: 800;
  text-decoration: none;
}

button {
  cursor: pointer;
}

button:disabled,
select:disabled {
  cursor: wait;
  opacity: 0.65;
}

.leaderboard-main {
  max-width: 1180px;
  margin: 0 auto;
}

.download-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
  padding: 18px 20px;
  border: 1px solid rgba(15, 106, 197, 0.12);
  border-radius: 8px;
  background: #ffffff;
}

.download-strip h2 {
  margin: 0 0 6px;
  font-size: 1.1rem;
}

.download-strip p {
  margin: 0;
  color: #637489;
}

.download-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
}

.download-link {
  border: 1px solid rgba(13, 123, 232, 0.22);
  border-radius: 8px;
  padding: 10px 14px;
  background: #ffffff;
  color: #0f5ea8;
  font-weight: 800;
  text-decoration: none;
  white-space: nowrap;
}

.download-link.is-primary {
  border-color: #0f6ac5;
  background: #0f6ac5;
  color: #ffffff;
}

.download-link.is-submit {
  border-color: rgba(12, 132, 93, 0.35);
  background: #0c845d;
  color: #ffffff;
}

.assignment-card {
  margin-bottom: 22px;
  padding: 22px;
  border: 1px solid rgba(23, 32, 51, 0.1);
  border-radius: 8px;
  background: #ffffff;
}

.assignment-header {
  display: grid;
  grid-template-columns: minmax(260px, 0.8fr) minmax(0, 1.2fr);
  gap: 22px;
  align-items: start;
  margin-bottom: 18px;
}

.assignment-header h2 {
  margin: 0;
  font-size: 1.55rem;
  line-height: 1.25;
}

.assignment-header p {
  margin: 0;
  color: #52657a;
  line-height: 1.8;
}

.assignment-steps {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.assignment-steps > div {
  min-height: 196px;
  padding: 16px;
  border: 1px solid rgba(23, 32, 51, 0.08);
  border-radius: 8px;
  background: #f9fbfd;
}

.assignment-steps h3 {
  margin: 0 0 10px;
  font-size: 1rem;
}

.assignment-steps ul {
  display: grid;
  gap: 8px;
  margin: 0;
  padding-left: 18px;
  color: #52657a;
  line-height: 1.65;
}

.rubric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1px;
  overflow: hidden;
  margin-top: 16px;
  border: 1px solid rgba(180, 87, 34, 0.14);
  border-radius: 8px;
  background: rgba(180, 87, 34, 0.14);
}

.rubric-grid div {
  padding: 16px;
  background: #fffdfa;
}

.rubric-grid strong,
.rubric-grid span {
  display: block;
}

.rubric-grid strong {
  min-height: 46px;
  color: #172033;
  line-height: 1.4;
}

.rubric-grid span {
  margin-top: 8px;
  color: #b45722;
  font-size: 1.35rem;
  font-weight: 900;
}

.rubric-grid p {
  margin: 8px 0 0;
  color: #637489;
  line-height: 1.6;
}

.summary-band {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1px;
  overflow: hidden;
  border: 1px solid rgba(15, 106, 197, 0.12);
  border-radius: 8px;
  background: rgba(15, 106, 197, 0.12);
}

.summary-band div {
  min-height: 104px;
  padding: 18px;
  background: #ffffff;
}

.summary-band span {
  display: block;
  color: #607187;
  font-size: 0.9rem;
}

.summary-band strong {
  display: block;
  margin-top: 10px;
  font-size: 2rem;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin: 24px 0 12px;
}

.toolbar h2 {
  margin: 0 0 6px;
  font-size: 1.35rem;
}

.toolbar p {
  margin: 0;
  color: #637489;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #52657a;
  font-weight: 700;
}

select {
  border: 1px solid rgba(23, 32, 51, 0.16);
  border-radius: 8px;
  padding: 9px 12px;
  background: #ffffff;
  color: #172033;
  font: inherit;
}

.state-message {
  margin: 20px 0 0;
  padding: 16px 18px;
  border: 1px solid rgba(15, 106, 197, 0.14);
  border-radius: 8px;
  background: #ffffff;
  color: #52657a;
}

.state-message.is-error {
  border-color: rgba(210, 50, 50, 0.28);
  color: #a22222;
}

.table-wrap {
  overflow-x: auto;
  border: 1px solid rgba(23, 32, 51, 0.1);
  border-radius: 8px;
  background: #ffffff;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 920px;
}

th,
td {
  padding: 14px 16px;
  border-bottom: 1px solid rgba(23, 32, 51, 0.08);
  text-align: left;
  white-space: nowrap;
}

th {
  color: #52657a;
  font-size: 0.86rem;
  font-weight: 800;
  background: #f9fbfd;
}

tbody tr:last-child td {
  border-bottom: 0;
}

.rank-cell,
.score-cell {
  font-weight: 900;
}

.score-cell {
  color: #0f6ac5;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  min-width: 58px;
  justify-content: center;
  border-radius: 999px;
  padding: 5px 9px;
  background: #f0f2f5;
  color: #637489;
  font-size: 0.82rem;
  font-weight: 800;
}

.status-pill.is-complete {
  background: rgba(17, 169, 130, 0.14);
  color: #08765a;
}

@media (max-width: 900px) {
  .leaderboard-topbar,
  .toolbar,
  .download-strip {
    flex-direction: column;
    align-items: stretch;
  }

  .topbar-actions {
    align-items: flex-start;
  }

  .summary-band {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .toolbar-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .download-actions {
    justify-content: flex-start;
  }

  .assignment-header,
  .assignment-steps,
  .rubric-grid {
    grid-template-columns: 1fr;
  }

  .assignment-steps > div {
    min-height: 0;
  }

  .rubric-grid strong {
    min-height: 0;
  }

  label {
    justify-content: space-between;
  }
}
</style>
