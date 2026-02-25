# Auto Clicker avec Détection d'Image

Script Python automatisé qui détecte une image à l'écran et clique dessus automatiquement.

## 📋 Prérequis

- Python 3.7 ou supérieur
- Les bibliothèques listées dans `requirements.txt`

## 🚀 Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## 📝 Utilisation

1. Placez l'image que vous souhaitez détecter dans le même dossier que le script et nommez-la `bouton.png`

2. Lancez le script :
```bash
python auto_clicker.py
```

3. Le script va :
   - Vérifier l'écran toutes les 2 secondes
   - Détecter l'image `bouton.png` si elle est présente
   - Cliquer automatiquement au centre de l'image détectée
   - Afficher des messages informatifs dans le terminal

## ⚠️ Arrêt du script

- **Méthode recommandée** : Appuyez sur la touche `q`
- **Méthode alternative** : Utilisez `Ctrl+C` dans le terminal

## ⚙️ Configuration

Vous pouvez modifier les paramètres dans le script `auto_clicker.py` :

- `IMAGE_PATH` : Chemin vers l'image à détecter (par défaut : `bouton.png`)
- `VERIFICATION_INTERVAL` : Intervalle en secondes entre chaque vérification (par défaut : 2)
- `CONFIDENCE_THRESHOLD` : Seuil de confiance pour la détection de 0 à 1 (par défaut : 0.8)

## 🔧 Fonctionnalités

✅ Détection automatique d'image à l'écran  
✅ Clic automatique au centre de l'image  
✅ Messages informatifs en temps réel  
✅ Système d'arrêt sécurisé  
✅ Gestion des erreurs robuste  
✅ Code structuré et commenté  

## 🛡️ Sécurité

Le script inclut plusieurs mécanismes de sécurité :
- Arrêt immédiat avec la touche `q`
- Gestion propre des interruptions (`Ctrl+C`)
- Vérification de l'existence des fichiers
- Gestion complète des exceptions

## 📌 Note importante

**Attention** : Ce script peut interagir avec votre système. Assurez-vous de :
- L'utiliser de manière responsable
- Tester dans un environnement contrôlé d'abord
- Comprendre les actions qu'il effectue
