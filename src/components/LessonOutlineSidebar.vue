<script setup>
import { computed } from "vue";

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  activeIndex: {
    type: Number,
    default: 0,
  },
  title: {
    type: String,
    default: "卡片大纲",
  },
});

const emit = defineEmits(["jump"]);

const current = computed(() => props.items[props.activeIndex] || null);
</script>

<template>
  <aside v-if="items.length" class="lesson-outline-sidebar" aria-label="卡片大纲">
    <section class="slide-outline">
      <h3>{{ title }}</h3>
      <div class="outline-current" v-if="current">
        当前：{{ current.number }} {{ current.label }}
      </div>
      <ol class="outline-list">
        <li v-for="item in items" :key="item.index">
          <button
            type="button"
            class="outline-btn"
            :class="[`level-${Math.min(item.level, 3)}`, { 'is-active': item.index === activeIndex }]"
            @click="emit('jump', item.index)"
          >
            <span class="outline-no">{{ item.number }}</span>
            <span class="outline-text">{{ item.label }}</span>
          </button>
        </li>
      </ol>
    </section>
  </aside>
</template>
