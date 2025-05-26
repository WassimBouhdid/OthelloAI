# Othello AI Game

Ce programme permet de lancer une série de parties d'Othello entre deux joueurs (humains ou intelligences artificielles).

## 🧠 Joueurs disponibles

Chaque joueur peut être l'un des suivants :

- `human` : un joueur humain
- `minimax` : une IA utilisant l'algorithme Minimax
- `montecarlo` : une IA utilisant la méthode Monte Carlo Tree Search

## ⚙️ Utilisation

### Exécution de base

```bash
python main.py Player1 Player2 Rounds
```

```bash
python main.py minimax mcts 10
```