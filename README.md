# Pokemon AI Agent per Game Boy Color 🎮🤖

## Cos'è questo progetto? 🌟

Immagina di avere un amico robot che può giocare a Pokémon al posto tuo! Questo progetto è proprio questo: un'intelligenza artificiale (IA) che impara a giocare ai giochi Pokémon del Game Boy Color da sola.

È come se avessi un cervello digitale che:
- 👀 Guarda lo schermo del gioco
- 🧠 Pensa a cosa fare
- 🎯 Preme i pulsanti giusti
- 📈 Diventa sempre più bravo giocando

L'obiettivo è vedere come un computer può imparare a catturare Pokémon, vincere battaglie e completare il gioco attraverso tentativi ed errori, proprio come farebbe un bambino che impara a giocare!

---

## Come funziona il nostro Robot Pokémon? 🤖⚡

Il nostro agente AI è composto da 4 "cervelli" diversi che lavorano insieme:

### 1. 🧠 **PokemonMemoryReader** - Il Lettore di Memoria
**Cosa fa:** È come avere degli occhi speciali che possono vedere dentro il gioco!

**Come funziona (spiegato semplice):**
- Immagina che il gioco Pokémon sia come una casa con tante stanze
- Ogni stanza (memoria) contiene informazioni diverse: quanti soldi hai, quali Pokémon hai catturato, quante medaglie hai vinto
- Il nostro robot sa esattamente dove guardare in ogni versione di Pokémon (Rosso, Blu, Giallo, Oro, Argento, Cristallo)
- È come avere una mappa segreta che ti dice dove sono nascosti tutti i tesori!

**Funzioni principali:**
- `_detect_game_type()`: "Che gioco stiamo giocando?" - Riconosce se è Pokémon Rosso, Blu, Giallo, ecc.
- `_get_memory_addresses()`: "Dove sono le informazioni importanti?" - Trova dove il gioco salva i dati
- `read_memory()`: "Leggi questo numero!" - Prende le informazioni dalla memoria del gioco
- `get_current_state()`: "Com'è la situazione ora?" - Raccoglie tutte le informazioni importanti
- `calculate_reward_events()`: "Quanto sono stato bravo?" - Calcola i punti in base a cosa è successo

### 2. 👁️ **PokemonStateDetector** - Il Detective dello Schermo
**Cosa fa:** Guarda lo schermo e capisce cosa sta succedendo nel gioco!

**Come funziona (spiegato semplice):**
- È come avere un detective che guarda lo schermo e dice: "Ah! Ora siamo in battaglia!" oppure "Stiamo parlando con qualcuno!"
- Analizza i colori, le forme e i pattern sullo schermo
- Riconosce situazioni diverse come battaglie, menu, dialoghi

**Funzioni principali:**
- `detect_battle()`: "Siamo in battaglia?" - Cerca le barre della vita dei Pokémon
- `detect_menu()`: "Siamo in un menu?" - Riconosce i menu del gioco
- `detect_dialogue()`: "Qualcuno sta parlando?" - Trova le finestre di dialogo
- `detect_blocked_movement()`: "Siamo bloccati?" - Capisce se non possiamo muoverci

### 3. 🧠💪 **PokemonDQN** - Il Cervello Intelligente
**Cosa fa:** È il vero cervello del robot, una rete neurale che impara a giocare!

**Come funziona (spiegato semplice):**
- Immagina il cervello come una rete di neuroni (come nel cervello umano)
- Ogni neurone è collegato ad altri neuroni
- Quando vede lo schermo del gioco, tutti i neuroni lavorano insieme per decidere cosa fare
- Più gioca, più i collegamenti diventano forti e intelligenti

**Caratteristiche speciali:**
- **Dueling DQN**: Ha due parti del cervello - una che valuta quanto è buona la situazione, e una che valuta quanto è buona ogni azione
- **Convolutional Layers**: Strati speciali che sono bravi a riconoscere immagini (come riconoscere un Pokémon sullo schermo)

### 4. 🎮 **PokemonAI** - Il Giocatore Robot
**Cosa fa:** È il "giocatore" vero e proprio che mette tutto insieme!

**Come funziona (spiegato semplice):**
- Prende le informazioni dal Lettore di Memoria
- Guarda lo schermo con il Detective
- Usa il Cervello Intelligente per decidere
- Preme i pulsanti del Game Boy
- Impara dai suoi errori

**Funzioni principali:**
- `_get_screen_tensor()`: "Trasforma lo schermo in numeri" - Converte l'immagine in dati che il cervello può capire
- `_detect_game_state()`: "Cosa sta succedendo?" - Usa il detective per capire la situazione
- `_calculate_reward()`: "Quanto sono stato bravo?" - Calcola i punti in base alle azioni
- `choose_action()`: "Cosa faccio ora?" - Decide quale pulsante premere
- `remember()`: "Ricorda questa esperienza" - Salva cosa è successo per imparare
- `replay()`: "Studia le esperienze passate" - Impara dalle esperienze salvate
- `play()`: "Gioca!" - Il loop principale dove tutto succede

## Strategie Intelligenti del Robot 🎯

### Sistema di Ricompense (Come diamo i voti al robot)
**Cose buone (+punti):**
- 🏆 Vincere una medaglia: +1000 punti (WOW!)
- 🎯 Catturare un nuovo Pokémon: +500 punti
- 👀 Vedere un nuovo Pokémon: +100 punti
- ⬆️ Pokémon sale di livello: +200 punti
- 💰 Guadagnare soldi: +1 punto per ogni moneta
- 🗺️ Esplorare nuovi posti: +50 punti

**Cose cattive (-punti):**
- 😵 Pokémon va KO: -100 punti
- 💸 Perdere soldi: -2 punti per ogni moneta
- 🔄 Rimanere bloccato: -10 punti

### Strategie Contestuali (Il robot è furbo!)
- **In battaglia:** Preferisce attaccare se ha tanta vita, difendersi se ne ha poca
- **Nei dialoghi:** Sa che deve premere 'A' per continuare a parlare
- **Nell'esplorazione:** Evita di ripetere le stesse mosse per non rimanere bloccato
- **Con poca vita:** Cerca di usare pozioni o andare al Centro Pokémon

## Tecnologie Avanzate Usate 🔬

### Deep Q-Network (DQN)
- **Cosa è:** Un tipo speciale di intelligenza artificiale che impara giocando
- **Come funziona:** Prova tante azioni, vede cosa succede, e ricorda cosa funziona meglio
- **Perché è speciale:** Può imparare strategie complesse che nemmeno noi umani avremmo pensato!

### Prioritized Experience Replay
- **Cosa è:** Il robot ricorda meglio le esperienze più importanti
- **Come funziona:** Come quando studi, ripeti di più le cose difficili
- **Perché è utile:** Impara più velocemente dalle situazioni importanti

### Double DQN
- **Cosa è:** Ha due cervelli che si controllano a vicenda
- **Come funziona:** Un cervello propone, l'altro valuta
- **Perché è meglio:** Evita di essere troppo ottimista sulle sue azioni

## Come far partire il Robot Pokémon? 🚀

### Preparazione (Cosa ti serve)
1. **Python installato** sul tuo computer (è il linguaggio che parla il robot)
2. **Un file ROM di Pokémon** (il gioco vero e proprio, con estensione `.gbc`)
3. **Un po' di pazienza** - il robot deve imparare! 😊

### Installazione Facile 📦

**Passo 1:** Apri il terminale (la "finestra nera" dove scrivi comandi)

**Passo 2:** Il robot installerà da solo tutto quello che gli serve! Ma se vuoi farlo manualmente:
```bash
pip install pyboy numpy Pillow keyboard torch opencv-python
```

**Passo 3:** Per il cervello super-intelligente (raccomandato!):
```bash
pip install torch torchvision
```

### Avvio del Robot 🎮

**Passo 1:** Vai nella cartella del progetto e scrivi:
```bash
python gbc_ai_agent.py
```

**Passo 2:** Il robot ti chiederà dove si trova il gioco Pokémon
- Scrivi il percorso completo del file `.gbc`
- Esempio: `C:\Giochi\Pokemon_Rosso.gbc`

**Passo 3:** Guarda il robot giocare! 🎉

### Controlli Durante il Gioco 🎮
- **ESC**: Ferma il robot ("Basta giocare!")
- **SPAZIO**: Metti in pausa ("Aspetta un momento!")
- **R**: Mostra un report dettagliato ("Come stai andando?")
- **S**: Salva i progressi ("Ricorda tutto!")

## Cosa Succede Quando il Robot Gioca? 🔄

### Il Ciclo di Apprendimento (spiegato semplice)
1. **👀 Osserva**: Il robot guarda lo schermo del gioco
2. **🧠 Pensa**: Usa tutti i suoi "cervelli" per decidere cosa fare
3. **🎯 Agisce**: Preme un pulsante (su, giù, A, B, ecc.)
4. **📊 Valuta**: Controlla se ha fatto bene o male
5. **💾 Ricorda**: Salva l'esperienza per imparare
6. **🔄 Ripete**: Ricomincia dal punto 1

### Cosa Impara il Robot? 📚
- **Esplorare**: Come muoversi nella mappa senza rimanere bloccato
- **Combattere**: Quando attaccare, quando difendersi, quando usare oggetti
- **Catturare**: Come lanciare le Pokéball al momento giusto
- **Strategia**: Quali Pokémon usare in battaglia
- **Gestione**: Come usare soldi e oggetti in modo intelligente

## File Importanti che Crea il Robot 📁

### Cartella `ai_saves_[nome_gioco]/`
Il robot crea una cartella speciale dove salva tutto:
- **`model.pth`**: Il cervello del robot (la rete neurale)
- **`memory.pkl`**: Tutte le esperienze che ha vissuto
- **`stats.json`**: Le statistiche di gioco (medaglie, Pokémon catturati, ecc.)
- **`checkpoints.pkl`**: Punti di salvataggio per non perdere i progressi

### Cosa Significano i Numeri sullo Schermo? 📊
- **Episode**: Quante "partite" ha giocato il robot
- **Frame**: Quanti "fotogrammi" ha visto (come i frame di un film)
- **Reward**: I punti totali guadagnati
- **Epsilon**: Quanto è "curioso" il robot (alto = prova cose nuove, basso = usa quello che sa)
- **Badges**: Quante medaglie ha vinto
- **Pokemon Caught**: Quanti Pokémon ha catturato

## Perché è Così Figo? 🌟

Questo progetto è speciale perché:
- **🎯 È specifico per Pokémon**: Non è un robot generico, sa esattamente come funzionano i giochi Pokémon
- **🧠 Impara davvero**: Non segue regole fisse, ma impara dall'esperienza
- **👁️ Vede tutto**: Può leggere la memoria del gioco E guardare lo schermo
- **🎮 È completo**: Gestisce battaglie, esplorazione, cattura, tutto!
- **📈 Migliora sempre**: Più gioca, più diventa bravo

## Curiosità Tecniche (per i più Curiosi) 🤓

### Architettura del Cervello
- **Input**: Schermo 160x144 pixel + dati dalla memoria
- **Elaborazione**: 3 strati convoluzionali + 2 strati fully connected
- **Output**: 9 azioni possibili (su, giù, sinistra, destra, A, B, Start, Select, niente)

### Algoritmi Usati
- **Double DQN**: Per decisioni più stabili
- **Prioritized Experience Replay**: Per imparare dalle esperienze più importanti
- **Dueling Network**: Per valutare meglio le situazioni
- **Epsilon-Greedy**: Per bilanciare esplorazione e sfruttamento

---

**Divertiti a guardare il tuo robot Pokémon diventare un vero maestro! 🏆🤖**

*Ricorda: l'intelligenza artificiale è come un bambino che impara - ci vuole tempo e pazienza, ma i risultati possono essere sorprendenti!* ✨