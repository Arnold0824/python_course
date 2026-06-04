import assert from 'node:assert/strict'
import { access, constants, readFile } from 'node:fs/promises'

import {
  FINAL_REVIEW_PDF_PATH,
  FINAL_REVIEW_STUDENT_IDS_PATH,
  normalizeStudentId,
  parseAllowedStudentIds,
  validateStudentId,
} from '../src/courses/python/finalReviewAccess.js'

const studentIdFile = new URL(`../public${FINAL_REVIEW_STUDENT_IDS_PATH}`, import.meta.url)
const reviewPdfFile = new URL(`../public${FINAL_REVIEW_PDF_PATH}`, import.meta.url)

await access(studentIdFile, constants.R_OK)
await access(reviewPdfFile, constants.R_OK)

assert.equal(normalizeStudentId(' 231123110162 '), '231123110162')
assert.equal(normalizeStudentId('abc 123'), '123')
assert.equal(normalizeStudentId('abc'), '')

const allowedIds = parseAllowedStudentIds(await readFile(studentIdFile, 'utf8'))

assert.ok(allowedIds.has('231123110162'), 'Known student ID should be present')
assert.ok(validateStudentId(' 231123110162 ', allowedIds).ok, 'Listed ID should pass validation')
assert.equal(validateStudentId('', allowedIds).ok, false, 'Empty ID should not pass validation')
assert.equal(
  validateStudentId('231123110999', allowedIds).ok,
  false,
  'Unlisted ID should not pass validation',
)

const pythonCourseSource = await readFile(
  new URL('../src/courses/python/course.js', import.meta.url),
  'utf8',
)
assert.match(pythonCourseSource, /final-review/, 'Python course should expose final review nav item')

const routerSource = await readFile(new URL('../src/router/index.js', import.meta.url), 'utf8')
assert.match(routerSource, /\/python\/final-review/, 'Router should register final review page')
