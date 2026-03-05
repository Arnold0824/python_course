<script setup>
import { computed } from "vue";
import { RouterView, useRoute } from "vue-router";
import CourseChapterNav from "./components/CourseChapterNav.vue";

const route = useRoute();
const activeChapter = computed(() => String(route.meta.chapterId || "1"));
</script>

<template>
  <CourseChapterNav :active-chapter="activeChapter" />
  <RouterView />
  <footer class="site-beian" role="contentinfo" aria-label="网站备案信息">
    <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">
      蜀ICP备2024111632号
    </a>
  </footer>
</template>
