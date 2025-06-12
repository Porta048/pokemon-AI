"""
Game Boy Color AI Agent - Deep Learning con PyTorch
Compatibile con Python 3.13+ e testato per funzionare correttamente
"""

import os
import sys
import time
import random
import numpy as np
import json
import pickle
from collections import deque
from datetime import datetime

# Funzione per installare dipendenze
def check_and_install_dependencies():
    """Verifica e installa le dipendenze necessarie"""
    required = {
        'pyboy': 'pyboy',
        'numpy': 'numpy',
        'PIL': 'Pillow',
        'keyboard': 'keyboard',
        'torch': 'torch torchvision --index-url https://download.pytorch.org/whl/cpu'
    }
    
    print("🔍 Controllo dipendenze...")
    missing = []
    
    # Controlla tutte tranne torch
    for module, package in required.items():
        if module != 'torch':
            try:
                __import__(module)
                print(f"✅ {module} già installato")
            except ImportError:
                missing.append(package)
    
    # Controlla PyTorch separatamente
    try:
        import torch
        print(f"✅ PyTorch già installato - versione {torch.__version__}")
        torch_available = True
    except ImportError:
        print("📦 PyTorch non trovato - installazione in corso...")
        print("⏳ Questo potrebbe richiedere qualche minuto...")
        result = os.system(f"{sys.executable} -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
        if result == 0:
            print("✅ PyTorch installato con successo!")
            torch_available = True
        else:
            print("❌ Errore installazione PyTorch - continuo senza deep learning")
            torch_available = False
    
    # Installa altre dipendenze mancanti
    if missing:
        print(f"📦 Installazione altre dipendenze: {', '.join(missing)}")
        for package in missing:
            os.system(f"{sys.executable} -m pip install {package}")
    
    return torch_available

# Installa dipendenze
torch_available = check_and_install_dependencies()

# Import dopo installazione
import pyboy
from pyboy.utils import WindowEvent
from PIL import Image
import keyboard

# Import PyTorch se disponibile
if torch_available:
    try:
        import torch
        import torch.nn as nn
        import torch.optim as optim
        import torch.nn.functional as F
        print(f"🔥 PyTorch {torch.__version__} caricato con successo!")
        # Test rapido
        test_tensor = torch.rand(1, 1, 144, 160)
        print("✅ PyTorch funziona correttamente!")
    except Exception as e:
        print(f"❌ Errore caricamento PyTorch: {e}")
        torch_available = False


# Rete neurale DQN in PyTorch
if torch_available:
    class DQN(nn.Module):
        """Deep Q-Network per Game Boy"""
        def __init__(self, n_actions):
            super(DQN, self).__init__()
            
            # Convolutional layers
            self.conv1 = nn.Conv2d(1, 32, kernel_size=8, stride=4)
            self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
            self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
            
            # Calcola dimensione dopo convoluzioni
            def conv2d_size_out(size, kernel_size, stride):
                return (size - kernel_size) // stride + 1
            
            convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(144, 8, 4), 4, 2), 3, 1)
            convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(160, 8, 4), 4, 2), 3, 1)
            linear_input_size = convh * convw * 64
            
            # Fully connected layers
            self.fc1 = nn.Linear(linear_input_size, 512)
            self.fc2 = nn.Linear(512, 256)
            self.fc3 = nn.Linear(256, n_actions)
            
            # Dropout per regolarizzazione
            self.dropout = nn.Dropout(0.2)
        
        def forward(self, x):
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            x = F.relu(self.conv3(x))
            x = x.view(x.size(0), -1)  # Flatten
            x = F.relu(self.fc1(x))
            x = self.dropout(x)
            x = F.relu(self.fc2(x))
            x = self.dropout(x)
            x = self.fc3(x)
            return x


class PyTorchGameBoyAI:
    """AI per Game Boy con PyTorch Deep Learning"""
    
    def __init__(self, rom_path, headless=False):
        print(f"\n🎮 Inizializzazione PyTorch AI per: {os.path.basename(rom_path)}")
        
        # Percorsi salvataggio
        self.rom_name = os.path.splitext(os.path.basename(rom_path))[0]
        self.save_dir = f"ai_saves_{self.rom_name}"
        os.makedirs(self.save_dir, exist_ok=True)
        
        self.model_path = os.path.join(self.save_dir, "model.pth")
        self.memory_path = os.path.join(self.save_dir, "memory.pkl")
        self.stats_path = os.path.join(self.save_dir, "stats.json")
        
        # Inizializza emulatore
        self.pyboy = pyboy.PyBoy(
            rom_path,
            window="headless" if headless else "SDL2",
            debug=False
        )
        print("✅ Emulatore PyBoy avviato!")
        
        # Definizione azioni
        self.actions = [
            [],  # 0: Nessuna azione
            [WindowEvent.PRESS_ARROW_UP],      # 1: Su
            [WindowEvent.PRESS_ARROW_DOWN],    # 2: Giù
            [WindowEvent.PRESS_ARROW_LEFT],    # 3: Sinistra
            [WindowEvent.PRESS_ARROW_RIGHT],   # 4: Destra
            [WindowEvent.PRESS_BUTTON_A],      # 5: A
            [WindowEvent.PRESS_BUTTON_B],      # 6: B
            [WindowEvent.PRESS_BUTTON_START],  # 7: Start
            [WindowEvent.PRESS_BUTTON_SELECT], # 8: Select
            # Combo utili
            [WindowEvent.PRESS_BUTTON_A, WindowEvent.PRESS_BUTTON_A],  # 9: Doppio A
            [WindowEvent.PRESS_BUTTON_B, WindowEvent.PRESS_BUTTON_B],  # 10: Doppio B
            # Combo direzionali
            [WindowEvent.PRESS_ARROW_UP, WindowEvent.PRESS_BUTTON_A],    # 11: Su + A
            [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.PRESS_BUTTON_A],  # 12: Giù + A
            [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.PRESS_BUTTON_A],  # 13: Sinistra + A
            [WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.PRESS_BUTTON_A], # 14: Destra + A
            [WindowEvent.PRESS_ARROW_UP, WindowEvent.PRESS_BUTTON_B],    # 15: Su + B
            [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.PRESS_BUTTON_B],  # 16: Giù + B
        ]
        
        self.action_names = ['Niente', 'Su', 'Giù', 'Sinistra', 'Destra', 
                            'A', 'B', 'Start', 'Select', '2xA', '2xB',
                            'Su+A', 'Giù+A', 'Sinistra+A', 'Destra+A', 'Su+B', 'Giù+B']
        
        # Release map
        self.release_map = {
            WindowEvent.PRESS_ARROW_UP: WindowEvent.RELEASE_ARROW_UP,
            WindowEvent.PRESS_ARROW_DOWN: WindowEvent.RELEASE_ARROW_DOWN,
            WindowEvent.PRESS_ARROW_LEFT: WindowEvent.RELEASE_ARROW_LEFT,
            WindowEvent.PRESS_ARROW_RIGHT: WindowEvent.RELEASE_ARROW_RIGHT,
            WindowEvent.PRESS_BUTTON_A: WindowEvent.RELEASE_BUTTON_A,
            WindowEvent.PRESS_BUTTON_B: WindowEvent.RELEASE_BUTTON_B,
            WindowEvent.PRESS_BUTTON_START: WindowEvent.RELEASE_BUTTON_START,
            WindowEvent.PRESS_BUTTON_SELECT: WindowEvent.RELEASE_BUTTON_SELECT,
        }
        
        # Carica statistiche
        self.stats = self._load_stats()
        
        # Parametri DQN
        self.batch_size = 32
        self.gamma = 0.95
        self.epsilon = max(0.1, 0.5 * (0.995 ** (self.stats.get('total_frames', 0) / 10000)))
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.998
        self.learning_rate = 0.0001
        self.memory = deque(maxlen=10000)
        self.priority_memory = deque(maxlen=2000)
        
        # Device (CPU per compatibilità)
        self.device = torch.device("cpu")
        print(f"🖥️ Usando device: {self.device}")
        
        # Inizializza modelli
        self.model = None
        self.target_model = None
        self.optimizer = None
        
        if torch_available:
            self._init_or_load_model()
        else:
            print("⚠️ PyTorch non disponibile - modalità senza deep learning")
        
        # Stato del gioco
        self.frame_count = 0
        self.episode_count = self.stats.get('episodes', 0)
        self.total_reward = 0
        self.best_reward = self.stats.get('best_reward', float('-inf'))
        
        # History
        self.action_history = deque(maxlen=30)
        self.reward_history = deque(maxlen=1000)
        self.loss_history = deque(maxlen=100)
        
        # Anti-loop
        self.stuck_counter = 0
        self.loop_detector = {}
        self.visited_states = set()
        
        # Carica memoria se esiste
        self._load_memory()
        
        # Pulisci memoria all'avvio
        self._clean_memory()
        
        print(f"✅ PyTorch AI pronta! Sessione #{self.episode_count + 1}")
        print(f"📊 Frame totali: {self.stats.get('total_frames', 0):,}")
        print(f"🏆 Miglior punteggio: {self.best_reward:.2f}")
    
    def _init_or_load_model(self):
        """Inizializza o carica il modello PyTorch"""
        try:
            self.model = DQN(len(self.actions)).to(self.device)
            self.target_model = DQN(len(self.actions)).to(self.device)
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
            
            if os.path.exists(self.model_path):
                print(f"📂 Caricamento modello esistente...")
                checkpoint = torch.load(self.model_path, map_location=self.device)
                self.model.load_state_dict(checkpoint['model_state'])
                self.target_model.load_state_dict(checkpoint['model_state'])
                self.optimizer.load_state_dict(checkpoint['optimizer_state'])
                self.epsilon = checkpoint.get('epsilon', self.epsilon)
                print("✅ Modello caricato con successo!")
            else:
                print("🔨 Creazione nuovo modello...")
                self.target_model.load_state_dict(self.model.state_dict())
                self._save_model()
                print("✅ Nuovo modello creato!")
            
            # Test del modello
            test_input = torch.rand(1, 1, 144, 160).to(self.device)  # [batch, channels, height, width]
            with torch.no_grad():
                output = self.model(test_input)
            print(f"✅ Test modello OK - output shape: {output.shape}")
            
        except Exception as e:
            print(f"❌ Errore inizializzazione modello: {e}")
            self.model = None
            self.target_model = None
            self.optimizer = None
    
    def _save_model(self):
        """Salva il modello PyTorch"""
        if self.model is not None:
            try:
                checkpoint = {
                    'model_state': self.model.state_dict(),
                    'optimizer_state': self.optimizer.state_dict(),
                    'epsilon': self.epsilon,
                    'episode': self.episode_count,
                    'frame': self.frame_count
                }
                torch.save(checkpoint, self.model_path)
                print(f"💾 Modello salvato: {self.model_path}")
                
                # Backup periodico
                if self.frame_count % 50000 == 0 and self.frame_count > 0:
                    backup_path = os.path.join(self.save_dir, f"model_backup_{self.frame_count}.pth")
                    torch.save(checkpoint, backup_path)
                    print(f"💾 Backup creato: {backup_path}")
                    
            except Exception as e:
                print(f"❌ Errore salvataggio modello: {e}")
    
    def _load_stats(self):
        """Carica statistiche"""
        if os.path.exists(self.stats_path):
            with open(self.stats_path, 'r') as f:
                return json.load(f)
        return {
            'episodes': 0,
            'total_frames': 0,
            'best_reward': float('-inf'),
            'average_rewards': [],
            'loss_history': []
        }
    
    def _save_stats(self):
        """Salva statistiche"""
        self.stats['episodes'] = self.episode_count
        self.stats['total_frames'] += self.frame_count
        self.stats['best_reward'] = max(self.best_reward, self.total_reward)
        
        if len(self.reward_history) > 0:
            self.stats['average_rewards'].append(float(np.mean(list(self.reward_history))))
        if len(self.loss_history) > 0:
            self.stats['loss_history'].append(float(np.mean(list(self.loss_history))))
        
        with open(self.stats_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def _save_memory(self):
        """Salva replay memory"""
        try:
            memory_data = {
                'memory': list(self.memory)[-5000:],
                'priority': list(self.priority_memory)
            }
            with open(self.memory_path, 'wb') as f:
                pickle.dump(memory_data, f)
            print(f"💾 Memoria salvata: {len(memory_data['memory']) + len(memory_data['priority'])} esperienze")
        except Exception as e:
            print(f"❌ Errore salvataggio memoria: {e}")
    
    def _load_memory(self):
        """Carica replay memory"""
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, 'rb') as f:
                    memory_data = pickle.load(f)
                
                # Filtra solo esperienze con shape corretta
                for exp in memory_data.get('memory', []):
                    if len(exp) == 5 and isinstance(exp[0], np.ndarray) and exp[0].shape == (144, 160):
                        self.memory.append(exp)
                
                for exp in memory_data.get('priority', []):
                    if len(exp) == 5 and isinstance(exp[0], np.ndarray) and exp[0].shape == (144, 160):
                        self.priority_memory.append(exp)
                
                print(f"📂 Memoria caricata: {len(self.memory)} esperienze valide")
            except Exception as e:
                print(f"⚠️ Errore caricamento memoria: {e}")
                # Pulisci memoria se corrotta
                self.memory.clear()
                self.priority_memory.clear()
    
    def _get_screen_tensor(self):
        """Ottiene lo schermo come tensore PyTorch"""
        screen = self.pyboy.screen.image
        gray = np.array(screen.convert('L'))
        normalized = gray.astype(np.float32) / 255.0
        
        # Converti in tensore PyTorch
        if torch_available:
            # Solo una unsqueeze per il canale, non per il batch
            tensor = torch.from_numpy(normalized.copy()).unsqueeze(0)  # Shape: [1, 144, 160]
            return tensor.to(self.device)
        else:
            return normalized
    
    def _calculate_reward(self, screen_tensor, previous_screen):
        """Calcola reward basato sui cambiamenti"""
        reward = 0
        
        if previous_screen is not None:
            if torch_available and isinstance(screen_tensor, torch.Tensor):
                # Calcola differenza in PyTorch
                diff = torch.abs(screen_tensor - previous_screen).mean().item()
            else:
                # Numpy fallback
                diff = np.mean(np.abs(screen_tensor - previous_screen))
            
            # Reward basato sul movimento
            if diff < 0.01:
                self.stuck_counter += 1
                reward -= min(2.0, self.stuck_counter * 0.05)
            else:
                if self.stuck_counter > 10:
                    reward += min(5.0, self.stuck_counter * 0.2)
                self.stuck_counter = 0
                reward += diff * 10
            
            # Penalità per azioni ripetitive
            if len(self.action_history) >= 10:
                recent = list(self.action_history)[-10:]
                unique = len(set(recent))
                if unique <= 2:
                    reward -= 3.0
                elif unique <= 3:
                    reward -= 1.0
        
        # Bonus sopravvivenza
        reward += 0.1
        
        # Bonus esplorazione
        if torch_available and isinstance(screen_tensor, torch.Tensor):
            # Usa solo i valori del tensore per l'hash, non l'intero oggetto
            state_bytes = screen_tensor.cpu().numpy().tobytes()
        else:
            state_bytes = screen_tensor.tobytes() if hasattr(screen_tensor, 'tobytes') else str(screen_tensor)
        
        state_hash = hash(state_bytes)
        if state_hash not in self.visited_states:
            self.visited_states.add(state_hash)
            reward += 2.0
        
        self.reward_history.append(reward)
        return reward
    
    def choose_action(self, state):
        """Sceglie azione con epsilon-greedy e anti-loop"""
        # Anti-loop check
        same_action_count = 0
        if len(self.action_history) > 0:
            last_action = self.action_history[-1]
            for a in reversed(self.action_history):
                if a == last_action:
                    same_action_count += 1
                else:
                    break
        
        force_different = same_action_count > 5
        
        # Debug se loop rilevato
        if same_action_count > 10:
            print(f"⚠️ LOOP: Azione {self.action_names[last_action]} ripetuta {same_action_count} volte!")
            self.epsilon = min(0.9, self.epsilon + 0.2)
        
        # Primi frame
        if self.frame_count < 200:
            if self.frame_count % 30 == 0:
                return 7  # START
            elif self.frame_count % 30 == 15:
                return 5  # A
        
        # Epsilon-greedy
        if random.random() < self.epsilon or force_different or self.model is None:
            # Esplorazione
            if force_different and len(self.action_history) > 0:
                available = [i for i in range(len(self.actions)) if i != self.action_history[-1]]
                action = random.choice(available)
            else:
                # Esplorazione bilanciata
                weights = [0.05, 0.15, 0.15, 0.15, 0.15, 0.15, 0.1, 0.05, 0.05, 0.0, 0.0, 0.05, 0.05, 0.05, 0.05, 0.03, 0.03]
                action = random.choices(range(len(self.actions)), weights=weights[:len(self.actions)])[0]
        else:
            # Sfruttamento con rete neurale
            with torch.no_grad():
                # Aggiungi dimensione batch
                state_batch = state.unsqueeze(0)  # Da [1, 144, 160] a [1, 1, 144, 160]
                q_values = self.model(state_batch)
                
                # Anti-loop nella rete
                if force_different and len(self.action_history) > 0:
                    q_values[0][self.action_history[-1]] = -1000
                
                # Aggiungi rumore per varietà
                if self.stuck_counter > 5:
                    noise = torch.randn_like(q_values) * 0.1
                    q_values += noise
                
                action = q_values.argmax().item()
        
        self.action_history.append(action)
        return action
    
    def remember(self, state, action, reward, next_state, done):
        """Salva esperienza nella memoria"""
        # Converti tensori in numpy per storage - rimuovi dimensione canale
        if torch_available and isinstance(state, torch.Tensor):
            state_np = state.squeeze(0).cpu().numpy()  # Da [1, 144, 160] a [144, 160]
            next_state_np = next_state.squeeze(0).cpu().numpy()
        else:
            state_np = state
            next_state_np = next_state
        
        experience = (state_np, action, reward, next_state_np, done)
        self.memory.append(experience)
        
        # Aggiungi a memoria prioritaria se importante
        if abs(reward) > 2.0 or done:
            self.priority_memory.append(experience)
    
    def replay(self):
        """Training con experience replay"""
        if self.model is None or len(self.memory) < self.batch_size:
            return
        
        try:
            # Mix memoria normale e prioritaria
            priority_size = min(self.batch_size // 3, len(self.priority_memory))
            normal_size = self.batch_size - priority_size
            
            batch = []
            if priority_size > 0:
                batch.extend(random.sample(self.priority_memory, priority_size))
            if normal_size > 0 and len(self.memory) >= normal_size:
                batch.extend(random.sample(self.memory, normal_size))
            
            # Prepara batch con shape consistenti
            states_list = []
            next_states_list = []
            actions_list = []
            rewards_list = []
            dones_list = []
            
            for e in batch:
                # e[0] e e[3] sono array numpy salvati
                state = e[0]
                next_state = e[3]
                
                # Assicurati che abbiano la forma corretta [144, 160]
                if isinstance(state, np.ndarray):
                    if state.shape == (144, 160):
                        states_list.append(state)
                        next_states_list.append(next_state)
                        actions_list.append(e[1])
                        rewards_list.append(e[2])
                        dones_list.append(e[4])
                    else:
                        # Skip se la forma non è corretta
                        continue
            
            # Se non abbiamo abbastanza esperienze valide, esci
            if len(states_list) < 4:
                return
            
            # Converti in array numpy e poi in tensori
            # Aggiungi dimensione canale [batch, 144, 160] -> [batch, 1, 144, 160]
            states_np = np.array(states_list)
            states_np = np.expand_dims(states_np, axis=1)  # Aggiungi dimensione canale
            next_states_np = np.array(next_states_list)
            next_states_np = np.expand_dims(next_states_np, axis=1)
            
            # Converti in tensori PyTorch
            states = torch.FloatTensor(states_np).to(self.device)
            actions = torch.LongTensor(actions_list).to(self.device)
            rewards = torch.FloatTensor(rewards_list).to(self.device)
            next_states = torch.FloatTensor(next_states_np).to(self.device)
            dones = torch.FloatTensor(dones_list).to(self.device)
            
            # Calcola Q-values correnti
            current_q_values = self.model(states).gather(1, actions.unsqueeze(1))
            
            # Calcola target Q-values con Double DQN
            with torch.no_grad():
                next_actions = self.model(next_states).argmax(1).unsqueeze(1)
                next_q_values = self.target_model(next_states).gather(1, next_actions).squeeze(1)
                target_q_values = rewards + (1 - dones) * self.gamma * next_q_values
            
            # Loss e backpropagation
            loss = F.smooth_l1_loss(current_q_values.squeeze(), target_q_values)
            
            self.optimizer.zero_grad()
            loss.backward()
            
            # Gradient clipping per stabilità
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            
            self.optimizer.step()
            
            # Salva loss per statistiche
            self.loss_history.append(loss.item())
            
            # Decay epsilon
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
            
        except Exception as e:
            print(f"⚠️ Errore durante training: {e}")
            import traceback
            traceback.print_exc()
    
    def update_target_model(self):
        """Soft update del target model"""
        if self.model is not None and self.target_model is not None:
            tau = 0.001
            for target_param, param in zip(self.target_model.parameters(), self.model.parameters()):
                target_param.data.copy_(tau * param.data + (1.0 - tau) * target_param.data)
    
    def _clean_memory(self):
        """Pulisce la memoria da esperienze corrotte o con shape sbagliata"""
        # Pulisci memoria normale
        cleaned_memory = deque(maxlen=10000)
        for exp in self.memory:
            if (len(exp) == 5 and 
                isinstance(exp[0], np.ndarray) and 
                isinstance(exp[3], np.ndarray) and
                exp[0].shape == (144, 160) and 
                exp[3].shape == (144, 160)):
                cleaned_memory.append(exp)
        
        # Pulisci memoria prioritaria
        cleaned_priority = deque(maxlen=2000)
        for exp in self.priority_memory:
            if (len(exp) == 5 and 
                isinstance(exp[0], np.ndarray) and 
                isinstance(exp[3], np.ndarray) and
                exp[0].shape == (144, 160) and 
                exp[3].shape == (144, 160)):
                cleaned_priority.append(exp)
        
        removed = (len(self.memory) - len(cleaned_memory)) + (len(self.priority_memory) - len(cleaned_priority))
        if removed > 0:
            print(f"🧹 Rimosse {removed} esperienze corrotte dalla memoria")
        
        self.memory = cleaned_memory
        self.priority_memory = cleaned_priority
    
    def play(self):
        """Loop principale del gioco"""
        print("\n🎮 GIOCO AVVIATO - PyTorch Deep Learning AI!")
        print("Comandi: ESC=Esci, SPACE=Pausa, S=Salva\n")
        
        paused = False
        previous_screen = None
        last_save_frame = 0
        
        try:
            while True:
                # Controlli tastiera
                if keyboard.is_pressed('escape'):
                    print("\n🛑 Salvataggio e uscita...")
                    break
                
                if keyboard.is_pressed('space'):
                    paused = not paused
                    print("⏸️ PAUSA" if paused else "▶️ RIPRENDI")
                    time.sleep(0.3)
                
                if keyboard.is_pressed('s'):
                    self._save_model()
                    self._save_memory()
                    self._save_stats()
                    print("💾 Salvataggio manuale completato!")
                    time.sleep(0.3)
                
                if paused:
                    self.pyboy.tick()
                    continue
                
                # Game step
                state = self._get_screen_tensor()
                action = self.choose_action(state)
                
                # Esegui azione
                for button in self.actions[action]:
                    self.pyboy.send_input(button)
                
                for _ in range(4):
                    self.pyboy.tick()
                
                for button in self.actions[action]:
                    if button in self.release_map:
                        self.pyboy.send_input(self.release_map[button])
                
                # Reward e prossimo stato
                next_state = self._get_screen_tensor()
                reward = self._calculate_reward(next_state, previous_screen)
                self.total_reward += reward
                
                # Salva esperienza
                if previous_screen is not None:
                    self.remember(state, action, reward, next_state, False)
                
                # Training
                if self.frame_count % 10 == 0 and len(self.memory) >= self.batch_size:
                    self.replay()
                
                # Update target
                if self.frame_count % 100 == 0:
                    self.update_target_model()
                
                # Salvataggio automatico
                if self.frame_count - last_save_frame >= 5000:
                    self._save_model()
                    self._save_memory()
                    self._save_stats()
                    last_save_frame = self.frame_count
                
                # Statistiche
                if self.frame_count % 500 == 0:
                    avg_reward = np.mean(list(self.reward_history)[-100:]) if len(self.reward_history) >= 100 else 0
                    avg_loss = np.mean(list(self.loss_history)) if len(self.loss_history) > 0 else 0
                    
                    recent_actions = list(self.action_history)[-20:] if len(self.action_history) >= 20 else list(self.action_history)
                    variety = len(set(recent_actions)) / len(recent_actions) if recent_actions else 0
                    
                    print(f"📊 Frame: {self.frame_count:,} | Reward: {self.total_reward:.2f} (avg: {avg_reward:.3f}) | "
                          f"Loss: {avg_loss:.4f} | ε: {self.epsilon:.3f} | "
                          f"Azione: {self.action_names[action]} | Varietà: {variety:.2%}")
                    
                    if variety < 0.3:
                        print("⚠️ Bassa varietà rilevata!")
                    
                    if self.total_reward > self.best_reward:
                        self.best_reward = self.total_reward
                        print(f"🏆 NUOVO RECORD! {self.best_reward:.2f}")
                
                # Aggiorna stato
                previous_screen = next_state
                self.frame_count += 1
                
                # Reset episodio
                if self.frame_count % 30000 == 0:
                    self.episode_count += 1
                    print(f"\n🔄 Fine episodio #{self.episode_count}")
                    print(f"📊 Reward totale: {self.total_reward:.2f}")
                    print(f"🧠 Stati esplorati: {len(self.visited_states)}")
                    
                    # Pulisci memoria ogni tot episodi
                    if self.episode_count % 5 == 0:
                        self._clean_memory()
                    
                    self.frame_count = 0
                    self.total_reward = 0
                    self.visited_states.clear()
                    
        except KeyboardInterrupt:
            print("\n⚠️ Interruzione...")
        
        finally:
            # Salvataggio finale
            print("\n💾 Salvataggio finale...")
            self._save_model()
            self._save_memory()
            self._save_stats()
            
            self.pyboy.stop()
            
            print(f"\n{'='*60}")
            print(f"📊 REPORT FINALE")
            print(f"{'='*60}")
            print(f"✅ Episodi: {self.episode_count}")
            print(f"🏆 Miglior punteggio: {self.best_reward:.2f}")
            print(f"🧠 Modello salvato in: {self.model_path}")


def main():
    """Funzione principale"""
    print("="*60)
    print("🎮 GAME BOY COLOR AI - PYTORCH DEEP LEARNING")
    print("="*60)
    print("\n🔥 Usa PyTorch invece di TensorFlow")
    print("✅ Compatibile con Python 3.13+")
    print("🧠 Deep Q-Network con anti-loop avanzato\n")
    
    # ROM selection
    while True:
        rom_path = input("📁 Percorso del file .gbc: ").strip().strip('"')
        
        if os.path.exists(rom_path) and rom_path.lower().endswith('.gbc'):
            break
        else:
            print("❌ File non valido!")
    
    print(f"\n✅ Gioco: {os.path.basename(rom_path)}")
    
    # Check existing saves
    rom_name = os.path.splitext(os.path.basename(rom_path))[0]
    save_dir = f"ai_saves_{rom_name}"
    if os.path.exists(save_dir):
        print(f"\n📂 Trovati salvataggi esistenti!")
        stats_path = os.path.join(save_dir, "stats.json")
        if os.path.exists(stats_path):
            with open(stats_path, 'r') as f:
                stats = json.load(f)
            print(f"   - Episodi: {stats.get('episodes', 0)}")
            print(f"   - Frame totali: {stats.get('total_frames', 0):,}")
            print(f"   - Miglior punteggio: {stats.get('best_reward', 0):.2f}")
            
            reset = input("\n⚠️ Vuoi RESETTARE? (s/N): ").lower().strip()
            if reset == 's':
                import shutil
                shutil.rmtree(save_dir)
                print("🗑️ Reset completato!")
    
    print("\n🚀 Avvio tra 3 secondi...")
    time.sleep(3)
    
    try:
        ai = PyTorchGameBoyAI(rom_path, headless=False)
        ai.play()
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPremi INVIO per uscire...")


if __name__ == "__main__":
    main()