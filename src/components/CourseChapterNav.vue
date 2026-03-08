<script setup>
import { computed } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { courseChapters } from "../config/chapters";

const props = defineProps({
  activeChapter: {
    type: String,
    required: true,
  },
});

const active = computed(() => String(props.activeChapter || "1"));
const route = useRoute();
const isAdminActive = computed(() => route.name === "admin-stats");
</script>

<template>
  <aside class="lesson-chapter-sidebar" aria-label="课程章节导航">
    <section class="chapter-nav">
      <h3>章节导航</h3>
      <ol class="chapter-list">
        <li v-for="chapter in courseChapters" :key="chapter.id">
          <RouterLink
            :to="chapter.path"
            class="chapter-link level-1"
            :class="{ 'is-active': chapter.id === active }"
          >
            <span class="chapter-no">{{ chapter.no }}</span>
            <span class="chapter-text">{{ chapter.label }}</span>
          </RouterLink>
        </li>
      </ol>
      <div class="chapter-admin">
        <RouterLink
          to="/admin/stats"
          class="chapter-link level-1"
          :class="{ 'is-active': isAdminActive }"
        >
          <span class="chapter-no">AD</span>
          <span class="chapter-text">统计后台</span>
        </RouterLink>
      </div>
    </section>
  </aside>
</template>

<style scoped>
.chapter-admin {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px dashed rgba(13, 123, 232, 0.18);
}

@media (max-width: 1280px) {
  .lesson-chapter-sidebar {
    display: block;
    left: 10px;
    right: 10px;
    bottom: calc(var(--beian-bar-height) + 10px + env(safe-area-inset-bottom, 0px));
    top: auto;
    width: auto;
    max-height: none;
    padding: 0;
    border-radius: 12px;
    border: 1px solid rgba(13, 123, 232, 0.18);
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(8px);
  }

  .chapter-nav {
    margin: 0;
    padding: 6px 8px;
    border-bottom: 0;
  }

  .chapter-list {
    display: flex;
    gap: 6px;
    overflow: auto;
  }

  .chapter-link.level-1 {
    min-width: max-content;
    padding-right: 10px;
  }

  .chapter-no {
    min-width: 22px;
  }

  .chapter-nav h3 {
    display: none;
  }
}
</style>
