(() => {
  'use strict';
  const CAMPAIGN_KEYS=['utm_source','utm_medium','utm_campaign','utm_content','utm_term'];
  const CONSENT_KEY='s90g_cookie_consent';
  const PRIVATE_SERVICES=new Set(['scelta-finiture-cucina','restyling-cucina-esistente','controllo-mirato','analisi-completa','acquisto-assistito-cucina']);
  const NAV_LINKS=[
    ['home','Home','/'],
    ['services','Servizi','/servizi.html'],
    ['process','Come funziona','/analisi-preventiva.html'],
    ['cases','Casi reali','/casi-analizzati.html'],
    ['professionals','Professionisti','/professionisti.html'],
    ['retailers','Rivenditori','/rivenditori-cucine.html'],
    ['method','Metodo 90G','/metodo-sistema90g.html'],
    ['innovation','Innovazioni','/innovazioni.html'],
    ['about','Chi sono','/chi-e-sistema90g.html'],
    ['contacts','Contatti','/contatti.html']
  ];
  const pageSlug=()=>{
    const name=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,'');
    return name==='index'?'home':name;
  };
  function syncConsentCookie(){
    const consent=window.localStorage.getItem(CONSENT_KEY);
    if(consent!=='accepted'&&consent!=='rejected')return;
    const secure=location.protocol==='https:'?'; Secure':'';
    document.cookie=`${CONSENT_KEY}=${encodeURIComponent(consent)}; Path=/; Domain=.sistema90g.it; Max-Age=31536000; SameSite=Lax${secure}`;
  }
  const activeKey=slug=>{
    if(slug==='home')return 'home';
    if(slug==='analisi-preventiva')return 'process';
    if(slug==='casi-analizzati'||slug.startsWith('casi-')||slug.startsWith('caso-'))return 'cases';
    if(slug==='rivenditori-cucine'||slug==='controllo-progetto-cucina')return 'retailers';
    if(slug==='professionisti')return 'professionals';
    if(slug==='metodo-sistema90g')return 'method';
    if(slug==='innovazioni'||location.pathname.includes('/approfondimenti/'))return 'innovation';
    if(slug==='chi-e-sistema90g')return 'about';
    if(slug==='contatti')return 'contacts';
    if(slug==='servizi'||PRIVATE_SERVICES.has(slug)||slug==='analisi-preventivo-cucina')return 'services';
    return '';
  };
  const inferRoleHint=slug=>{
    if(PRIVATE_SERVICES.has(slug))return 'private';
    if(slug==='rivenditori-cucine'||slug==='controllo-progetto-cucina')return 'retailer';
    return '';
  };
  const inferContentType=slug=>{
    if(slug.startsWith('caso-'))return 'case';
    if(slug.startsWith('casi-'))return 'case-category';
    if(slug==='innovazioni'||location.pathname.includes('/approfondimenti/'))return 'article';
    if(['professionisti','rivenditori-cucine'].includes(slug))return 'professional';
    if(slug==='servizi'||PRIVATE_SERVICES.has(slug)||slug==='controllo-progetto-cucina')return 'service';
    return 'page';
  };
  function campaignParams(){
    const current=new URL(location.href), out={};
    CAMPAIGN_KEYS.forEach(k=>{const v=current.searchParams.get(k);if(v)out[k]=v});
    return out;
  }
  function preserveCampaignParams(scope=document){
    const params=campaignParams();
    if(!Object.keys(params).length)return;
    scope.querySelectorAll('a[href]').forEach(link=>{
      const raw=link.getAttribute('href')||'';
      if(!raw||raw.startsWith('#')||raw.startsWith('mailto:')||raw.startsWith('tel:')||link.hasAttribute('data-no-campaign'))return;
      let target;try{target=new URL(raw,location.href)}catch{return}
      if(target.origin!==location.origin)return;
      Object.entries(params).forEach(([k,v])=>target.searchParams.set(k,v));
      link.href=target.toString();
    });
  }
  function preparePathLinks(scope=document){
    const current=new URL(location.href), slug=pageSlug(), defaultRole=inferRoleHint(slug);
    scope.querySelectorAll('a[data-start-path]').forEach((link,index)=>{
      const target=new URL(link.getAttribute('href')||'/analisi-preventiva.html#percorso',location.href);
      target.searchParams.set('source_page',link.dataset.sourcePage||slug);
      target.searchParams.set('content_type',link.dataset.contentType||inferContentType(slug));
      target.searchParams.set('cta_position',link.dataset.ctaPosition||((link.closest('header'))?'header':(link.closest('footer')?'footer':`inline-${index+1}`)));
      if(link.dataset.service)target.searchParams.set('service_hint',link.dataset.service);
      const role=link.dataset.roleHint||defaultRole;if(role)target.searchParams.set('role_hint',role);
      if(link.dataset.caseId)target.searchParams.set('case_id',link.dataset.caseId);
      CAMPAIGN_KEYS.forEach(k=>{const v=current.searchParams.get(k);if(v)target.searchParams.set(k,v)});
      link.href=target.toString();
    });
  }
  function normalizeActionLabels(scope=document){
    scope.querySelectorAll('a[data-start-path]').forEach(link=>{
      const text=(link.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
      if(text.includes('invia il tuo caso')||text.includes('sottoponi il caso')||text==='valuta il caso'||text.startsWith('parliamo del caso')){
        const arrow=link.querySelector('[aria-hidden="true"]');
        if(arrow){const first=link.querySelector('span:not([aria-hidden])')||link.querySelector('span');if(first)first.textContent='Valuta il tuo caso';}
        else link.textContent='Valuta il tuo caso →';
      }
    });
    scope.querySelectorAll('a.s90g-link').forEach(link=>{
      const text=(link.textContent||'').replace(/\s+/g,' ').trim();
      if(!/^(Scopri|Approfondisci)\s*→?$/i.test(text))return;
      const card=link.closest('article,.s90g-service-card,.s90g-prof-card');
      const title=card?.querySelector('h2,h3')?.textContent?.trim();
      link.textContent=title?`Vedi ${title} →`:'Vedi il servizio →';
    });
  }
  function buildNavigation(){
    const header=document.querySelector('.s90g-header');
    const nav=header?.querySelector('.s90g-nav');
    if(!header||!nav)return;
    const key=activeKey(pageSlug());
    nav.id='s90g-main-navigation';
    nav.innerHTML=NAV_LINKS.map(([id,label,href])=>`<a data-nav-key="${id}" href="${href}"${id===key?' aria-current="page"':''}>${label}</a>`).join('');
    let toggle=header.querySelector('.s90g-menu-toggle');
    if(!toggle){
      toggle=document.createElement('button');
      toggle.type='button';toggle.className='s90g-menu-toggle';toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-controls',nav.id);
      toggle.innerHTML='<span>Menu</span><span aria-hidden="true">☰</span>';
      nav.before(toggle);
    }
    const setOpen=open=>{header.classList.toggle('is-nav-open',open);toggle.setAttribute('aria-expanded',String(open));toggle.querySelector('[aria-hidden="true"]').textContent=open?'×':'☰'};
    toggle.addEventListener('click',()=>setOpen(toggle.getAttribute('aria-expanded')!=='true'));
    nav.addEventListener('click',event=>{if(event.target.closest('a'))setOpen(false)});
    document.addEventListener('keydown',event=>{if(event.key==='Escape'&&header.classList.contains('is-nav-open')){setOpen(false);toggle.focus()}});
    document.addEventListener('click',event=>{if(header.classList.contains('is-nav-open')&&!header.contains(event.target))setOpen(false)});
    const mq=matchMedia('(min-width: 1181px)');const reset=()=>{if(mq.matches)setOpen(false)};mq.addEventListener?.('change',reset);
    header.classList.add('s90g-nav-ready');
  }
  function addSkipLink(){
    if(document.querySelector('.s90g-skip-link'))return;
    const main=document.querySelector('main');if(!main)return;if(!main.id)main.id='contenuto-principale';
    const link=document.createElement('a');link.className='s90g-skip-link';link.href=`#${main.id}`;link.textContent='Vai al contenuto principale';document.body.prepend(link);
  }
  function enhancePathLinks(){
    const slug=pageSlug(), role=inferRoleHint(slug);
    if(role)document.querySelectorAll('a[data-start-path]').forEach(link=>{if(!link.dataset.roleHint)link.dataset.roleHint=role});
  }
  function init(){
    syncConsentCookie();
    document.addEventListener('click',event=>{
      if(event.target.closest('[data-cookie-choice],a[data-start-path],a[data-final-portal]'))queueMicrotask(syncConsentCookie);
    },true);
    addSkipLink();buildNavigation();enhancePathLinks();normalizeActionLabels();preparePathLinks();preserveCampaignParams();
    document.dispatchEvent(new CustomEvent('s90g:navigation-ready'));
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
