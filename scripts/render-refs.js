const { Cite } = require('@citation-js/core')
require('@citation-js/plugin-csl')
const fs = require('fs')
const path = require('path')

const ROOT = path.join(__dirname, '..')
const allRefs = JSON.parse(fs.readFileSync(path.join(ROOT, 'references.json'), 'utf8'))

function escapeRe (s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') }

// Which references appear in each document
const docRefs = {
  'primaria-secundaria': [
    'cast-2024', 'darling-hammond-2020', 'de-la-cruz-2023', 'diaz-barriga-2006',
    'durlak-2011', 'european-schoolnet-2017', 'flavell-1979', 'fraser-1998',
    'guevara-sf', 'oecd-2017', 'pimienta-2007', 'pimienta-2012',
    'schraw-dennison-1994', 'sep-2022', 'unesco-2015a', 'unesco-2015b',
    'unesco-2018', 'unesco-2020', 'unesco-2021', 'unesco-2023',
    'wiggins-mctighe-2017-facetas', 'wiggins-mctighe-2017-planear'
  ],
  'preparatoria-universidad': [
    'cast-2024', 'darling-hammond-2020', 'deci-ryan-2000', 'diaz-barriga-2006',
    'european-schoolnet-2017', 'fraser-1998', 'guevara-sf', 'helding-fraser-2013',
    'lges-2021', 'oecd-2017', 'oecd-2020', 'pimienta-2007', 'pimienta-2012',
    'unesco-2015a', 'unesco-2015b', 'unesco-2018', 'unesco-2019', 'unesco-2020',
    'unesco-2021', 'unesco-2023', 'wiggins-mctighe-2017-facetas',
    'wiggins-mctighe-2017-planear'
  ],
  'estrategias-comprension': [
    'diaz-barriga-2006', 'guevara-sf', 'pimienta-2007', 'pimienta-2012',
    'wiggins-mctighe-2017-facetas', 'wiggins-mctighe-2017-planear'
  ],
  slides: [
    'cast-2024', 'darling-hammond-2020', 'deci-ryan-2000', 'diaz-barriga-2006',
    'durlak-2011', 'european-schoolnet-2017', 'flavell-1979', 'fraser-1998',
    'guevara-sf', 'helding-fraser-2013', 'lges-2021', 'oecd-2017',
    'pimienta-2007', 'pimienta-2012', 'schraw-dennison-1994', 'sep-2022',
    'unesco-2015a', 'unesco-2015b', 'unesco-2020', 'unesco-2021', 'unesco-2023',
    'wiggins-mctighe-2017-facetas', 'wiggins-mctighe-2017-planear'
  ]
}

// Overrides for entries that citeproc doesn't format well
const manualOverrides = {
  'guevara-sf': {
    html: 'Guevara Salazar, M. S. (s.f.). <i>Estrategia de Enseñanza</i> [Presentación de clase].',
    text: 'Guevara Salazar, M. S. (s.f.). *Estrategia de Enseñanza* [Presentación de clase].'
  },
  'lges-2021': {
    html: 'Ley General de Educación Superior. (2021). <i>Diario Oficial de la Federación</i>, 20 de abril de 2021. <a href="https://www.diputados.gob.mx/LeyesBiblio/pdf/LGES_200421.pdf">https://www.diputados.gob.mx/LeyesBiblio/pdf/LGES_200421.pdf</a>',
    text: 'Ley General de Educación Superior. (2021). *Diario Oficial de la Federación*, 20 de abril de 2021. https://www.diputados.gob.mx/LeyesBiblio/pdf/LGES_200421.pdf'
  }
}

function formatBibliography (refIds, format) {
  const refs = allRefs.filter(r => refIds.includes(r.id))
  const missing = refIds.filter(id => !allRefs.find(r => r.id === id))
  if (missing.length) {
    console.warn(`  Warning: missing reference IDs: ${missing.join(', ')}`)
  }
  const cite = new Cite(refs)
  return cite.format('bibliography', {
    format,
    template: 'apa',
    lang: 'en-US'
  })
}

function extractEntries (html) {
  const entries = []
  const re = /<div[^>]*class="csl-entry"[^>]*data-csl-entry-id="([^"]*)"[^>]*>([\s\S]*?)<\/div>/g
  let m
  while ((m = re.exec(html)) !== null) {
    entries.push({ id: m[1], content: m[2].trim() })
  }
  // Also try the other attribute order
  if (entries.length === 0) {
    const re2 = /<div[^>]*data-csl-entry-id="([^"]*)"[^>]*class="csl-entry"[^>]*>([\s\S]*?)<\/div>/g
    while ((m = re2.exec(html)) !== null) {
      entries.push({ id: m[1], content: m[2].trim() })
    }
  }
  return entries
}

// Spanish APA post-processing
function spanishApa (text) {
  return text
    // & → y (author separator)
    .replace(/&#38; /g, 'y ')
    .replace(/ & /g, ' y ')
    // "In " → "En " (chapter references)
    .replace(/\. In /g, '. En ')
    // English ordinals → Spanish
    .replace(/\((\d+)(?:st|nd|rd|th) ed\.\)/g, '($1.ª ed.)')
    // Restore "y" inside known titles that have "and" in English
    // (no-op for our references since titles are preserved as-is)
}

// Make bare URLs clickable in HTML
function linkifyUrls (html) {
  // Match URLs that aren't already inside href="" or <a> tags
  return html.replace(
    /(?<![">])(https?:\/\/[^\s<]+)/g,
    '<a href="$1">$1</a>'
  )
}

function buildHtmlList (entries) {
  const items = entries.map(e => {
    let content = manualOverrides[e.id]?.html ?? e.content
    content = spanishApa(content)
    content = linkifyUrls(content)
    return `        <li>${content}</li>`
  }).join('\n')
  return `<ul class="referencias">\n${items}\n      </ul>`
}

function replaceInHtml (filePath, entries) {
  let content = fs.readFileSync(filePath, 'utf8')
  const re = /<ul class="referencias">[\s\S]*?<\/ul>/
  if (!re.test(content)) {
    console.error(`  ERROR: could not find <ul class="referencias"> in ${filePath}`)
    process.exit(1)
  }
  content = content.replace(re, buildHtmlList(entries))
  fs.writeFileSync(filePath, content, 'utf8')
}

// Convert HTML entry to Slidev markdown
function htmlToSlidevMarkdown (entry) {
  if (manualOverrides[entry.id]?.text) {
    return manualOverrides[entry.id].text
  }
  let text = entry.content
  text = text
    .replace(/<i>(.*?)<\/i>/g, '*$1*')
    .replace(/<[^>]+>/g, '')
    .replace(/&#38;/g, '&')
    .replace(/&amp;/g, '&')
    .replace(/&#60;/g, '<')
    .replace(/&#62;/g, '>')
  text = spanishApa(text)
  return text
}

function replaceInSlides (filePath, textEntries) {
  let content = fs.readFileSync(filePath, 'utf8')

  // Split references roughly in half for two slides
  const mid = Math.ceil(textEntries.length / 2)
  const slide1Refs = textEntries.slice(0, mid)
  const slide2Refs = textEntries.slice(mid)

  const slide1Body = slide1Refs.join('\n\n')
  const slide2Body = slide2Refs.join('\n\n')

  // Replace between sentinel markers
  const divOpen = '<div class="text-xs space-y-1 mt-2 leading-relaxed">'
  for (const [i, body] of [[1, slide1Body], [2, slide2Body]]) {
    const start = `<!-- REFS:SLIDE${i}:START -->`
    const end = `<!-- REFS:SLIDE${i}:END -->`
    const re = new RegExp(
      escapeRe(start) + '[\\s\\S]*?' + escapeRe(end)
    )
    if (!re.test(content)) {
      console.error(`  ERROR: could not find ${start} / ${end} in slides.md`)
      process.exit(1)
    }
    const replacement = `${start}\n${divOpen}\n\n${body}\n\n</div>\n${end}`
    content = content.replace(re, replacement)
  }

  fs.writeFileSync(filePath, content, 'utf8')
}

// === Main ===
console.log('Rendering references from references.json...\n')

// HTML documents (ul-based references)
for (const doc of ['primaria-secundaria', 'preparatoria-universidad']) {
  console.log(`  ${doc}.html`)
  const html = formatBibliography(docRefs[doc], 'html')
  const entries = extractEntries(html)
  const filePath = path.join(ROOT, 'documento', `${doc}.html`)
  replaceInHtml(filePath, entries)
  console.log(`    → ${entries.length} references written`)
}

// Estrategias-comprension (sentinel marker based)
{
  const doc = 'estrategias-comprension'
  console.log(`  ${doc}.html`)
  const html = formatBibliography(docRefs[doc], 'html')
  const entries = extractEntries(html)
  const filePath = path.join(ROOT, 'documento', `${doc}.html`)
  let content = fs.readFileSync(filePath, 'utf8')
  const start = '<!-- REFS:ESTRATEGIAS:START -->'
  const end = '<!-- REFS:ESTRATEGIAS:END -->'
  const re = new RegExp(escapeRe(start) + '[\\s\\S]*?' + escapeRe(end))
  if (!re.test(content)) {
    console.error(`  ERROR: could not find sentinel markers in ${doc}.html`)
    process.exit(1)
  }
  const items = entries.map(e => {
    let c = manualOverrides[e.id]?.html ?? e.content
    c = spanishApa(c)
    c = linkifyUrls(c)
    return `        <li>${c}</li>`
  }).join('\n')
  const refBlock = `${start}\n      <ul class="referencias">\n${items}\n      </ul>\n      ${end}`
  content = content.replace(re, refBlock)
  fs.writeFileSync(filePath, content, 'utf8')
  console.log(`    → ${entries.length} references written`)
}

// Slides
console.log('  slides.md')
const slidesHtml = formatBibliography(docRefs.slides, 'html')
const slidesEntries = extractEntries(slidesHtml)
const slidesText = slidesEntries.map(e => htmlToSlidevMarkdown(e))
replaceInSlides(path.join(ROOT, 'slides.md'), slidesText)
console.log(`    → ${slidesText.length} references written (split across 2 slides)`)

console.log('\nDone!')
