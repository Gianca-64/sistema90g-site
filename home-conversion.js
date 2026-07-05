(() => {
  const page = location.pathname.split('/').pop() || 'index.html';
  if (page !== 'index.html') return;

  const portal = 'https://sistema90g-console.sistema90g.workers.dev/richiesta';
  document.querySelectorAll('a[href="#contatto"]').forEach(link => {
    link.href = portal;
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = 'Sottoponi il caso';
  });

  if (document.querySelector('#prove-concrete')) return;
  const hero = document.querySelector('main .premium-hero');
  if (!hero) return;

  const section = document.createElement('section');
  section.className = 'premium-section proof-section';
  section.id = 'prove-concrete';
  section.innerHTML = `
    <div class="container">
      <div class="premium-copy wide">
        <p class="eyebrow">Tre problemi reali</p>
        <h2>Prima il problema concreto. Poi il metodo.</h2>
        <p>Questi casi mostrano il tipo di criticità che può restare nascosta finché il progetto non viene messo alla prova nell’uso quotidiano.</p>
      </div>
      <div class="proof-grid">
        <article>
          <span>Cucina</span>
          <h3>La lavastoviglie entra nel passaggio.</h3>
          <p>Finché resta chiusa il corridoio sembra sufficiente. Quando viene aperta, il percorso può bloccarsi.</p>
          <a class="text-link" href="caso-lavastoviglie-passaggio-cucina.html">Leggi il caso</a>
        </article>
        <article>
          <span>Distribuzione</span>
          <h3>La nuova stanza entra, ma comprime la zona giorno.</h3>
          <p>Una funzione aggiunta può sembrare risolta sulla pianta e spostare il problema nell’ambiente più usato.</p>
          <a class="text-link" href="caso-terza-camera-zona-giorno.html">Leggi il caso</a>
        </article>
        <article>
          <span>Preventivo</span>
          <h3>Il totale è chiaro, il valore ottenuto molto meno.</h3>
          <p>Materiali, lavorazioni, accessori ed esclusioni possono rendere poco leggibile ciò che si sta realmente acquistando.</p>
          <a class="text-link" href="caso-preventivo-cucina-sconto-valore.html">Leggi il caso</a>
        </article>
      </div>
      <p class="proof-all"><a class="text-link" href="casi-analizzati.html">Guarda tutti i casi analizzati</a></p>
    </div>`;

  hero.insertAdjacentElement('afterend', section);
})();