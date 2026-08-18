from pathlib import Path

PAGE = Path('lavastoviglie-cucina-aperture-passaggi.html')
s = PAGE.read_text()

marker = '<h2>Quando la posizione è critica</h2><p>Le situazioni più delicate sono vicino agli angoli, di fronte a un\'isola, accanto a cassettoni molto larghi o quando il passaggio serve anche per raggiungere altre zone della cucina.</p>'

block = '''<h2>Dove mettere la lavastoviglie rispetto al lavello?</h2><p>La vicinanza al lavello è utile perché concentra la zona lavaggio e semplifica i movimenti tra risciacquo, carico e scarico. La posizione va però verificata insieme ad aperture, angoli, passaggi e attacchi: essere “vicino al lavello” non basta se lo sportello aperto crea un conflitto.</p><h2>Meglio a destra o a sinistra del lavello?</h2><p>Non esiste un lato corretto in assoluto. Conta come viene usata la cucina, dove resta lo spazio operativo, quale mano viene usata più spesso e soprattutto cosa succede quando lavello, lavastoviglie, cassetti e passaggi sono utilizzati contemporaneamente.</p><h2>Lavastoviglie vicino a un angolo: cosa verificare?</h2><p>Vicino a un angolo bisogna controllare che anta, maniglia, zoccolo, cestelli estratti e moduli adiacenti possano funzionare senza urti o sovrapposizioni. Anche pochi centimetri possono cambiare molto l'uso reale.</p><h2>Se lo sportello aperto blocca il passaggio</h2><p>Il problema non è soltanto poter aprire la lavastoviglie, ma poterla caricare e scaricare senza impedire il passaggio necessario alle altre funzioni della cucina. La verifica va fatta con persona presente e cestelli estratti.</p><h2>Lavastoviglie vicino al forno o sotto il piano cottura</h2><p>La compatibilità non va data per scontata. Ingombri, ventilazione, isolamento, collegamenti e istruzioni dei modelli scelti devono essere verificati sul progetto reale e sulle schede tecniche del produttore.</p><h2>Quanto può essere distante da acqua e scarico?</h2><p>La distanza utile dipende dal percorso reale di carico e scarico, dalle indicazioni del produttore e dalla configurazione dell'impianto. Non va fissata solo in base a una misura generica: tubazioni, pendenze, accessibilità e manutenzione devono essere valutate con chi realizza l'impianto.</p><h2>Progettare bene la zona lavaggio</h2><p>Lavello, lavastoviglie, contenitori per rifiuti e spazio di appoggio dovrebbero funzionare come una sequenza coerente. La posizione migliore è quella che riduce movimenti inutili senza creare nuove interferenze con passaggi, cassetti, forno o piano cottura.</p>'''

if block in s:
    print('SKIP lavastoviglie-cucina-aperture-passaggi.html: già ampliata')
elif marker in s:
    s = s.replace(marker, marker + block, 1)
    PAGE.write_text(s)
    print('OK lavastoviglie-cucina-aperture-passaggi.html')
else:
    raise SystemExit('Marker non trovato in lavastoviglie-cucina-aperture-passaggi.html')

print('Search Everywhere: posizione lavastoviglie ampliata nella guida esistente.')
