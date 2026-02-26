"""
Client Python pour MyBrowser
Wrapper pour interagir avec le serveur de navigateur programmable
"""

import requests
import json
from typing import Optional, Dict, List, Any

class BrowserClient:
    """Client pour contrôler le navigateur via l'API REST"""
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Effectue une requête POST"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        return response.json()
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Effectue une requête GET"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        return response.json()
    
    # ========================================================================
    # NAVIGATION
    # ========================================================================
    
    def open(self, url: str, wait_until: str = "domcontentloaded") -> Dict:
        """
        Ouvre une URL
        
        Args:
            url: URL à ouvrir
            wait_until: 'load', 'domcontentloaded', 'networkidle'
        """
        return self._post("/open", {"url": url, "waitUntil": wait_until})
    
    def back(self) -> Dict:
        """Retourne à la page précédente"""
        return self._post("/nav/back")
    
    def forward(self) -> Dict:
        """Avance à la page suivante"""
        return self._post("/nav/forward")
    
    def reload(self) -> Dict:
        """Recharge la page actuelle"""
        return self._post("/reload")
    
    # ========================================================================
    # INTERACTIONS
    # ========================================================================
    
    def click(self, selector: str, timeout: int = 20000) -> Dict:
        """
        Clique sur un élément
        
        Args:
            selector: Sélecteur CSS de l'élément
            timeout: Timeout en millisecondes
        """
        return self._post("/click", {"selector": selector, "timeout": timeout})
    
    def type(self, selector: str, text: str, clear: bool = True, delay: int = 50) -> Dict:
        """
        Tape du texte dans un élément
        
        Args:
            selector: Sélecteur CSS de l'élément
            text: Texte à taper
            clear: Effacer le contenu existant
            delay: Délai entre chaque touche (ms)
        """
        return self._post("/type", {
            "selector": selector,
            "text": text,
            "clear": clear,
            "delay": delay
        })
    
    def scroll(self, y: int = 800, x: int = 0) -> Dict:
        """
        Fait défiler la page
        
        Args:
            y: Pixels verticaux
            x: Pixels horizontaux
        """
        return self._post("/scroll", {"y": y, "x": x})
    
    def wait(self, selector: str, timeout: int = 30000) -> Dict:
        """
        Attend qu'un élément apparaisse
        
        Args:
            selector: Sélecteur CSS de l'élément
            timeout: Timeout en millisecondes
        """
        return self._post("/wait", {"selector": selector, "timeout": timeout})
    
    def hover(self, selector: str) -> Dict:
        """
        Survole un élément
        
        Args:
            selector: Sélecteur CSS de l'élément
        """
        return self._post("/hover", {"selector": selector})
    
    # ========================================================================
    # EXTRACTION DE CONTENU
    # ========================================================================
    
    def get_text(self) -> str:
        """Récupère tout le texte de la page"""
        result = self._get("/content/text")
        return result.get("text", "")
    
    def get_html(self) -> str:
        """Récupère le HTML de la page"""
        result = self._get("/content/html")
        return result.get("html", "")
    
    def extract(self, selector: str, mode: str = "text", attribute: Optional[str] = None) -> Any:
        """
        Extrait du contenu d'un élément spécifique
        
        Args:
            selector: Sélecteur CSS
            mode: 'text', 'html', ou 'attribute'
            attribute: Nom de l'attribut (si mode='attribute')
        """
        data = {"selector": selector, "mode": mode}
        if attribute:
            data["attribute"] = attribute
        
        result = self._post("/extract", data)
        return result.get("result")
    
    def get_links(self, limit: int = 200) -> List[Dict]:
        """
        Récupère tous les liens de la page
        
        Args:
            limit: Nombre maximum de liens
        """
        result = self._get("/links", {"limit": limit})
        return result.get("links", [])
    
    def get_title(self) -> str:
        """Récupère le titre de la page"""
        result = self._get("/title")
        return result.get("title", "")
    
    # ========================================================================
    # SCREENSHOTS & MEDIA
    # ========================================================================
    
    def screenshot(self, full_page: bool = True) -> str:
        """
        Prend une capture d'écran
        
        Args:
            full_page: Capturer la page entière
            
        Returns:
            Chemin du fichier de capture
        """
        result = self._get("/screenshot", {"fullPage": str(full_page).lower()})
        return result.get("path", "")
    
    def pdf(self) -> str:
        """
        Génère un PDF de la page
        
        Returns:
            Chemin du fichier PDF
        """
        result = self._get("/pdf")
        return result.get("path", "")
    
    # ========================================================================
    # COOKIES
    # ========================================================================
    
    def get_cookies(self) -> List[Dict]:
        """Récupère tous les cookies"""
        result = self._get("/cookies")
        return result.get("cookies", [])
    
    def set_cookies(self, cookies: List[Dict]) -> Dict:
        """
        Définit des cookies
        
        Args:
            cookies: Liste de dictionnaires de cookies
        """
        return self._post("/cookies/set", {"cookies": cookies})
    
    def clear_cookies(self) -> Dict:
        """Efface tous les cookies"""
        return self._post("/cookies/clear")
    
    # ========================================================================
    # UTILITAIRES
    # ========================================================================
    
    def status(self) -> Dict:
        """Vérifie le statut du navigateur"""
        return self._get("/status")
    
    def close(self) -> Dict:
        """Ferme le navigateur"""
        return self._post("/close")
    
    def eval(self, code: str) -> Any:
        """
        Exécute du JavaScript dans la page
        
        Args:
            code: Code JavaScript à exécuter
        """
        result = self._get("/eval", {"code": code})
        return result.get("result")


# ============================================================================
# EXEMPLES D'UTILISATION
# ============================================================================

def example_google_search():
    """Exemple : Recherche Google"""
    browser = BrowserClient()
    
    print("🔍 Recherche Google...")
    
    # Ouvrir Google
    browser.open("https://www.google.com")
    print("✓ Google ouvert")
    
    # Taper dans la barre de recherche
    browser.type("textarea[name=q]", "Playwright automation")
    print("✓ Texte tapé")
    
    # Attendre un peu
    import time
    time.sleep(1)
    
    # Récupérer les suggestions ou faire Enter
    # browser.click("input[name=btnK]")
    
    # Extraire le contenu
    text = browser.get_text()
    print(f"✓ Texte extrait : {len(text)} caractères")
    
    # Screenshot
    screenshot_path = browser.screenshot()
    print(f"✓ Screenshot : {screenshot_path}")


def example_extract_article():
    """Exemple : Extraire un article"""
    browser = BrowserClient()
    
    print("📰 Extraction d'article...")
    
    # Ouvrir une page de blog
    browser.open("https://example.com")
    
    # Extraire le titre
    title = browser.extract("h1", mode="text")
    print(f"Titre : {title}")
    
    # Extraire le contenu
    content = browser.extract("article", mode="html")
    print(f"Contenu : {len(content)} caractères")
    
    # Lister les liens
    links = browser.get_links(limit=10)
    print(f"Liens trouvés : {len(links)}")
    for link in links[:5]:
        print(f"  - {link['text'][:50]} -> {link['href']}")


def example_navigation():
    """Exemple : Navigation complète"""
    browser = BrowserClient()
    
    print("🌐 Test de navigation...")
    
    # Vérifier le statut
    status = browser.status()
    print(f"Statut : {status}")
    
    # Ouvrir une page
    result = browser.open("https://example.com")
    print(f"✓ Page ouverte : {result.get('title')}")
    
    # Récupérer le titre
    title = browser.get_title()
    print(f"✓ Titre : {title}")
    
    # Scroll
    browser.scroll(y=500)
    print("✓ Scroll effectué")
    
    # Screenshot
    screenshot = browser.screenshot()
    print(f"✓ Screenshot : {screenshot}")


if __name__ == "__main__":
    print("=" * 60)
    print("Client Python MyBrowser")
    print("=" * 60)
    print("\nAssurez-vous que le serveur est lancé :")
    print("  cd mybrowser && node server.js")
    print("\nExemples disponibles :")
    print("  - example_google_search()")
    print("  - example_extract_article()")
    print("  - example_navigation()")
    print("=" * 60)
    
    # Décommenter pour tester
    # example_navigation()
