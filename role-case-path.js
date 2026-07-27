(() => {
const portalConfig=window.S90G_PORTAL_CONFIG||{enabled:false,status:'unconfigured',url:'',message:'Il collegamento alla richiesta non è configurato.'};
const euro=value=>new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(value);
const roleLabels={private:'Privato',retailer:'Rivenditore di cucine',interior:'Interior designer',technician:'Architetto o geometra',company:'Impresa di costruzioni',agency:'Agenzia immobiliare',other:'Altro professionista'};
const privateBase={relationship:'La valutazione riguarda direttamente il richiedente. Il servizio viene confermato dopo il controllo del materiale.'};
const professionalBase={relationship:'Il cliente finale resta associato al soggetto che presenta il caso. Sistema 90G non lo contatta autonomamente e condivide la valutazione soltanto con i destinatari autorizzati.'};
const catalog={
 private:[
  {id:'scelta-finiture-cucina',label:'Devo confrontare due finiture per la cucina',title:'Scelta Finiture cucina',price:47,time:'Entro 1 giorno lavorativo',description:'Confronto tra un massimo di due alternative già selezionate.',includes:['lettura delle due alternative','coerenza con ambiente e luce','manutenzione e risultato percepito'],limits:['massimo due alternative','non comprende sviluppo di nuove combinazioni'],...privateBase},
  {id:'restyling-cucina-esistente',label:'Voglio aggiornare una cucina già installata',title:'Restyling',price:79,time:'Entro 1 giorno lavorativo',description:'Direzione di intervento per una cucina esistente, partendo da vincoli ed elementi da mantenere.',includes:['lettura della cucina attuale','priorità e vincoli','direzione di restyling'],limits:['non è un progetto esecutivo','non comprende preventivi o codici prodotto'],...privateBase},
  {id:'controllo-mirato',label:'Ho un solo dubbio preciso',title:'Controllo mirato',price:127,time:'Entro 2 giorni lavorativi',description:'Verifica concentrata su una domanda principale e circoscritta.',includes:['risposta al dubbio principale','conseguenze osservabili','punti da chiarire'],limits:['un problema principale','non comprende una nuova proposta completa'],...privateBase},
  {id:'analisi-completa',label:'Devo controllare un progetto o preventivo nel suo insieme',title:'Analisi completa',price:253,time:'Entro 2 giorni lavorativi',description:'Lettura di più aspetti collegati di una proposta già esistente.',includes:['mappa delle criticità','conseguenze e priorità','aspetti da verificare'],limits:['richiede una proposta esistente','non comprende una nuova progettazione'],...privateBase},
  {id:'acquisto-assistito-cucina',label:'Devo sviluppare la direzione di una cucina nuova',title:'Acquisto Assistito Cucina 90G',price:290,time:'Entro 3 giorni lavorativi',description:'Proposta preliminare indipendente in due fasi, prima dell’adattamento del rivenditore.',includes:['proposta funzionale preliminare','prime viste tridimensionali','una revisione e fascicolo finale'],limits:['non include codici, ordine o progetto esecutivo','il rivenditore verifica e adatta al marchio'],...privateBase},
  {id:'studio-preliminare-spazi',label:'Devo organizzare gli spazi senza una proposta definita',title:'Studio preliminare degli spazi',price:560,time:'Entro 3 giorni lavorativi',description:'Organizzazione preliminare di funzioni, vincoli e priorità con planimetria descrittiva.',includes:['sintesi delle esigenze','organizzazione delle funzioni','planimetria descrittiva'],limits:['non è un progetto architettonico definitivo','richiede verifiche del professionista incaricato'],...privateBase}
 ],
 retailer:[
  {id:'verifica-progetto-cucina',label:'Ho già sviluppato un progetto cucina da verificare',title:'Analisi progetto cucina',price:150,time:'Consegna standard definita dopo il controllo del materiale',description:'Lettura indipendente di un progetto già sviluppato per individuare criticità visibili, coerenza e dati mancanti.',includes:['passaggi e aperture','uso e piano di lavoro','documento sintetico al rivenditore'],limits:['non comprende nuova composizione o alternative','un progetto, un referente, una consegna'],...professionalBase},
  {id:'manual-review',label:'Il caso non ha ancora un progetto cucina definito',title:'Qualificazione manuale del caso',price:null,time:'Definito dopo la prima valutazione',description:'Il servizio standard del rivenditore richiede un progetto già sviluppato. Il caso verrà qualificato prima di proporre un perimetro.',includes:['verifica dell’idoneità','indicazione del materiale mancante','eventuale servizio alternativo'],limits:['nessun prezzo automatico senza perimetro','nessun contatto al cliente senza autorizzazione'],...professionalBase}
 ],
 professional:[
  {id:'verifica-preliminare-immobile',label:'Devo verificare un singolo immobile',title:'Verifica preliminare immobile',price:149,time:'Consegna standard definita dopo il controllo del materiale',description:'Lettura preliminare di documenti, esigenze, limiti visibili e verifiche necessarie.',includes:['sintesi dell’immobile','informazioni mancanti','punti da affidare ai tecnici competenti'],limits:['non certifica fattibilità o conformità','non sostituisce il professionista incaricato'],...professionalBase},
  {id:'analisi-unita-varianti',label:'Devo analizzare almeno tre unità o varianti collegate',title:'Analisi di più unità o varianti',unitPrice:110,minUnits:3,time:'Consegna definita in base al numero di unità',description:'Analisi uniforme di unità o varianti collegate con un referente e documentazione organizzata.',includes:['scheda per ogni unità','quadro di elementi comuni e differenze','criticità e dati mancanti'],limits:['minimo tre unità o varianti','materiale uniforme e un solo ciclo di integrazioni'],...professionalBase}
 ],
 other:[
  {id:'manual-review',label:'Desidero descrivere il mio ruolo e il caso',title:'Valutazione professionale personalizzata',price:null,time:'Definito dopo la prima valutazione',description:'Il ruolo o il perimetro non rientrano nei percorsi standard e devono essere verificati prima di indicare condizioni e prezzo.',includes:['qualificazione del ruolo','verifica del rapporto con il cliente','proposta del perimetro corretto'],limits:['nessun prezzo automatico senza perimetro','nessun contatto al cliente senza autorizzazione'],...professionalBase}
 ]
};
const calculatePrice=(selection,units=0)=>{if(selection.unitPrice){const unitCount=Math.max(selection.minUnits,Number(units)||selection.minUnits);return {unitCount,price:selection.unitPrice*unitCount,priceText:euro(selection.unitPrice*unitCount),priceNote:`${euro(selection.unitPrice)} × ${unitCount} unità o varianti`};}if(selection.price!==null)return {unitCount:null,price:selection.price,priceText:euro(selection.price),priceNote:'Il prezzo viene confermato dopo il controllo del materiale.'};return {unitCount:null,price:null,priceText:'Da definire dopo la qualificazione',priceNote:'Nessun costo viene applicato senza una proposta preventiva.'};};
if(typeof window!=='undefined')window.S90G_PATH={catalog,calculatePrice};
function group(role){return role==='private'?'private':role==='retailer'?'retailer':role==='other'?'other':'professional'}
function init(){
 const form=document.getElementById('s90g-role-path'); if(!form)return;
 const steps=[...form.querySelectorAll('[data-step]')], progress=[...document.querySelectorAll('[data-progress]')];
 const roleOptions=document.getElementById('s90g-role-options'), situationOptions=document.getElementById('s90g-situation-options');
 const roleValue=document.getElementById('s90g-role-value'), unitControl=document.getElementById('s90g-unit-control'), units=document.getElementById('s90g-units');
 let role='',selection=null;
 const show=n=>{steps.forEach(x=>x.hidden=Number(x.dataset.step)!==n);progress.forEach(x=>x.classList.toggle('is-active',Number(x.dataset.progress)<=n)); if(n===3)document.querySelector('[data-step="3"]').focus?.(); document.getElementById('percorso').scrollIntoView({behavior:'smooth',block:'start'});};
 const selectedInput=name=>form.querySelector(`input[name="${name}"]:checked`);
 roleOptions.addEventListener('change',()=>{role=selectedInput('role')?.value||''; form.querySelector('[data-next="2"]').disabled=!role;});
 form.querySelector('[data-next="2"]').addEventListener('click',()=>{
  role=selectedInput('role')?.value||''; if(!role)return;
  roleValue.textContent=`Percorso per: ${roleLabels[role]}. Seleziona la situazione più vicina al caso reale.`;
  situationOptions.innerHTML='';
  catalog[group(role)].forEach(item=>{const label=document.createElement('label');label.className='s90g-choice';label.innerHTML=`<input type="radio" name="situation" value="${item.id}"><span><strong>${item.label}</strong><small>${item.description}</small></span>`;situationOptions.appendChild(label)});
  unitControl.hidden=true; form.querySelector('[data-next="3"]').disabled=true; show(2);
 });
 situationOptions.addEventListener('change',()=>{
  const id=selectedInput('situation')?.value; selection=catalog[group(role)].find(x=>x.id===id)||null;
  unitControl.hidden=!(selection&&selection.unitPrice); form.querySelector('[data-next="3"]').disabled=!selection;
 });
 units.addEventListener('input',()=>{if(Number(units.value)<3)units.setCustomValidity('Il minimo è 3 unità o varianti.');else units.setCustomValidity('');});
 form.querySelector('[data-next="3"]').addEventListener('click',()=>{
  if(!selection)return; const calculated=calculatePrice(selection,units.value);let {unitCount,priceText,priceNote}=calculated;if(unitCount)units.value=unitCount;
  document.getElementById('s90g-result-title').textContent=selection.title;
  document.getElementById('s90g-result-description').textContent=selection.description;
  document.getElementById('s90g-result-price').textContent=priceText;
  document.getElementById('s90g-result-price-note').textContent=priceNote;
  document.getElementById('s90g-result-time').textContent=selection.time;
  document.getElementById('s90g-result-includes').innerHTML=selection.includes.map(x=>`<li>${x}</li>`).join('');
  document.getElementById('s90g-result-limits').innerHTML=selection.limits.map(x=>`<li>${x}</li>`).join('');
  document.getElementById('s90g-result-relationship').textContent=selection.relationship;
  const source=new URL(location.href), cta=document.getElementById('s90g-result-cta');
  cta.dataset.service=selection.id;
  if(portalConfig.enabled&&portalConfig.url){
   const target=new URL(portalConfig.url);
   target.searchParams.set('requester_role',role);target.searchParams.set('case_context',selection.id);target.searchParams.set('service',selection.id);
   target.searchParams.set('service_title',selection.title);target.searchParams.set('service_time',selection.time);
   if(calculated.price!==null){target.searchParams.set('service_price',String(calculated.price));target.searchParams.set('service_currency','EUR');}
   if(selection.unitPrice)target.searchParams.set('unit_price',String(selection.unitPrice));
   target.searchParams.set('source_page',source.searchParams.get('source_page')||'analisi-preventiva');
   target.searchParams.set('content_type',source.searchParams.get('content_type')||'guided-path');target.searchParams.set('cta_position','step-3-result');
   ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','case_id'].forEach(k=>{if(source.searchParams.get(k))target.searchParams.set(k,source.searchParams.get(k))});
   if(unitCount)target.searchParams.set('units',String(unitCount));
   cta.href=target.toString();cta.dataset.portalEnabled='true';cta.removeAttribute('aria-disabled');cta.removeAttribute('role');
   cta.querySelector('span').textContent='Inizia la richiesta';
   document.getElementById('s90g-result-disclaimer').textContent='Il servizio viene confermato dopo il controllo del materiale. Nel modulo successivo inserirai i dati iniziali; allegati, pagamento e consegna non sono ancora gestiti nel portale.';
  }else{
   cta.href='/contatti.html';cta.dataset.portalEnabled='false';cta.removeAttribute('aria-disabled');cta.removeAttribute('role');
   cta.querySelector('span').textContent='Contatta Sistema 90G';
   document.getElementById('s90g-result-disclaimer').textContent='Servizio, prezzo e condizioni restano visibili. Il collegamento alla richiesta non è al momento configurato.';
  }
  document.dispatchEvent(new CustomEvent('s90g:path-result',{detail:{role,service:selection.id,units:unitCount||''}}));show(3);
 });
 const portalBanner=document.getElementById('s90g-portal-banner');
 if(portalBanner&&portalConfig.message){const message=portalBanner.querySelector('p');if(message)message.textContent=portalConfig.message;}
 form.querySelectorAll('[data-back]').forEach(btn=>btn.addEventListener('click',()=>show(Number(btn.dataset.back))));
 const params=new URL(location.href).searchParams, hinted=params.get('service_hint');
 if(hinted){const matchingRole=Object.keys(catalog).find(k=>catalog[k].some(x=>x.id===hinted));const hintedRole=matchingRole==='private'?'private':matchingRole==='retailer'?'retailer':'';if(hintedRole){const input=form.querySelector(`input[name="role"][value="${hintedRole}"]`);if(input){input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));}}}else{const source=params.get('source_page');const sourceRole=source==='rivenditori-cucine'?'retailer':source==='agenzie-immobiliari'?'agency':'';if(sourceRole){const input=form.querySelector(`input[name="role"][value="${sourceRole}"]`);if(input){input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));}}}
}
document.addEventListener('DOMContentLoaded',init);
})();
