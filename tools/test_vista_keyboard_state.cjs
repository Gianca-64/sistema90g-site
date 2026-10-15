const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { runInNewContext } = require('node:vm');
const source = readFileSync(require('node:path').join(__dirname, '../s90g-home-acquisition-v1.js'), 'utf8');

function fixture(lang = 'it') {
  const document = { documentElement: { lang }, activeElement: null };
  const element = (textContent = '') => ({
    textContent, disabled: true, dataset: {}, attrs: { 'aria-pressed': 'false' }, handlers: {},
    setAttribute(name, value) { this.attrs[name] = value; },
    getAttribute(name) { return this.attrs[name]; },
    addEventListener(name, fn) { this.handlers[name] = fn; },
    focus() { document.activeElement = this; },
    click() { if (!this.disabled) this.handlers.click?.({ preventDefault() {}, stopImmediatePropagation() {} }); },
  });
  const toggle = element();
  const title = element('Initial title');
  const copy = element('Initial explanation');
  const label = element();
  const hotspots = Array.from({ length: 4 }, (_, i) => {
    const item = element();
    item.dataset = { title: `Point ${i}`, copy: `Explanation ${i}`, vistaId: `${i}` };
    return item;
  });
  const stage = { classList: { toggle() {} } };
  const nodes = { '[data-vista-stage]': stage, '[data-vista-toggle]': toggle,
    '[data-vista-toggle-label]': label, '[data-vista-title]': title, '[data-vista-copy]': copy };
  const root = { dataset: {}, querySelector: selector => nodes[selector], querySelectorAll: () => hotspots };
  document.querySelector = () => root;
  document.querySelectorAll = () => [];
  runInNewContext(source, { document, window: { scrollX: 0, scrollY: 0 }, requestAnimationFrame: fn => fn() });
  return { document, toggle, title, copy, hotspots };
}

for (const language of ['it', 'en-GB']) {
  test(`Vista keyboard lifecycle (${language})`, () => {
    const f = fixture(language);
    assert.equal(f.toggle.disabled, false);
    assert.ok(f.hotspots.every(x => x.disabled));
    f.hotspots[0].click();
    assert.equal(f.title.textContent, 'Initial title');
    for (let cycle = 0; cycle < 3; cycle++) {
      f.toggle.click();
      assert.ok(f.hotspots.every(x => !x.disabled));
      f.hotspots[2].focus();
      f.hotspots[2].click();
      assert.equal(f.title.textContent, 'Point 2');
      assert.equal(f.hotspots[2].attrs['aria-pressed'], 'true');
      f.toggle.click();
      assert.ok(f.hotspots.every(x => x.disabled));
      assert.ok(f.hotspots.every(x => x.attrs['aria-pressed'] === 'false'));
      assert.equal(f.document.activeElement, f.toggle);
      assert.equal(f.title.textContent, 'Initial title');
      assert.equal(f.copy.textContent, 'Initial explanation');
    }
  });
}

test('Pages without Vista are unaffected', () => {
  const document = { documentElement: { lang: 'it' }, querySelector: () => null, querySelectorAll: () => [] };
  assert.doesNotThrow(() => runInNewContext(source, { document }));
});
