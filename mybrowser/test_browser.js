// Script de test pour initialiser le navigateur
const fetch = require('node-fetch');

const BASE_URL = 'http://localhost:3000';

async function testBrowser() {
    try {
        console.log('🚀 Test du navigateur...\n');

        // 1. Ouvrir une page
        console.log('1️⃣ Ouverture de example.com...');
        const openResponse = await fetch(`${BASE_URL}/open`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                url: 'https://example.com',
                waitUntil: 'domcontentloaded'
            })
        });
        const openData = await openResponse.json();
        console.log('   Résultat:', openData);

        // 2. Attendre un peu
        console.log('\n2️⃣ Attente de 2 secondes...');
        await new Promise(resolve => setTimeout(resolve, 2000));

        // 3. Prendre un screenshot
        console.log('\n3️⃣ Capture d\'écran...');
        const screenshotResponse = await fetch(`${BASE_URL}/screenshot?fullPage=true`);
        const screenshotData = await screenshotResponse.json();
        console.log('   Résultat:', screenshotData);

        // 4. Obtenir le statut
        console.log('\n4️⃣ Statut du navigateur...');
        const statusResponse = await fetch(`${BASE_URL}/status`);
        const statusData = await statusResponse.json();
        console.log('   URL actuelle:', statusData.url);
        console.log('   Titre:', statusData.title);

        console.log('\n✅ Test terminé avec succès !');
        console.log('📸 Screenshot sauvegardé dans:', screenshotData.path);
        console.log('\n🌐 Ouvrez maintenant http://localhost:3000/control.html');
        console.log('   et cliquez sur "📸 Actualiser" pour voir le screenshot');

    } catch (error) {
        console.error('❌ Erreur:', error.message);
    }
}

testBrowser();
