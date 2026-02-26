#!/usr/bin/env python3
"""
Script pour extraire toutes les données d'une page web
Utilise le serveur MyBrowser pour l'extraction
"""

import sys
import time
import json
from client import BrowserClient

def extract_page_data(url):
    """
    Extrait toutes les données d'une page web
    """
    print("=" * 80)
    print(f"🌐 EXTRACTION DE DONNÉES: {url}")
    print("=" * 80)
    print()
    
    # Initialiser le client
    browser = BrowserClient()
    
    # 1. OUVRIR LA PAGE
    print("📂 Ouverture de la page...")
    result = browser.open(url, wait_until="networkidle")
    
    if not result.get('ok'):
        print(f"❌ Erreur lors de l'ouverture: {result.get('error')}")
        return
    
    print(f"✅ Page ouverte: {result.get('title')}")
    print(f"   URL finale: {result.get('url')}")
    print()
    
    # Attendre que la page soit complètement chargée
    time.sleep(2)
    
    # 2. INFORMATIONS GÉNÉRALES
    print("📊 INFORMATIONS GÉNÉRALES")
    print("-" * 80)
    
    title = browser.get_title()
    print(f"Titre: {title}")
    
    current_url = browser.status().get('url')
    print(f"URL: {current_url}")
    print()
    
    # 3. EXTRACTION DES LIENS
    print("🔗 LIENS TROUVÉS")
    print("-" * 80)
    
    links = browser.get_links(limit=500)
    print(f"Nombre total de liens: {len(links)}")
    print()
    
    # Catégoriser les liens
    internal_links = []
    external_links = []
    navigation_links = []
    
    for link in links:
        href = link.get('href', '')
        text = link.get('text', '').strip()
        
        if not href or href.startswith('#'):
            continue
            
        if url in href or href.startswith('/'):
            internal_links.append(link)
            # Liens de navigation (menu, etc.)
            if text and len(text) < 30:
                navigation_links.append(link)
        else:
            external_links.append(link)
    
    print(f"✓ Liens internes: {len(internal_links)}")
    print(f"✓ Liens externes: {len(external_links)}")
    print(f"✓ Liens de navigation: {len(navigation_links)}")
    print()
    
    # Afficher les liens de navigation
    if navigation_links:
        print("📌 NAVIGATION PRINCIPALE:")
        for i, link in enumerate(navigation_links[:20], 1):
            text = link.get('text', '').strip()
            href = link.get('href', '')
            if text:
                print(f"  {i}. {text[:50]} → {href}")
        print()
    
    # Afficher quelques liens internes
    if internal_links:
        print("📄 LIENS INTERNES (échantillon):")
        for i, link in enumerate(internal_links[:10], 1):
            text = link.get('text', '').strip() or '[Sans texte]'
            href = link.get('href', '')
            print(f"  {i}. {text[:60]} → {href}")
        print()
    
    # Afficher quelques liens externes
    if external_links:
        print("🌍 LIENS EXTERNES (échantillon):")
        for i, link in enumerate(external_links[:10], 1):
            text = link.get('text', '').strip() or '[Sans texte]'
            href = link.get('href', '')
            print(f"  {i}. {text[:60]} → {href}")
        print()
    
    # 4. EXTRACTION DU CONTENU TEXTUEL
    print("📝 CONTENU TEXTUEL")
    print("-" * 80)
    
    text_content = browser.get_text()
    text_lines = [line.strip() for line in text_content.split('\n') if line.strip()]
    
    print(f"Nombre de lignes de texte: {len(text_lines)}")
    print(f"Nombre de caractères: {len(text_content)}")
    print()
    
    # Extraire les titres
    print("📌 TITRES ET SECTIONS:")
    try:
        # Essayer d'extraire les titres H1
        h1_titles = browser.eval("Array.from(document.querySelectorAll('h1')).map(h => h.innerText)")
        if h1_titles and isinstance(h1_titles, list):
            for i, title in enumerate(h1_titles[:5], 1):
                print(f"  H1 {i}: {title[:100]}")
        
        # Essayer d'extraire les titres H2
        h2_titles = browser.eval("Array.from(document.querySelectorAll('h2')).map(h => h.innerText)")
        if h2_titles and isinstance(h2_titles, list):
            for i, title in enumerate(h2_titles[:10], 1):
                print(f"  H2 {i}: {title[:100]}")
    except Exception as e:
        print(f"  Erreur lors de l'extraction des titres: {e}")
    
    print()
    
    # 5. EXTRACTION DES IMAGES
    print("🖼️  IMAGES")
    print("-" * 80)
    
    try:
        images = browser.eval("""
            Array.from(document.querySelectorAll('img')).map(img => ({
                src: img.src,
                alt: img.alt || '',
                title: img.title || ''
            })).slice(0, 20)
        """)
        
        if images and isinstance(images, list):
            print(f"Nombre d'images trouvées: {len(images)}")
            for i, img in enumerate(images[:10], 1):
                alt = img.get('alt', '')[:50] or '[Sans description]'
                src = img.get('src', '')[:80]
                print(f"  {i}. {alt} → {src}")
        else:
            print("Aucune image trouvée")
    except Exception as e:
        print(f"Erreur lors de l'extraction des images: {e}")
    
    print()
    
    # 6. EXTRACTION DES MÉTADONNÉES
    print("🏷️  MÉTADONNÉES")
    print("-" * 80)
    
    try:
        meta_description = browser.eval("document.querySelector('meta[name=\"description\"]')?.content")
        if meta_description:
            print(f"Description: {meta_description}")
        
        meta_keywords = browser.eval("document.querySelector('meta[name=\"keywords\"]')?.content")
        if meta_keywords:
            print(f"Mots-clés: {meta_keywords}")
        
        og_title = browser.eval("document.querySelector('meta[property=\"og:title\"]')?.content")
        if og_title:
            print(f"Open Graph Title: {og_title}")
        
        og_image = browser.eval("document.querySelector('meta[property=\"og:image\"]')?.content")
        if og_image:
            print(f"Open Graph Image: {og_image}")
    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées: {e}")
    
    print()
    
    # 7. CAPTURE D'ÉCRAN
    print("📸 CAPTURE D'ÉCRAN")
    print("-" * 80)
    
    screenshot_path = browser.screenshot(full_page=True)
    print(f"✅ Screenshot sauvegardé: {screenshot_path}")
    print()
    
    # 8. SAUVEGARDER LES DONNÉES DANS UN FICHIER JSON
    print("💾 SAUVEGARDE DES DONNÉES")
    print("-" * 80)
    
    data = {
        "url": current_url,
        "title": title,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "links": {
            "total": len(links),
            "internal": len(internal_links),
            "external": len(external_links),
            "navigation": [{"text": l.get('text'), "href": l.get('href')} for l in navigation_links[:20]],
            "internal_sample": [{"text": l.get('text'), "href": l.get('href')} for l in internal_links[:20]],
            "external_sample": [{"text": l.get('text'), "href": l.get('href')} for l in external_links[:20]]
        },
        "content": {
            "text_length": len(text_content),
            "lines": len(text_lines),
            "sample": text_lines[:10]
        },
        "screenshot": screenshot_path
    }
    
    filename = f"extraction_{int(time.time())}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Données sauvegardées dans: {filename}")
    print()
    
    # 9. RÉSUMÉ
    print("=" * 80)
    print("✅ EXTRACTION TERMINÉE")
    print("=" * 80)
    print(f"URL: {current_url}")
    print(f"Titre: {title}")
    print(f"Liens trouvés: {len(links)} (internes: {len(internal_links)}, externes: {len(external_links)})")
    print(f"Texte: {len(text_content)} caractères")
    print(f"Screenshot: {screenshot_path}")
    print(f"Données JSON: {filename}")
    print("=" * 80)


if __name__ == "__main__":
    # URL par défaut ou depuis les arguments
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.digisense.es"
    
    # S'assurer que l'URL a un protocole
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        extract_page_data(url)
    except KeyboardInterrupt:
        print("\n\n🛑 Extraction interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
