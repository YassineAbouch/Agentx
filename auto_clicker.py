"""
Script de détection et clic automatique d'image à l'écran
Utilise pyautogui et opencv pour détecter une image (bouton.png) et cliquer dessus
"""

import pyautogui
import cv2
import numpy as np
import time
import sys
import threading
import math

# Configuration
IMAGE_PATH = 'bouton.png'
VERIFICATION_INTERVAL = 2  # Secondes entre chaque vérification
CONFIDENCE_THRESHOLD = 0.8  # Seuil de confiance pour la détection (0-1)

# Variable globale pour l'arrêt
stop_script = False

# Désactiver la protection pyautogui pour permettre les mouvements
pyautogui.FAILSAFE = True  # Déplacer la souris dans le coin pour arrêter

def find_image_on_screen(image_path):
    """
    Recherche une image sur l'écran et retourne ses coordonnées centrales
    
    Args:
        image_path (str): Chemin vers l'image à détecter
        
    Returns:
        tuple: Coordonnées (x, y) du centre de l'image, ou None si non trouvée
    """
    try:
        # Capture d'écran
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        
        # Chargement de l'image template à détecter
        template = cv2.imread(image_path)
        if template is None:
            print(f"❌ Erreur : L'image '{image_path}' n'a pas pu être chargée.")
            print("   Vérifiez que le fichier existe dans le répertoire courant.")
            return None
        
        # Recherche de l'image dans la capture d'écran
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Vérification du seuil de confiance
        if max_val >= CONFIDENCE_THRESHOLD:
            # Calcul des coordonnées du centre de l'image détectée
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y, max_val)
        else:
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de la détection : {e}")
        return None

def click_at_position(coords):
    """
    Effectue un clic à la position donnée
    
    Args:
        coords (tuple): Coordonnées (x, y) où cliquer
    """
    try:
        x, y, confidence = coords
        print(f"✓ Image trouvée à ({x}, {y}) avec {confidence*100:.1f}% de confiance")
        print(f"  → Clic en cours...")
        pyautogui.click(x, y)
        print(f"  → Clic effectué avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors du clic : {e}")

def mouse_circle_demo():
    """
    Démonstration : Fait bouger la souris en cercle au démarrage
    """
    print("\n🎮 DÉMONSTRATION : Contrôle de la souris")
    print("=" * 60)
    print("La souris va maintenant effectuer des mouvements circulaires...")
    print("⚠️  Déplacez la souris dans le coin supérieur gauche pour arrêter")
    print()
    
    # Obtenir la position actuelle de la souris
    start_x, start_y = pyautogui.position()
    print(f"📍 Position de départ : ({start_x}, {start_y})")
    
    # Obtenir la taille de l'écran
    screen_width, screen_height = pyautogui.size()
    
    # Centre de l'écran pour le cercle
    center_x = screen_width // 2
    center_y = screen_height // 2
    radius = 200  # Rayon du cercle en pixels
    
    print(f"🎯 Centre du cercle : ({center_x}, {center_y})")
    print(f"📏 Rayon : {radius} pixels")
    print(f"⏱️  Durée : 5 secondes\n")
    
    time.sleep(1)
    print("🚀 Démarrage dans 3...")
    time.sleep(1)
    print("🚀 2...")
    time.sleep(1)
    print("🚀 1...\n")
    
    # Déplacer la souris au point de départ du cercle
    pyautogui.moveTo(center_x + radius, center_y, duration=0.5)
    
    # Faire 3 tours complets
    num_circles = 3
    points_per_circle = 50
    total_duration = 5  # secondes
    delay = total_duration / (num_circles * points_per_circle)
    
    print("🔄 Mouvements circulaires en cours...\n")
    
    for circle in range(num_circles):
        for i in range(points_per_circle):
            angle = (2 * math.pi * i) / points_per_circle
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            pyautogui.moveTo(x, y, duration=delay)
            time.sleep(delay / 2)
        
        print(f"✓ Tour {circle + 1}/{num_circles} terminé")
    
    # Retourner à la position de départ
    print("\n↩️  Retour à la position de départ...")
    pyautogui.moveTo(start_x, start_y, duration=1)
    
    print("\n✅ Démonstration terminée !")
    print("=" * 60)
    print()

def analyze_screen_content():
    """
    Analyse le contenu de l'écran avec OpenCV
    Détecte : couleurs dominantes, contours, zones d'intérêt, texte potentiel
    """
    print("\n🔍 ANALYSE DU CONTENU DE L'ÉCRAN")
    print("=" * 60)
    
    try:
        # Capture d'écran
        print("📸 Capture de l'écran en cours...")
        screenshot = pyautogui.screenshot()
        screen_array = np.array(screenshot)
        screen_bgr = cv2.cvtColor(screen_array, cv2.COLOR_RGB2BGR)
        
        height, width = screen_bgr.shape[:2]
        print(f"📐 Dimensions de l'écran : {width}x{height} pixels")
        
        # 1. ANALYSE DES COULEURS DOMINANTES
        print("\n🎨 Analyse des couleurs dominantes...")
        pixels = screen_bgr.reshape(-1, 3)
        pixels_float = np.float32(pixels)
        
        # K-means pour trouver les 5 couleurs principales
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 5
        _, labels, centers = cv2.kmeans(pixels_float, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        centers = np.uint8(centers)
        print("   Top 5 couleurs (BGR) :")
        for i, color in enumerate(centers):
            b, g, r = color
            print(f"   {i+1}. RGB({r}, {g}, {b}) - #{r:02x}{g:02x}{b:02x}")
        
        # 2. DÉTECTION DES CONTOURS
        print("\n📐 Détection des contours...")
        gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrer les contours significatifs (surface > 1000 pixels)
        significant_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
        print(f"   ✓ {len(significant_contours)} zones significatives détectées")
        
        # Afficher les 5 plus grandes zones
        sorted_contours = sorted(significant_contours, key=cv2.contourArea, reverse=True)[:5]
        print("   Top 5 zones par taille :")
        for i, cnt in enumerate(sorted_contours):
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            print(f"   {i+1}. Position: ({x}, {y}), Taille: {w}x{h}px, Surface: {int(area)}px²")
        
        # 3. DÉTECTION DE ZONES LUMINEUSES
        print("\n💡 Détection des zones lumineuses...")
        hsv = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2HSV)
        _, _, v = cv2.split(hsv)
        bright_threshold = 200
        bright_pixels = np.sum(v > bright_threshold)
        bright_percentage = (bright_pixels / (width * height)) * 100
        print(f"   ✓ {bright_percentage:.2f}% de pixels lumineux (> {bright_threshold}/255)")
        
        # 4. DÉTECTION DE MOUVEMENTS / ZONES ACTIVES (zones avec beaucoup de détails)
        print("\n🎯 Analyse des zones riches en détails...")
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        activity = np.abs(laplacian).mean()
        print(f"   ✓ Niveau d'activité visuelle : {activity:.2f}")
        if activity > 50:
            print("   → Écran avec beaucoup de détails (texte, images)")
        elif activity > 20:
            print("   → Écran avec détails modérés")
        else:
            print("   → Écran peu détaillé (couleurs unies)")
        
        # 5. DÉTECTION DE RECTANGLES (boutons, fenêtres)
        print("\n🔲 Détection de formes rectangulaires...")
        rectangles = []
        for cnt in significant_contours[:20]:  # Analyser les 20 plus grands contours
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            
            if len(approx) == 4:  # Rectangle
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)
                if 0.5 < aspect_ratio < 5:  # Filtrer les rectangles trop étirés
                    rectangles.append((x, y, w, h))
        
        print(f"   ✓ {len(rectangles)} rectangles détectés (boutons potentiels)")
        if rectangles[:3]:
            print("   Top 3 rectangles :")
            for i, (x, y, w, h) in enumerate(rectangles[:3]):
                print(f"   {i+1}. Position: ({x}, {y}), Taille: {w}x{h}px")
        
        # 6. STATISTIQUES GÉNÉRALES
        print("\n📊 Statistiques générales :")
        mean_color = cv2.mean(screen_bgr)[:3]
        print(f"   • Couleur moyenne (BGR) : ({int(mean_color[0])}, {int(mean_color[1])}, {int(mean_color[2])})")
        print(f"   • Luminosité moyenne : {int(v.mean())}/255")
        print(f"   • Contraste (écart-type) : {int(v.std())}")
        
        # Détecter si l'écran est plutôt clair ou sombre
        if v.mean() > 150:
            print("   • Thème : 🌞 Clair (mode jour)")
        elif v.mean() > 80:
            print("   • Thème : 🌤️  Neutre")
        else:
            print("   • Thème : 🌙 Sombre (mode nuit)")
        
        print("\n✅ Analyse terminée !")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse : {e}")
        print()

def check_for_quit():
    """
    Fonction pour vérifier si l'utilisateur veut arrêter (mode macOS compatible)
    """
    global stop_script
    print("💡 Astuce: Utilisez Ctrl+C dans le terminal pour arrêter le script")

def main():
    """
    Fonction principale - Boucle de détection et clic
    """
    print("=" * 60)
    print("🔍 Script de détection et clic automatique")
    print("=" * 60)
    print(f"📁 Image recherchée : {IMAGE_PATH}")
    print(f"⏱️  Intervalle de vérification : {VERIFICATION_INTERVAL} secondes")
    print(f"🎯 Seuil de confiance : {CONFIDENCE_THRESHOLD*100}%")
    print("\n⚠️  ARRÊT : Utilisez Ctrl+C dans le terminal pour arrêter")
    print("=" * 60)
    print()
    
    # DÉMONSTRATION : Mouvements circulaires de la souris au démarrage
    try:
        mouse_circle_demo()
        time.sleep(2)
    except Exception as e:
        print(f"⚠️  Erreur pendant la démonstration : {e}")
        print("   Le script continue...\n")
    
    # ANALYSE DU CONTENU DE L'ÉCRAN
    try:
        analyze_screen_content()
        time.sleep(2)
    except Exception as e:
        print(f"⚠️  Erreur pendant l'analyse : {e}")
        print("   Le script continue...\n")
    
    try:
        iteration = 0
        while not stop_script:
            iteration += 1
            print(f"\n[Itération #{iteration}] Recherche de l'image...")
            
            # Recherche de l'image
            coords = find_image_on_screen(IMAGE_PATH)
            
            if coords:
                # Image trouvée - Clic
                click_at_position(coords)
            else:
                # Image non trouvée
                print("ℹ️  Image non trouvée à l'écran")
            
            # Attente avant la prochaine vérification
            print(f"⏳ Attente de {VERIFICATION_INTERVAL} secondes...")
            time.sleep(VERIFICATION_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt manuel détecté (Ctrl+C)")
        print("   Fin du script.")
    except Exception as e:
        print(f"\n❌ Erreur critique : {e}")
    finally:
        print("\n" + "=" * 60)
        print("✓ Script terminé proprement")
        print("=" * 60)

if __name__ == "__main__":
    main()
