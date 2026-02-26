# MyBrowser - Programmable Browser Controller

Contrôleur de navigateur puissant basé sur Playwright avec une API REST complète.

## 🚀 Installation

```bash
cd mybrowser
npm install
npm run install-browsers
```

## ▶️ Démarrage

```bash
npm start
```

Le serveur démarre sur `http://localhost:3000`

## 📝 API Endpoints

### Navigation

#### Ouvrir une URL
```bash
curl -X POST http://localhost:3000/open \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

#### Retour / Avance / Reload
```bash
curl -X POST http://localhost:3000/nav/back
curl -X POST http://localhost:3000/nav/forward
curl -X POST http://localhost:3000/reload
```

### Interactions

#### Cliquer sur un élément
```bash
curl -X POST http://localhost:3000/click \
  -H "Content-Type: application/json" \
  -d '{"selector": "button.submit"}'
```

#### Taper du texte
```bash
curl -X POST http://localhost:3000/type \
  -H "Content-Type: application/json" \
  -d '{"selector": "input[name=search]", "text": "hello world"}'
```

#### Scroller
```bash
curl -X POST http://localhost:3000/scroll \
  -H "Content-Type: application/json" \
  -d '{"y": 1000}'
```

#### Attendre un élément
```bash
curl -X POST http://localhost:3000/wait \
  -H "Content-Type: application/json" \
  -d '{"selector": ".loading-complete"}'
```

#### Hover (survoler)
```bash
curl -X POST http://localhost:3000/hover \
  -H "Content-Type: application/json" \
  -d '{"selector": ".menu-item"}'
```

### Extraction de contenu

#### Récupérer le texte de la page
```bash
curl http://localhost:3000/content/text
```

#### Récupérer le HTML
```bash
curl http://localhost:3000/content/html
```

#### Extraire un élément spécifique
```bash
# Texte
curl -X POST http://localhost:3000/extract \
  -H "Content-Type: application/json" \
  -d '{"selector": "h1", "mode": "text"}'

# HTML
curl -X POST http://localhost:3000/extract \
  -H "Content-Type: application/json" \
  -d '{"selector": ".article", "mode": "html"}'

# Attribut
curl -X POST http://localhost:3000/extract \
  -H "Content-Type: application/json" \
  -d '{"selector": "img", "mode": "attribute", "attribute": "src"}'
```

#### Lister tous les liens
```bash
curl http://localhost:3000/links
curl "http://localhost:3000/links?limit=50"
```

#### Récupérer le titre
```bash
curl http://localhost:3000/title
```

### Screenshots & PDF

#### Capture d'écran
```bash
curl "http://localhost:3000/screenshot?fullPage=true"
```

#### Générer un PDF
```bash
curl http://localhost:3000/pdf
```

### Cookies

#### Récupérer les cookies
```bash
curl http://localhost:3000/cookies
```

#### Définir des cookies
```bash
curl -X POST http://localhost:3000/cookies/set \
  -H "Content-Type: application/json" \
  -d '{"cookies": [{"name": "session", "value": "abc123", "domain": ".example.com", "path": "/"}]}'
```

#### Effacer les cookies
```bash
curl -X POST http://localhost:3000/cookies/clear
```

### Utilitaires

#### Vérifier le statut
```bash
curl http://localhost:3000/status
```

#### Exécuter du JavaScript
```bash
curl "http://localhost:3000/eval?code=document.title"
curl "http://localhost:3000/eval?code=window.location.href"
```

#### Fermer le navigateur
```bash
curl -X POST http://localhost:3000/close
```

## 🎯 Exemples d'utilisation

### Exemple 1 : Recherche Google
```bash
# Ouvrir Google
curl -X POST http://localhost:3000/open \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Taper dans la barre de recherche
curl -X POST http://localhost:3000/type \
  -H "Content-Type: application/json" \
  -d '{"selector": "textarea[name=q]", "text": "Playwright automation"}'

# Cliquer sur le bouton de recherche
curl -X POST http://localhost:3000/click \
  -H "Content-Type: application/json" \
  -d '{"selector": "input[name=btnK]"}'

# Attendre les résultats
curl -X POST http://localhost:3000/wait \
  -H "Content-Type: application/json" \
  -d '{"selector": "#search"}'

# Extraire les liens
curl http://localhost:3000/links
```

### Exemple 2 : Navigation et extraction
```bash
# Ouvrir une page de blog
curl -X POST http://localhost:3000/open \
  -H "Content-Type: application/json" \
  -d '{"url": "https://blog.example.com"}'

# Extraire le titre de l'article
curl -X POST http://localhost:3000/extract \
  -H "Content-Type: application/json" \
  -d '{"selector": "article h1", "mode": "text"}'

# Extraire le contenu
curl -X POST http://localhost:3000/extract \
  -H "Content-Type: application/json" \
  -d '{"selector": "article .content", "mode": "html"}'

# Faire une capture d'écran
curl http://localhost:3000/screenshot
```

## 🛡️ Sécurité

### Whitelist de domaines
Modifiez `server.js` pour restreindre les domaines :

```javascript
const CONFIG = {
  allowedDomains: ['example.com', 'mysite.com']  // Empty = all allowed
};
```

### Timeouts
Tous les endpoints ont des timeouts configurables pour éviter les blocages.

### Rate limiting
Ajoutez un middleware Express pour limiter les requêtes :

```bash
npm install express-rate-limit
```

## ⚙️ Configuration

Modifiez les paramètres dans `server.js` :

```javascript
const CONFIG = {
  headless: false,           // true = mode invisible
  timeout: 45000,            // timeout par défaut (ms)
  allowedDomains: [],        // whitelist de domaines
  maxScreenshots: 50,        // limite de screenshots
  userAgent: "..."           // user agent personnalisé
};
```

## 🔧 Gestion des cas complexes

### Captcha / Cloudflare
- Mode `headless: false` permet l'intervention manuelle
- Le navigateur reste ouvert pour que vous complétiez le captcha
- Utilisez `/wait` pour attendre que vous ayez terminé

### Pages React / SPA
```bash
# Attendre le réseau idle
curl -X POST http://localhost:3000/open \
  -H "Content-Type: application/json" \
  -d '{"url": "https://react-app.com", "waitUntil": "networkidle"}'
```

### Lazy loading
```bash
# Scroller progressivement
curl -X POST http://localhost:3000/scroll -d '{"y": 1000}'
# Attendre le nouveau contenu
curl -X POST http://localhost:3000/wait -d '{"selector": ".new-items"}'
```

## 📂 Structure des fichiers

```
mybrowser/
├── server.js           # Serveur principal
├── package.json        # Dépendances
├── screenshots/        # Screenshots générés
└── pdfs/              # PDFs générés
```

## 🐛 Debugging

Vérifiez le statut du navigateur :
```bash
curl http://localhost:3000/status
```

Logs détaillés dans la console du serveur.

## 💡 Tips

1. **Mode headless** : Activez `headless: true` pour la production
2. **Cookies** : Sauvegardez les cookies pour maintenir les sessions
3. **Selectors** : Utilisez les CSS selectors (`.class`, `#id`, `[attribute]`)
4. **Timeouts** : Augmentez les timeouts pour les pages lentes
5. **Screenshots** : Créez le dossier `screenshots/` et `pdfs/` avant utilisation

## 📦 Dépendances

- **express** : Serveur HTTP
- **playwright** : Automatisation de navigateur

## 🚀 Next Steps

- [ ] CLI wrapper (`mybrowser open`, `mybrowser click`)
- [ ] UI Electron pour contrôle visuel
- [ ] Mode "readable" avec extraction intelligente
- [ ] WebSocket pour notifications en temps réel
- [ ] Queue de tâches pour automatisation batch
