import { readdir, readFile, rm, writeFile } from "node:fs/promises"
import { extname, join } from "node:path"
import { fileURLToPath } from "node:url"

const publicDir = fileURLToPath(new URL("../public/", import.meta.url))
const targetExtensions = new Set([".html", ".js", ".css", ".json", ".xml"])
const excluded = [
  ".raw/",
  ".raw",
  ".raw",
  ".obsidian",
  "hot.md",
  "log.md",
  "references/source-ledger.json",
  "references/claim-ledger.md"
]

const replacements = [
  [/[ \t]*\/\/# sourceMappingURL=data:[^<\r\n]*/g, ""],
  [/[ \t]*\/\*# sourceMappingURL=data:[\s\S]*?\*\//g, ""],
  [/\.raw\/\.manifest\.json/g, "the source manifest"],
  [/\.raw\/sources\//g, "the immutable source store"],
  [/\.raw\//g, "the immutable source layer"],
  [/references\/source-ledger\.json/g, "the source ledger"],
  [/references\/claim-ledger\.md/g, "the claim ledger"],
  [/references\/CONFIDENCE_TAGS\.md/g, "the confidence tags reference"],
  [/references\/canon/g, "the canon layer"],
  [/[A-Za-z]:\\[^\s<>"']+/g, "local path removed"],
  [/\/Users\/[^\s<>"']+/g, "local path removed"],
  [/\/home\/[^\s<>"']+/g, "local path removed"],
]

let scanned = 0
let updated = 0
let removed = 0

function shouldExclude(path) {
  const normalized = path.replaceAll("\\", "/")
  return excluded.some((pattern) => {
    const clean = String(pattern).replace(/\/\*\*$/, "").replace(/\/$/, "")
    return clean && (normalized.includes(`/${clean}/`) || normalized.endsWith(`/${clean}`) || normalized.includes(clean))
  })
}

async function walk(dir) {
  const entries = await readdir(dir, { withFileTypes: true })
  for (const entry of entries) {
    const fullPath = join(dir, entry.name)
    if (shouldExclude(fullPath)) {
      await rm(fullPath, { recursive: true, force: true })
      removed += 1
      continue
    }
    if (entry.isDirectory()) {
      await walk(fullPath)
      continue
    }
    if (!entry.isFile() || !targetExtensions.has(extname(entry.name))) {
      continue
    }
    scanned += 1
    const original = await readFile(fullPath, "utf8")
    const sanitized = replacements.reduce((text, [pattern, value]) => text.replace(pattern, value), original)
    if (sanitized !== original) {
      await writeFile(fullPath, sanitized)
      updated += 1
    }
  }
}

await walk(publicDir)
console.log(`Sanitized ${updated} of ${scanned} public files and removed ${removed} excluded paths.`)
