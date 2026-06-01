import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'

import { pythonCourse } from '../src/courses/python/course.js'

const chapter10 = pythonCourse.chapters.find((chapter) => chapter.id === '10')

assert.ok(chapter10, 'Python course should register chapter 10')
assert.equal(chapter10.no, '10', 'Chapter 10 should use display number 10')
assert.equal(chapter10.label, '第十章 AI 协作编程')
assert.equal(chapter10.path, '/python/chapter/10')
assert.equal(typeof chapter10.component, 'function', 'Chapter 10 should lazy-load a view component')

const chapter10Content = await import('../src/courses/python/chapter10Content.js')

assert.ok(
  Array.isArray(chapter10Content.chapter10ConceptCards),
  'Chapter 10 concept cards should be exported',
)
assert.ok(
  chapter10Content.chapter10ConceptCards.length >= 4,
  'Chapter 10 needs enough concept cards',
)
assert.ok(
  Array.isArray(chapter10Content.chapter10WorkflowUnits),
  'Chapter 10 workflow units should be exported',
)
assert.ok(
  chapter10Content.chapter10WorkflowUnits.length >= 5,
  'Chapter 10 needs a detailed workflow',
)
assert.ok(
  Array.isArray(chapter10Content.chapter10Pitfalls),
  'Chapter 10 pitfalls should be exported',
)
assert.ok(
  chapter10Content.chapter10Pitfalls.length >= 6,
  'Chapter 10 needs common pitfall coverage',
)
assert.ok(
  Array.isArray(chapter10Content.chapter10PromptExamples),
  'Chapter 10 prompt examples should be exported',
)
assert.ok(chapter10Content.chapter10PromptExamples.length >= 3, 'Chapter 10 needs prompt examples')
assert.ok(
  Array.isArray(chapter10Content.chapter10ToolCards),
  'Chapter 10 tool cards should be exported',
)
assert.ok(chapter10Content.chapter10ToolCards.length >= 5, 'Chapter 10 needs common tool coverage')

const toolNames = chapter10Content.chapter10ToolCards.map((tool) => tool.name)
assert.ok(toolNames.includes('Codex'), 'Chapter 10 should introduce Codex')
assert.ok(toolNames.includes('Claude Code'), 'Chapter 10 should introduce Claude Code')
assert.ok(toolNames.includes('CC Switch'), 'Chapter 10 should introduce CC Switch')

const chapter10View = await readFile(
  new URL('../src/courses/python/views/ChapterTenView.vue', import.meta.url),
  'utf8',
)

assert.match(
  chapter10View,
  /\/courses\/python\/ch10\/chatgpt-please-meme\.jpg/,
  'Chapter 10 cover should include the ChatGPT politeness meme',
)

const promptText = chapter10Content.chapter10PromptExamples
  .map((example) => `${example.title}\n${example.bad}\n${example.good}\n${example.reason}`)
  .join('\n')

assert.match(promptText, /游戏|贪吃蛇|猜数字|pygame|turtle/, 'Prompt examples should be creative')
assert.doesNotMatch(promptText, /食堂|CSV|pandas/i, 'Prompt examples should not reuse earlier experiments')
