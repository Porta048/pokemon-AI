# Game Boy Color AI Agent

## In Breve

Questo progetto è un'intelligenza artificiale (IA) che impara a giocare ai giochi del Game Boy Color da sola! In pratica, è un "cervello" digitale che guarda lo schermo del gioco, decide quale mossa fare (come premere un pulsante o muovere il personaggio) e cerca di migliorare giocando tante volte.

L'obiettivo è vedere come un computer può imparare a giocare a Pokémon (o altri giochi GBC) attraverso tentativi ed errori, diventando sempre più bravo.

---

## Spiegazione Dettagliata del Codice

Questo documento descrive il funzionamento tecnico dello script Python `gbc_ai_agent.py`, l'agente AI progettato per giocare automaticamente a giochi per Game Boy Color utilizzando la libreria PyBoy.

## Funzionalità Principali

L'agente AI è in grado di:

- Caricare una ROM di un gioco per Game Boy Color.
- Interagire con l'emulatore PyBoy inviando input (pressione di tasti).
- Osservare lo stato del gioco catturando screenshot.
- Implementare una strategia di gioco basata su reinforcement learning (se TensorFlow è disponibile) o una strategia più semplice basata su regole e casualità.
- Apprendere e migliorare le proprie decisioni nel tempo (modalità Deep Learning).
- Gestire lo stato di pausa e interruzione del gioco.

## Struttura del Codice

Il codice è organizzato principalmente attorno alla classe `GameBoyAI` e ad alcune funzioni di supporto.

### Funzioni di Supporto

- **`check_and_install_dependencies()`**: Questa funzione verifica la presenza delle librerie Python necessarie (`pyboy`, `numpy`, `Pillow`, `keyboard`) e le installa automaticamente se mancanti. Controlla anche la disponibilità di `tensorflow` per abilitare la modalità di apprendimento profondo.

### Classe `GameBoyAI`

Questa è la classe principale che incapsula tutta la logica dell'agente AI.

- **`__init__(self, rom_path, headless=False)`**: Il costruttore inizializza l'emulatore PyBoy con la ROM specificata. Definisce le azioni possibili che l'agente può compiere (movimenti, pressione dei tasti A, B, Start, Select) e inizializza i parametri per l'algoritmo di reinforcement learning (epsilon per la strategia epsilon-greedy, memoria per le esperienze, batch size per il training). Inizializza anche lo stato del gioco (conteggio frame, reward totale, ecc.) e, se TensorFlow è disponibile, costruisce il modello di rete neurale.

- **`_build_model(self)`**: (Utilizzata solo se TensorFlow è disponibile) Costruisce un modello di rete neurale convoluzionale (CNN) utilizzando Keras. Questo modello prende come input l'immagine dello schermo del gioco e restituisce i Q-values per ogni azione possibile. Viene creato anche un `target_model` per stabilizzare l'apprendimento (tecnica comune nel Deep Q-Learning).

- **`_get_screen_state(self)`**: Cattura lo schermo corrente del gioco dall'emulatore, lo converte in scala di grigi e lo normalizza. Questo array NumPy rappresenta lo stato attuale del gioco che viene fornito in input al modello AI.

- **`_calculate_reward(self, current_screen)`**: Calcola un punteggio (reward) basato sui cambiamenti osservati nello schermo. L'idea è di premiare l'agente quando l'immagine cambia (indicando progresso o interazione) e penalizzarlo se lo schermo rimane statico per troppo tempo (indicando che l'agente potrebbe essere bloccato).

- **`choose_action(self, state)`**: Decide quale azione compiere. Se TensorFlow è disponibile e il modello è stato addestrato, utilizza una strategia epsilon-greedy: con probabilità epsilon sceglie un'azione casuale (esplorazione), altrimenti sceglie l'azione con il Q-value più alto predetto dal modello (sfruttamento). Se TensorFlow non è disponibile o il modello non è pronto, utilizza una strategia più semplice basata su movimenti casuali, cercando di evitare di rimanere bloccato e di ripetere la stessa azione troppe volte.

- **`remember(self, state, action, reward, next_state, done)`**: Salva l'esperienza corrente (stato, azione, reward, stato successivo, fine episodio) in una memoria a capacità limitata (deque). Queste esperienze verranno usate per addestrare il modello.

- **`replay(self)`**: (Utilizzata solo se TensorFlow è disponibile) Addestra il modello di rete neurale campionando un batch di esperienze dalla memoria. Per ogni esperienza, calcola i Q-values target usando l'equazione di Bellman e aggiorna i pesi del modello tramite backpropagation.

- **`update_target_model(self)`**: (Utilizzata solo se TensorFlow è disponibile) Copia periodicamente i pesi dal modello principale al `target_model`. Questo aiuta a stabilizzare il processo di apprendimento.

- **`play(self)`**: È il loop principale del gioco. In ogni iterazione:
    1. Gestisce gli input da tastiera (ESC per uscire, SPAZIO per mettere in pausa).
    2. Ottiene lo stato corrente dello schermo.
    3. Sceglie un'azione.
    4. Esegue l'azione inviando i comandi all'emulatore.
    5. Fa avanzare l'emulatore di alcuni frame.
    6. Rilascia i pulsanti premuti.
    7. Calcola il reward.
    8. Salva l'esperienza nella memoria.
    9. Periodicamente, addestra il modello (`replay()`) e aggiorna il `target_model()`.
    10. Stampa statistiche sul progresso.
    11. Aggiorna lo stato precedente dello schermo e il conteggio dei frame.

### Funzione `main()`

- È la funzione principale che avvia l'applicazione.
- Stampa un messaggio di benvenuto.
- Chiede all'utente di fornire il percorso del file ROM del gioco (`.gbc`).
- Verifica che il file esista e sia valido.
- Crea un'istanza della classe `GameBoyAI`.
- Chiama il metodo `play()` per avviare il gioco e l'agente AI.
- Gestisce eventuali eccezioni che potrebbero verificarsi durante l'esecuzione.

## Come Eseguire lo Script

1.  **Assicurarsi di avere Python installato.**
2.  **Salvare il codice** come `gbc_ai_agent.py` in una cartella.
3.  **Installare le dipendenze:**
    Lo script tenterà di installare automaticamente le dipendenze mancanti. Tuttavia, è possibile installarle manualmente eseguendo:
    ```bash
    pip install pyboy numpy Pillow keyboard
    ```
    Per la modalità di apprendimento profondo (opzionale ma consigliata per prestazioni migliori), installare TensorFlow:
    ```bash
    pip install tensorflow
    ```
4.  **Procurarsi un file ROM** di un gioco per Game Boy Color (con estensione `.gbc`).
5.  **Eseguire lo script** da un terminale o prompt dei comandi:
    ```bash
    python gbc_ai_agent.py
    ```
6.  Quando richiesto, **inserire il percorso completo** del file ROM.
7.  Il gioco si avvierà e l'AI inizierà a giocare.
    -   Premere `ESC` per terminare l'esecuzione.
    -   Premere `SPAZIO` per mettere in pausa/riprendere il gioco.

## Flusso di Esecuzione

1.  Lo script inizia con la funzione `main()`.
2.  Vengono controllate e installate le dipendenze.
3.  L'utente fornisce il percorso della ROM.
4.  Viene creata un'istanza di `GameBoyAI`.
    -   L'emulatore PyBoy viene inizializzato.
    -   Se TensorFlow è disponibile, il modello CNN viene costruito.
5.  Il metodo `play()` viene chiamato, avviando il loop di gioco.
    -   L'AI osserva lo schermo, sceglie un'azione, la esegue e riceve un reward.
    -   Le esperienze vengono memorizzate e usate per addestrare il modello (se applicabile).
6.  Il gioco continua finché l'utente non preme `ESC`.
7.  Al termine, vengono stampate le statistiche della sessione.

Questo agente AI rappresenta un esempio di come le tecniche di intelligenza artificiale, in particolare il reinforcement learning, possono essere applicate per insegnare a un programma a giocare a videogiochi complessi.