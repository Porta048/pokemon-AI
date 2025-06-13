# 🤖 Pokemon Ensemble AI - Sistema Multi-Agent

## 📋 Panoramica

Il Pokemon Ensemble AI è un sistema avanzato di training parallelo che utilizza multiple istanze di agenti AI per accelerare l'apprendimento e migliorare le performance nel gioco Pokemon Gold/Silver/Crystal.

### 🎯 Caratteristiche Principali

- **Training Parallelo**: 3-6 agenti che imparano simultaneamente
- **Ensemble Learning**: Combinazione intelligente delle conoscenze
- **Specializzazione**: Ogni agente si focalizza su aspetti diversi del gioco
- **Sincronizzazione**: Condivisione periodica delle conoscenze tra agenti
- **Configurazione Flessibile**: Parametri personalizzabili per ogni agente

## 🚀 Avvio Rapido

### 1. Installazione Dipendenze

```bash
pip install torch pyboy numpy pillow keyboard
```

### 2. Preparazione ROM

Assicurati di avere un file ROM Pokemon (.gbc) nella directory del progetto:
- Pokemon Gold
- Pokemon Silver  
- Pokemon Crystal

### 3. Avvio Ensemble

#### Modalità Interattiva (Raccomandato)
```bash
python launch_ensemble.py
```

#### Modalità Automatica
```bash
python launch_ensemble.py --auto --agents 3 --method soft_merge --episodes 30
```

#### Modalità Avanzata
```bash
python launch_ensemble.py --rom "Pokemon Silver.gbc" --agents 4 --method majority_vote --episodes 50
```

## 🧠 Metodi Ensemble

### 1. Soft Merge (Raccomandato)
- **Descrizione**: Combina gradualmente i Q-values dei diversi agenti
- **Vantaggi**: Apprendimento stabile e continuo
- **Uso**: Ideale per training a lungo termine

### 2. Majority Vote
- **Descrizione**: Sceglie l'azione votata dalla maggioranza degli agenti
- **Vantaggi**: Decisioni robuste e conservative
- **Uso**: Buono per situazioni critiche

## 👥 Configurazione Agenti

### Agente 1: Explorer
- **Focus**: Esplorazione e scoperta
- **Parametri**: Epsilon alto, reward scaling per esplorazione
- **Obiettivo**: Trovare nuove aree e Pokemon Center

### Agente 2: Battler
- **Focus**: Combattimenti e battaglie
- **Parametri**: Gamma alto, memoria estesa
- **Obiettivo**: Ottimizzare strategie di combattimento

### Agente 3: Navigator
- **Focus**: Navigazione e gestione menu
- **Parametri**: Learning rate alto, batch size ottimizzato
- **Obiettivo**: Efficienza nei menu e navigazione

## ⚙️ Configurazione Avanzata

### File ensemble_config.json

```json
{
  "ensemble_settings": {
    "num_agents": 3,
    "ensemble_method": "soft_merge",
    "sync_interval": 1000,
    "max_episodes_per_agent": 50
  },
  "agent_configurations": [
    {
      "agent_id": 0,
      "name": "Explorer",
      "learning_rate": 0.0003,
      "focus": "exploration"
    }
  ]
}
```

### Parametri Personalizzabili

- **learning_rate**: Velocità di apprendimento (0.0001-0.001)
- **epsilon_decay**: Velocità riduzione esplorazione (0.995-0.9999)
- **gamma**: Fattore sconto ricompense future (0.95-0.999)
- **batch_size**: Dimensione batch training (16-128)
- **memory_size**: Dimensione memoria replay (5000-50000)
- **reward_scaling**: Moltiplicatore ricompense (0.5-2.0)

## 📊 Monitoraggio Performance

### Output in Tempo Reale
```
📈 Ensemble Progress (t=120s):
   Agenti attivi: 3/3
   Reward medio: 45.67
   Frame totali: 15,420
🔄 Pesi ensemble aggiornati: ['0.350', '0.425', '0.225']
```

### File di Salvataggio
- `ai_saves_[ROM]_agent_0/`: Dati Agente Explorer
- `ai_saves_[ROM]_agent_1/`: Dati Agente Battler
- `ai_saves_[ROM]_agent_2/`: Dati Agente Navigator
- `ensemble_state.json`: Stato generale ensemble

## 🎮 Utilizzo del Modello Ensemble

### Caricamento Ensemble Trainato

```python
from ensemble_pokemon_ai import EnsemblePokemonAI

# Carica ensemble esistente
ensemble = EnsemblePokemonAI("Pokemon Silver.gbc", num_agents=3)
ensemble.initialize_agents()

# Ottieni azione dall'ensemble
state = get_current_game_state()
action = ensemble.get_ensemble_action(state)
```

### Continuare Training

```python
# Continua training da checkpoint
ensemble.start_parallel_training(max_episodes_per_agent=20)
```

## 🔧 Risoluzione Problemi

### Errore "ROM non trovato"
- Verifica che il file ROM sia nella directory corretta
- Controlla l'estensione (.gbc, .gb)
- Usa il percorso completo se necessario

### Errore "PyTorch non disponibile"
```bash
pip install torch torchvision torchaudio
```

### Performance Basse
- Riduci il numero di agenti (2-3)
- Diminuisci la risoluzione se possibile
- Usa modalità headless per agenti non primari

### Memoria Insufficiente
- Riduci `memory_size` nella configurazione
- Diminuisci `batch_size`
- Usa meno agenti simultanei

## 📈 Ottimizzazione Performance

### Hardware Raccomandato
- **CPU**: 4+ core per 3 agenti
- **RAM**: 8GB+ per ensemble completo
- **GPU**: Opzionale ma accelera il training

### Configurazioni Ottimali

#### Setup Veloce (2 agenti)
```json
{
  "num_agents": 2,
  "sync_interval": 500,
  "max_episodes_per_agent": 20
}
```

#### Setup Bilanciato (3 agenti)
```json
{
  "num_agents": 3,
  "sync_interval": 1000,
  "max_episodes_per_agent": 30
}
```

#### Setup Intensivo (4+ agenti)
```json
{
  "num_agents": 4,
  "sync_interval": 1500,
  "max_episodes_per_agent": 50
}
```

## 🎯 Strategie di Training

### Training Incrementale
1. Inizia con 2 agenti per 20 episodi
2. Aggiungi il terzo agente
3. Aumenta gradualmente gli episodi
4. Ottimizza i parametri basandoti sui risultati

### Training Specializzato
1. Configura agenti con focus diversi
2. Monitora le performance individuali
3. Aggiusta i pesi ensemble dinamicamente
4. Salva configurazioni vincenti

## 📚 Esempi Pratici

### Esempio 1: Training Rapido
```bash
# Training veloce per test
python launch_ensemble.py --auto --agents 2 --episodes 15
```

### Esempio 2: Training Intensivo
```bash
# Training completo overnight
python launch_ensemble.py --agents 4 --method soft_merge --episodes 100
```

### Esempio 3: Training Specializzato
```python
# Configurazione custom per esplorazione
config = {
    'agent_id': 0,
    'focus': 'exploration',
    'reward_scaling': 1.5,
    'epsilon_min': 0.15
}
```

## 🤝 Contributi

Per contribuire al progetto:
1. Fork del repository
2. Crea branch per nuove feature
3. Testa le modifiche con ensemble
4. Invia pull request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi LICENSE per dettagli.

---

**Nota**: Assicurati di possedere legalmente i ROM Pokemon utilizzati. Questo software è solo per scopi educativi e di ricerca.