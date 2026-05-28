<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import CourseSwitcher from '../components/CourseSwitcher.vue'
import { fetchIdeaMessages, submitIdeaMessage } from '../services/ideas'

const route = useRoute()

const messages = ref([])
const content = ref('')
const displayName = ref('')
const isLoading = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

let refreshTimer = 0

const maxLength = 500
const remaining = computed(() => maxLength - content.value.length)
const canSubmit = computed(
  () => content.value.trim().length > 0 && remaining.value >= 0 && !isSubmitting.value,
)

function formatTime(value) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return ''
  }

  return new Intl.DateTimeFormat('zh-CN', {
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    month: '2-digit',
  }).format(date)
}

async function loadMessages({ silent = false } = {}) {
  if (!silent) {
    isLoading.value = true
  }
  errorMessage.value = ''

  try {
    messages.value = await fetchIdeaMessages({ limit: 50 })
  } catch (error) {
    if (!silent) {
      errorMessage.value = error.message || '想法加载失败，请稍后重试。'
    }
  } finally {
    isLoading.value = false
  }
}

async function submitMessage() {
  if (!canSubmit.value) {
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const savedMessage = await submitIdeaMessage({
      chapterId: route.query.chapter ? String(route.query.chapter) : null,
      content: content.value,
      displayName: displayName.value,
      pagePath: route.fullPath,
    })
    messages.value = [savedMessage, ...messages.value].slice(0, 50)
    content.value = ''
    successMessage.value = '已发送。刷新后仍会保留在匿名想法墙里。'
  } catch (error) {
    errorMessage.value = error.message || '发送失败，请稍后重试。'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  void loadMessages()
  refreshTimer = window.setInterval(() => {
    void loadMessages({ silent: true })
  }, 5000)
})

onUnmounted(() => {
  window.clearInterval(refreshTimer)
})
</script>

<template>
  <div class="idea-wall-page">
    <header class="idea-wall-topbar">
      <RouterLink class="idea-wall-brand" to="/python/chapter/10">
        <span>匿名想法墙</span>
        <strong>AI 协作编程课堂</strong>
      </RouterLink>
      <CourseSwitcher />
    </header>

    <main class="idea-wall-main">
      <section class="idea-wall-compose" aria-labelledby="idea-compose-title">
        <div class="idea-wall-compose-copy">
          <p class="idea-wall-kicker">CLASS IDEA WALL</p>
          <h1 id="idea-compose-title">把你的想法匿名发出来</h1>
          <p>
            可以写想做的小游戏、工具、网页、脚本，或者对 AI
            协作编程的疑问。不要填写姓名、学号、手机号、密码或其他个人信息。
          </p>
        </div>

        <form class="idea-wall-form" @submit.prevent="submitMessage">
          <label>
            昵称可留空
            <input
              v-model="displayName"
              maxlength="64"
              placeholder="例如：匿名同学、想做游戏的人"
              type="text"
            />
          </label>

          <label>
            我的想法
            <textarea
              v-model="content"
              :maxlength="maxLength"
              placeholder="例如：我想做一个文字版地牢探险游戏，玩家可以捡装备、遇到随机事件。"
              rows="6"
            ></textarea>
          </label>

          <div class="idea-wall-form-footer">
            <span :class="{ 'is-danger': remaining < 0 }">还可输入 {{ remaining }} 字</span>
            <button :disabled="!canSubmit" type="submit">
              {{ isSubmitting ? '发送中...' : '发送想法' }}
            </button>
          </div>
        </form>
      </section>

      <section class="idea-wall-list-section" aria-labelledby="idea-list-title">
        <div class="idea-wall-list-head">
          <div>
            <p class="idea-wall-kicker">RECENT IDEAS</p>
            <h2 id="idea-list-title">最近想法</h2>
          </div>
          <button :disabled="isLoading" type="button" @click="loadMessages()">
            {{ isLoading ? '刷新中...' : '刷新' }}
          </button>
        </div>

        <p v-if="errorMessage" class="idea-wall-alert is-error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="idea-wall-alert is-success">{{ successMessage }}</p>

        <div v-if="messages.length" class="idea-wall-list">
          <article class="idea-message" v-for="message in messages" :key="message.id">
            <div class="idea-message-meta">
              <strong>{{ message.displayName || '匿名同学' }}</strong>
              <time :datetime="message.createdAt">{{ formatTime(message.createdAt) }}</time>
            </div>
            <p>{{ message.content }}</p>
          </article>
        </div>

        <div v-else class="idea-wall-empty">
          <h3>还没有想法</h3>
          <p>第一个发言可以很简单：写下你想让 AI 帮你一起做什么。</p>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.idea-wall-page {
  min-height: 100vh;
  padding-bottom: calc(var(--beian-bar-height) + 30px);
  color: var(--text-primary);
  background:
    linear-gradient(180deg, rgba(248, 251, 255, 0.94), rgba(239, 247, 255, 0.96)),
    radial-gradient(circle at 18% 12%, rgba(15, 106, 197, 0.14), transparent 34%);
}

.idea-wall-topbar {
  position: sticky;
  top: 0;
  z-index: 80;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 12px clamp(14px, 2vw, 30px);
  border-bottom: 1px solid rgba(13, 123, 232, 0.12);
  background: rgba(247, 251, 255, 0.86);
  backdrop-filter: blur(10px);
}

.idea-wall-brand {
  display: inline-grid;
  gap: 2px;
  color: var(--text-primary);
  text-decoration: none;
}

.idea-wall-brand span {
  width: fit-content;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(13, 123, 232, 0.15);
  color: #0b4c8a;
  font-size: 0.72rem;
  font-weight: 800;
}

.idea-wall-brand strong {
  font-family: var(--font-serif);
  font-size: 1.02rem;
}

.idea-wall-main {
  width: min(1120px, calc(100% - 28px));
  margin: 28px auto 0;
  display: grid;
  gap: 18px;
}

.idea-wall-compose,
.idea-wall-list-section {
  border: 1px solid rgba(13, 123, 232, 0.14);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 42px rgba(13, 62, 108, 0.08);
}

.idea-wall-compose {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(320px, 1.1fr);
  gap: 22px;
  padding: clamp(20px, 3vw, 34px);
}

.idea-wall-compose-copy {
  display: grid;
  align-content: center;
  gap: 12px;
}

.idea-wall-kicker {
  margin: 0;
  color: #0a62be;
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.11em;
}

.idea-wall-compose h1,
.idea-wall-list-head h2 {
  margin: 0;
  color: var(--text-primary);
  font-family: var(--font-serif);
  line-height: 1.28;
}

.idea-wall-compose h1 {
  font-size: clamp(1.8rem, 4vw, 3rem);
}

.idea-wall-compose p {
  margin: 0;
  color: #3d5d79;
  line-height: 1.75;
}

.idea-wall-form {
  display: grid;
  gap: 14px;
}

.idea-wall-form label {
  display: grid;
  gap: 7px;
  color: #173b58;
  font-weight: 900;
}

.idea-wall-form input,
.idea-wall-form textarea {
  width: 100%;
  border: 1px solid rgba(100, 116, 139, 0.26);
  border-radius: 12px;
  background: #ffffff;
  color: #1f3348;
  font: inherit;
  font-weight: 500;
  line-height: 1.55;
  padding: 11px 12px;
  outline: none;
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.idea-wall-form textarea {
  min-height: 148px;
  resize: vertical;
}

.idea-wall-form input:focus,
.idea-wall-form textarea:focus {
  border-color: rgba(13, 123, 232, 0.58);
  box-shadow: 0 0 0 3px rgba(13, 123, 232, 0.13);
}

.idea-wall-form-footer,
.idea-wall-list-head,
.idea-message-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.idea-wall-form-footer span {
  color: #5b7489;
  font-size: 0.9rem;
}

.idea-wall-form-footer span.is-danger {
  color: #d63535;
  font-weight: 900;
}

.idea-wall-form button,
.idea-wall-list-head button {
  border: 0;
  border-radius: 12px;
  background: #0f6ac5;
  color: #ffffff;
  cursor: pointer;
  font: inherit;
  font-weight: 900;
  padding: 10px 16px;
  transition: background 0.18s ease, transform 0.12s ease, opacity 0.18s ease;
}

.idea-wall-form button:hover,
.idea-wall-list-head button:hover {
  background: #0b5aab;
}

.idea-wall-form button:disabled,
.idea-wall-list-head button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.idea-wall-form button:active,
.idea-wall-list-head button:active {
  transform: translateY(1px);
}

.idea-wall-list-section {
  padding: clamp(18px, 2.6vw, 28px);
}

.idea-wall-list-head {
  align-items: flex-end;
}

.idea-wall-list {
  margin-top: 16px;
  display: grid;
  gap: 10px;
}

.idea-message {
  padding: 14px;
  border: 1px solid rgba(13, 123, 232, 0.13);
  border-radius: 14px;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
}

.idea-message-meta strong {
  color: #173b58;
}

.idea-message-meta time {
  color: #6a8193;
  font-size: 0.84rem;
}

.idea-message p {
  margin: 9px 0 0;
  color: #2e4d66;
  line-height: 1.7;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.idea-wall-alert {
  margin: 14px 0 0;
  padding: 10px 12px;
  border-radius: 12px;
  font-weight: 800;
}

.idea-wall-alert.is-error {
  background: rgba(254, 242, 242, 0.86);
  color: #b42318;
}

.idea-wall-alert.is-success {
  background: rgba(236, 253, 245, 0.9);
  color: #0f766e;
}

.idea-wall-empty {
  margin-top: 16px;
  padding: 28px 18px;
  border: 1px dashed rgba(13, 123, 232, 0.3);
  border-radius: 14px;
  background: rgba(239, 246, 255, 0.56);
  text-align: center;
}

.idea-wall-empty h3,
.idea-wall-empty p {
  margin: 0;
}

.idea-wall-empty h3 {
  color: #173b58;
  font-family: var(--font-serif);
  font-size: 1.2rem;
}

.idea-wall-empty p {
  margin-top: 8px;
  color: #516e84;
}

@media (max-width: 820px) {
  .idea-wall-topbar {
    align-items: flex-start;
    flex-direction: column;
  }

  .idea-wall-compose {
    grid-template-columns: 1fr;
  }

  .idea-wall-form-footer,
  .idea-wall-list-head {
    align-items: stretch;
    flex-direction: column;
  }

  .idea-wall-form-footer button,
  .idea-wall-list-head button {
    width: 100%;
  }
}
</style>
