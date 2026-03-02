#!/usr/bin/env node
/**
 * validate-responsive.js
 * Validación automática de reglas responsive mínimas para componentes HTML de email AMEX.
 *
 * Uso:
 *   node scripts/validate-responsive.js libs/components/hero-banner/hero-banner-overlay-v40.html
 *   node scripts/validate-responsive.js libs/components/  (valida todos)
 */

const fs = require('fs');
const path = require('path');

// ─── Reglas globales (aplican a todos los componentes) ────────────────────────

const GLOBAL_RULES = [
  {
    id: 'meta-viewport',
    desc: 'Meta viewport presente',
    test: (html) => /name=["']viewport["']/.test(html),
    severity: 'CRITICO',
  },
  {
    id: 'container-width-620',
    desc: 'Contenedor raíz con width="620"',
    test: (html) => /width=["']620["']/.test(html),
    severity: 'CRITICO',
  },
  {
    id: 'container-class',
    desc: 'Contenedor raíz con clase .container',
    test: (html) => /class=["'][^"']*container[^"']*["']/.test(html),
    severity: 'CRITICO',
  },
  {
    id: 'media-query-breakpoint',
    desc: '@media only screen and (max-width: 619px) presente',
    test: (html) => /@media\s+only\s+screen\s+and\s+\(max-width\s*:\s*619px\)/.test(html),
    severity: 'CRITICO',
  },
  {
    id: 'container-media-rule',
    desc: 'Clase .container tiene regla en @media',
    test: (html) => /\.container\s*\{[^}]*width.*100%/.test(html),
    severity: 'MEDIO',
  },
  {
    id: 'images-alt',
    desc: 'Todas las imágenes tienen atributo alt',
    test: (html) => {
      const imgs = html.match(/<img[^>]+>/gi) || [];
      return imgs.every(img => /\balt\s*=/.test(img));
    },
    severity: 'MEDIO',
  },
  {
    id: 'images-height-auto',
    desc: 'Imágenes no decorativas tienen height:auto',
    test: (html) => {
      const imgs = html.match(/<img[^>]+>/gi) || [];
      // Solo verifica imágenes con src externo (no íconos fijos de 28px social)
      const contentImgs = imgs.filter(img => {
        const altMatch = img.match(/\balt\s*=\s*["']([^"']*)["']/);
        const alt = altMatch ? altMatch[1] : '';
        return alt.length > 0; // imágenes con alt descriptivo
      });
      return contentImgs.every(img => /height\s*:\s*auto/.test(img));
    },
    severity: 'MEDIO',
  },
];

// ─── Reglas por tipo de componente ────────────────────────────────────────────

const COMPONENT_RULES = {
  'two-column': [
    {
      id: 'full-width-block-class',
      desc: 'Columnas 2-col tienen clase .full-width-block',
      test: (html) => /class=["'][^"']*full-width-block[^"']*["']/.test(html),
      severity: 'CRITICO',
    },
    {
      id: 'full-width-block-media-rule',
      desc: '.full-width-block tiene regla en @media',
      test: (html) => /\.full-width-block\s*\{[^}]*width.*100%/.test(html),
      severity: 'CRITICO',
    },
    {
      id: 'height-auto-class',
      desc: 'Celda con height fijo tiene .height-auto',
      test: (html) => {
        if (!/height=["']\d+["']/.test(html)) return true; // no hay height fijo
        return /class=["'][^"']*height-auto[^"']*["']/.test(html);
      },
      severity: 'MEDIO',
    },
  ],
  'hero-overlay': [
    {
      id: 'vml-background',
      desc: 'Existe bloque VML para background-image (Outlook)',
      test: (html) => /\[if gte mso 9\]/.test(html) && /v:image/.test(html),
      severity: 'CRITICO',
    },
    {
      id: 'mobile-off-spacer',
      desc: 'Columna spacer tiene .mobile-off',
      test: (html) => /class=["'][^"']*mobile-off[^"']*["']/.test(html),
      severity: 'MEDIO',
    },
    {
      id: 'bg-blue-overlay',
      desc: '.BgBlue definida en media query para overlay mobile',
      test: (html) => /\.BgBlue\s*\{/.test(html),
      severity: 'MEDIO',
    },
  ],
  'footer-nav': [
    {
      id: 'fm-nav-link-class',
      desc: 'Links de nav tienen clase .fm-nav-link',
      test: (html) => /class=["'][^"']*fm-nav-link[^"']*["']/.test(html),
      severity: 'MEDIO',
    },
    {
      id: 'fm-border-class',
      desc: 'Links (salvo el primero) tienen clase .fm-border',
      test: (html) => /class=["'][^"']*fm-border[^"']*["']/.test(html),
      severity: 'MEDIO',
    },
  ],
};

// ─── Detección de tipo de componente ─────────────────────────────────────────

function detectComponentType(html, filePath) {
  const name = path.basename(filePath);
  if (/hero-banner.*overlay/.test(name) || (/v:image/.test(html) && /BgBlue|background/.test(html))) {
    return 'hero-overlay';
  }
  if (/footer-nav/.test(name) || /fm-nav-link|fm-border/.test(html)) {
    return 'footer-nav';
  }
  // 2 columnas: tiene <th> con width="50%" o full-width-block
  if (/width=["']50%["']/.test(html) || /horizontal-pair|hotel-card|section-compras|section-gastro|section-hoteles/.test(name)) {
    return 'two-column';
  }
  return 'single-column';
}

// ─── Runner ───────────────────────────────────────────────────────────────────

function validateFile(filePath) {
  const html = fs.readFileSync(filePath, 'utf-8');
  const componentType = detectComponentType(html, filePath);
  const rules = [...GLOBAL_RULES, ...(COMPONENT_RULES[componentType] || [])];

  const results = rules.map(rule => ({
    ...rule,
    pass: rule.test(html),
  }));

  const failures = results.filter(r => !r.pass);
  const criticals = failures.filter(r => r.severity === 'CRITICO');
  const mediums = failures.filter(r => r.severity === 'MEDIO');

  return { filePath, componentType, results, failures, criticals, mediums };
}

function printReport(report) {
  const { filePath, componentType, failures, criticals, mediums } = report;
  const relPath = path.relative(process.cwd(), filePath);
  const status = failures.length === 0 ? 'PASS' : (criticals.length > 0 ? 'FAIL' : 'WARN');
  const statusEmoji = { PASS: '✅', FAIL: '❌', WARN: '⚠️' }[status];

  console.log(`\n${statusEmoji} ${relPath}`);
  console.log(`   Tipo: ${componentType} | Errores: ${criticals.length} críticos, ${mediums.length} medios`);

  if (failures.length > 0) {
    failures.forEach(f => {
      const icon = f.severity === 'CRITICO' ? '❌' : '⚠️';
      console.log(`   ${icon} [${f.severity}] ${f.desc} (${f.id})`);
    });
  }

  return { status, criticals: criticals.length, mediums: mediums.length };
}

// ─── Entry point ──────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Uso: node scripts/validate-responsive.js <archivo.html|directorio>');
  process.exit(1);
}

const target = args[0];
const files = [];

if (fs.statSync(target).isDirectory()) {
  // Recolectar todos los .html en el directorio recursivamente
  function walk(dir) {
    fs.readdirSync(dir).forEach(f => {
      const full = path.join(dir, f);
      if (fs.statSync(full).isDirectory()) walk(full);
      else if (f.endsWith('.html')) files.push(full);
    });
  }
  walk(target);
} else {
  files.push(target);
}

console.log(`\n=== Validación Responsive — ${files.length} archivo(s) ===`);

let totalCriticals = 0;
let totalMediums = 0;
let totalPass = 0;

files.forEach(f => {
  const report = validateFile(f);
  const { status, criticals, mediums } = printReport(report);
  totalCriticals += criticals;
  totalMediums += mediums;
  if (status === 'PASS') totalPass++;
});

console.log(`\n=== Resumen ===`);
console.log(`  Archivos: ${files.length} | Aprobados: ${totalPass} | Con errores: ${files.length - totalPass}`);
console.log(`  Críticos totales: ${totalCriticals} | Medios totales: ${totalMediums}`);

if (totalCriticals > 0) {
  process.exit(1);
}
