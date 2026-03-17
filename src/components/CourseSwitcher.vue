<script setup>
import { computed } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { courses } from "../config/courses";

const route = useRoute();
const activeCourseId = computed(() => String(route.meta.courseId || "python"));
</script>

<template>
  <nav class="course-switcher" aria-label="课程切换">
    <RouterLink
      v-for="course in courses"
      :key="course.id"
      :to="course.home"
      class="course-switcher-link"
      :class="{ 'is-active': course.id === activeCourseId }"
    >
      <span class="course-switcher-text">
        {{ course.shortLabel || course.label }}
      </span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.course-switcher {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 18px;
}

.course-switcher-link {
  min-width: max-content;
  border: 0;
  background: none;
  color: #385a74;
  padding: 4px 0 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-family: var(--font-sans);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: color 0.18s ease, border-color 0.18s ease;
}

.course-switcher-link:hover {
  color: #0f6ac5;
}

.course-switcher-link.is-active {
  color: #0f6ac5;
  border-bottom-color: rgba(13, 123, 232, 0.7);
}

.course-switcher-text {
  font-size: 0.82rem;
  line-height: 1.32;
}

.course-switcher-link:focus-visible {
  outline: 2px solid rgba(13, 123, 232, 0.35);
  outline-offset: 2px;
  border-radius: 4px;
}

@media (max-width: 900px) {
  .course-switcher {
    justify-content: flex-start;
    gap: 10px;
  }
}
</style>
