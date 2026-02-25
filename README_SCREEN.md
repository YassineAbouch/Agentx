# Screen.py - Outil d'analyse de fenêtres Windows

## 🎯 Fonctionnalités

Ce script fait 3 choses principales :

1. ✅ **Liste toutes les fenêtres ouvertes** (titre + position + processus)
2. ✅ **Affiche la fenêtre active** en cours
3. ✅ **Capture d'écran complète** (sauvegardée en `screenshot.png`)
4. ✅ **Bonus : Liste les onglets Chrome** (si Chrome est lancé avec le remote debugging)

## 📋 Installation

### 1. Installer les dépendances Python

```bash
pip install -r requirements_screen.txt
```

Ou manuellement :
```bash
pip install pywin32 psutil mss pillow requests
```

### 2. (Optionnel) Activer le mode debugging Chrome

Pour lister les onglets Chrome ouverts, fermez Chrome puis relancez-le avec :

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**Note** : Adaptez le chemin si Chrome est installé ailleurs.

## 🚀 Utilisation

```bash
python Screen.py
```

## 📤 Résultats

Le script génère :

1. **`screenshot.png`** - Capture d'écran complète
2. **`screen_report.json`** - Rapport JSON détaillé contenant :
   - Timestamp
   - Fenêtre active
   - Liste de toutes les fenêtres ouvertes
   - Onglets Chrome (si disponible)

## 📊 Exemple de sortie

```
Starting Screen.py ...

✅ Screenshot saved: C:\path\to\screenshot.png
✅ Report saved: screen_report.json

Active window: chrome.exe — Google Chrome
Open windows found: 23
Chrome tabs found: 5
  1. GitHub Copilot  |  https://github.com/...
  2. Stack Overflow  |  https://stackoverflow.com/...
  3. ChatGPT  |  https://chat.openai.com/...
```

## 📝 Structure du JSON

```json
{
  "timestamp": "2026-02-25T10:30:00",
  "active_window": {
    "hwnd": 123456,
    "title": "Visual Studio Code",
    "pid": 12345,
    "process": "Code.exe",
    "exe": "C:\\Program Files\\Microsoft VS Code\\Code.exe",
    "bounds": {"x": 100, "y": 100, "w": 1920, "h": 1080}
  },
  "open_windows": [...],
  "screenshot_file": "C:\\path\\to\\screenshot.png",
  "chrome_tabs": {
    "debug_port": 9222,
    "tabs": [...]
  }
}
```

## ⚠️ Compatibilité

- **Windows** : ✅ Supporté nativement (pywin32)
- **macOS** : ⚠️ Nécessite une version adaptée (utilisation de `Quartz`, `AppKit`)
- **Linux** : ⚠️ Nécessite une version adaptée (utilisation de `wmctrl`, `xdotool`)

## 🔧 Notes techniques

- Utilise `win32gui` pour énumérer les fenêtres Windows
- Utilise `mss` pour les captures d'écran rapides
- Utilise l'API Chrome DevTools Protocol pour lister les onglets
- Filtre automatiquement les fenêtres cachées et sans titre

## 💡 Cas d'usage

- Automation de tests
- Monitoring d'applications
- Debug de fenêtres
- Audit de navigation Chrome
- Scripts de productivité
