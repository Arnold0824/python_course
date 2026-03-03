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
</template>
