# 🕹️ Othello AI

Ce projet est une implémentation du jeu **Othello (Reversi)** avec une interface graphique en **Pygame**. Il propose trois modes de jeu :
- Humain vs Humain
- Humain vs IA (Minimax ou Monte Carlo Tree Search)
- IA vs IA (simulation)

Deux intelligences artificielles sont implémentées :
- **Minimax avec élagage alpha-bêta** (`Minimax.py`)
- **Monte Carlo Tree Search (MCTS)** (`MonteCarlo.py`)

Le cœur du jeu est géré par la classe `Board` dans `board.py` et l’interface utilisateur se trouve dans `main.py`.

---

## ✅ Prérequis

- Python **≥ 3.11**
- [Poetry](https://python-poetry.org/docs/#installation)

---

## 🚀 Installation et exécution avec Poetry

1. **Cloner le dépôt**

   ```bash
   git clone <URL_DU_DEPOT>
   cd othelloai
   ```

2. **Installer les dépendances avec Poetry**

   Assure-toi d’avoir installé Poetry, puis exécute :

   ```bash
   poetry install
   ```

   Cela créera un environnement virtuel et installera `pygame` et les autres dépendances définies dans `pyproject.toml`.

3. **Lancer le projet**

   Pour démarrer le jeu :

   ```bash
   poetry run python main.py
   ```

   Cela ouvrira la fenêtre du jeu avec un écran d’accueil interactif.

---

## 📁 Structure des fichiers

```bash
.
├── main.py            # Interface utilisateur et boucle principale du jeu
├── board.py           # Logique du plateau de jeu
├── Minimax.py         # Implémentation de l'IA Minimax
├── MonteCarlo.py      # Implémentation de l'IA Monte Carlo Tree Search
├── pyproject.toml     # Dépendances et configuration Poetry
├── icons/             # Pions noirs et blancs
└── fonts/             # Polices utilisées dans l'interface
```

---

## 👨‍💻 Auteurs

- **Wassim Bouhdid** — 000596875  
- **Leila Bourouf** — 000592462  
- **Maxime Van den Broeck** — 000461666  
