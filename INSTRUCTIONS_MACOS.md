# ⚠️ Configuration requise pour macOS

## Problème actuel
Le script ne peut pas capturer l'écran car macOS bloque l'accès par défaut pour des raisons de sécurité.

**Erreur rencontrée** : `could not create image from display`

## 🔧 Solution : Accorder les permissions

### Étape 1 : Ouvrir les Préférences Système
1. Cliquez sur le menu Apple () en haut à gauche
2. Sélectionnez **Réglages Système** (ou **Préférences Système** sur les anciennes versions)

### Étape 2 : Configurer les permissions
1. Allez dans **Confidentialité et sécurité**
2. Cliquez sur **Enregistrement de l'écran** dans la liste à gauche
3. Cherchez **Terminal** ou **iTerm** (selon ce que vous utilisez)
4. **Activez la case à cocher** à côté de Terminal/iTerm

### Étape 3 : Redémarrer le Terminal
1. **Fermez complètement** l'application Terminal
2. **Rouvrez** Terminal
3. Relancez le script :
   ```bash
   cd /Users/yassineabouch/Workspace/AgentX
   python3 auto_clicker.py
   ```

## 📝 Note importante
- Vous devrez peut-être également activer **Accessibilité** dans la même section pour que le clic automatique fonctionne
- Ces permissions sont nécessaires une seule fois

## 🧪 Test rapide
Une fois les permissions accordées, ouvrez l'image bouton.png :
```bash
open bouton.png
```

Puis lancez le script :
```bash
python3 auto_clicker.py
```

Le script devrait maintenant détecter et cliquer sur l'image ! 🎉
