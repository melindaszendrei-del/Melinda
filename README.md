# Adaptív Szimbiotikus Akkumulátor Rendszer (ASAS)

**Önszerveződő, játékelméleti és adaptív energiatároló hálózat — kutatási és fejlesztési koncepció.**

Státusz: **CONCEPT / VALIDATION OPEN**  
Dokumentációs felülvizsgálat: 2026. november 26.

## 1. Cél és alapelvek

Az ASAS energiatárolók, energiaforrások, fogyasztók és hálózati kapcsolatok összehangolt működését vizsgálja.

- **Önszerveződés:** decentralizált döntéshozatal és helyi alkalmazkodás, a szükséges hálózati és biztonsági felügyelet megtartásával.
- **Szimbiotikus együttműködés:** energia- és információcsere a résztvevők között, kölcsönös előnyre törekedve.
- **Játékelméleti optimalizálás:** a résztvevők stratégiáinak és ösztönzőinek összehangolása, többek között Nash-egyensúly vizsgálatával. A Nash-egyensúly önmagában nem garantál közös nyereséget vagy globális optimumot.
- **Adaptivitás:** alkalmazkodás a megújuló termelés, a fogyasztás és a környezeti feltételek változásaihoz.

## 2. Energetikai alkalmazások

- Akkumulátoros energiatároló hálózatok; hidrogéntárolás mint külön vizsgálandó alkalmazás.
- Okoshálózatok (Smart Grids).
- Elektromos járművek és V2G (Vehicle-to-Grid).
- Ipari energiamenedzsment, gyárak és adatközpontok.

A cél a tárolási és kisütési döntések jobb összehangolása, a kihasználatlan kapacitás csökkentése, valamint a változó kereslet és termelés kezelése. A hálózati energiaátirányítás csak a tényleges infrastruktúra, kapacitás, engedélyek és szabályozás keretei között lehetséges.

## 3. Tervezett működés

| Funkció | Tervezett szerep |
| --- | --- |
| Szenzorok és IoT | Állapot- és környezeti adatok gyűjtése |
| AI és gépi tanulás | Termelési és fogyasztási előrejelzés, adaptív döntéstámogatás |
| Játékelméleti optimalizálás | Helyi stratégiák és együttműködési ösztönzők vizsgálata |
| Decentralizált kommunikáció | Információcsere és koordináció |
| Edge Computing | Helyi adatfeldolgozás és döntéstámogatás |
| Blokklánc | Opcionálisan vizsgálandó tranzakciós technológia, nem igazolt követelmény |

A központi kérdés, hogy a helyi döntések és a kölcsönös kapcsolatok miként hozhatnak létre rendszerszintű alkalmazkodást. A decentralizáció nem helyettesíti a BMS-t, a védelmi funkciókat vagy a hálózati biztonsági követelményeket.

## 4. Általánosított szimbiotikus keret

A korábbi dokumentáció az ASAS rövidítést Adaptív Szimbiotikus Rendszer, illetve Adaptív Szimbiotikus Alrendszer értelemben is használta. Az energetikai projekt eredeti neve változatlan. Az általánosítás külön koncepcionális alkalmazási irány, nem bizonyított, univerzálisan működő algoritmus.

| Terület | Vizsgálandó alkalmazás |
| --- | --- |
| Energia | Tárolás, megújulók és fogyasztók koordinációja |
| Pénzügy | Résztvevői ösztönzők és adaptív döntési stratégiák |
| Logisztika | Erőforrás-megosztás, üres fuvarok csökkentése |
| Ipar | Gyártási kapacitások adaptív összehangolása |
| Közösségi rendszerek | Erőforrások együttműködésen alapuló elosztása |

Az egyes alkalmazások saját modelljeiket, korlátaikat és külön validációt igényelnek.

## 5. Hatékonyság és validáció

A korai ASAS-leírás 30%-os hatékonysági előnyt említett. **Ez jelenleg nem igazolt teljesítményadat.** A nyilvános kódtár alapágán nincs olyan szimuláció, mérési napló vagy referencia-összehasonlítás, amely ezt alátámasztaná. Az érték történeti kutatási célkitűzésként marad meg; az előny mértéke és a mérőszám definíciója nyitott.

A hagyományos rendszerekhez viszonyított költség-, karbantartási, rugalmassági és hatékonysági előnyök szintén tesztelendő hipotézisek.

### Nyitott műszaki dokumentáció és validáció

- Állapotváltozók, tároló- és hálózati modell, energiaegyensúly.
- Töltési/kisütési korlátok, veszteségek, degradáció és biztonsági feltételek.
- Szereplők, stratégiák, hasznossági függvények és együttműködési feltételek.
- Reprodukálható szimuláció, referenciairányítás, mérőszámok és azonos tesztfeltételek.
- Zavarok, előrejelzési hibák és kommunikációs kiesések vizsgálata.
- Kísérleti vagy pilotadatok; külön fizikai hardvervalidáció.

Ez a lista fejlesztési irány, nem elvégzett tesztek jegyzéke.

## 6. Együttműködés

Kutatási együttműködés, energetikai pilotprojektek, valamint külön ipari, pénzügyi és logisztikai alkalmazási kutatások lehetségesek. Az egyetemekkel és kutatóintézetekkel való együttműködés célkitűzés; a dokumentum nem állít fennálló intézményi partnerséget.

Kapcsolat: melinda.szendrei@gmail.com

## 7. Licenc

A kódtárban található **[MIT License](LICENSE)** feltételei irányadók a licenc hatálya alá tartozó nyilvános anyagokra, beleértve a kereskedelmi felhasználás engedélyét is. A korábbi README-ben szereplő GPL/MIT non-profit korlátozás és 1–5%-os nyereségrészesedés nem az MIT-licenc feltétele. Külön szolgáltatások vagy együttműködések külön megállapodás tárgyai lehetnek, de ez nem korlátozza az MIT által megadott jogokat.

## 8. Eredet és hatókör

Ez a dokumentációs felülvizsgálat a korábbi nyilvános ASAS README tartalmát rendezi, a megalapozatlan teljesítményállításokat pontosítja, és elkülöníti a koncepciót az igazolt eredményektől.

Az [eredeti nyilvános README](https://github.com/melindaszendrei-del/Melinda/blob/dd1283058c0980701e5c1062dac9470253f8e4d9/README.md) változatlanul elérhető a Git-történetben. A LICENSE és a külön kutatási ágak nem módosultak. Ez a felülvizsgálat nem új algoritmus, nem hardvervalidáció és nem teljes kutatási archívum.
