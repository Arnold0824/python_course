import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'

const routerSource = await readFile('src/router/index.js', 'utf8')
const chapterTenSource = await readFile('src/courses/python/views/ChapterTenView.vue', 'utf8')
const ideaWallSource = await readFile('src/views/IdeaWallView.vue', 'utf8')
const ideaServiceSource = await readFile('src/services/ideas.js', 'utf8')

assert.match(routerSource, /\/python\/ideas/, 'Router should expose a standalone idea wall page')
assert.match(chapterTenSource, /\/python\/ideas/, 'Chapter 10 should link to the idea wall')
assert.match(ideaWallSource, /匿名想法墙/, 'Idea wall page should be student-facing')
assert.match(ideaWallSource, /最近想法/, 'Idea wall page should show recent messages')
assert.match(ideaWallSource, /textarea/, 'Idea wall page should include a message input')
assert.match(ideaWallSource, /fetchIdeaMessages/, 'Idea wall page should fetch existing messages')
assert.match(ideaWallSource, /submitIdeaMessage/, 'Idea wall page should submit new messages')
assert.match(ideaServiceSource, /\/api\/ideas\/messages/, 'Frontend idea service should use API route')
