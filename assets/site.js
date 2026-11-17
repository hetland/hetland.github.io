const search = document.querySelector('#publication-search');
const year = document.querySelector('#publication-year');
if (search && year) {
  const rows = [...document.querySelectorAll('.publication')];
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#no-results');
  function filter() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let total = 0;
    rows.forEach(row => {
      const show = (!year.value || row.dataset.year === year.value) && terms.every(t => row.textContent.toLocaleLowerCase().includes(t));
      row.hidden = !show;
      total += show ? 1 : 0;
    });
    document.querySelectorAll('.publication-year').forEach(group => { group.hidden = ![...group.querySelectorAll('.publication')].some(row => !row.hidden); });
    count.textContent = `${total} publication${total === 1 ? '' : 's'}`;
    empty.hidden = total > 0;
  }
  search.addEventListener('input', filter);
  year.addEventListener('change', filter);
  document.querySelector('#clear-filters').addEventListener('click', () => { search.value = ''; year.value = ''; filter(); search.focus(); });
}
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(button.dataset.copy); button.textContent = 'Citation copied'; }
  catch { button.textContent = 'Select and copy the citation below'; }
  setTimeout(() => { button.textContent = 'Copy citation'; }, 2500);
}));
