#!/bin/bash
# Deploy Amazi music page to VPS
# Usage: bash deploy.sh

VPS="root@72.62.22.12"
REMOTE_DIR="/var/www/amazi"
MUSIC_SRC="/c/Users/kamel/Downloads/amazi music"

echo "==> Création du dossier sur le VPS..."
ssh $VPS "mkdir -p $REMOTE_DIR/music"

echo "==> Upload de la page HTML..."
scp index.html $VPS:$REMOTE_DIR/

echo "==> Upload des fichiers MP3..."
scp "$MUSIC_SRC/Riad — Sérénité Orientale.mp3"      $VPS:$REMOTE_DIR/music/riad.mp3
scp "$MUSIC_SRC/Rif Eternal — Café Amazigh.mp3"      $VPS:$REMOTE_DIR/music/rif-eternal.mp3
scp "$MUSIC_SRC/Tafaska — Âme du Café Amazigh.mp3"   $VPS:$REMOTE_DIR/music/tafaska.mp3
scp "$MUSIC_SRC/Tifinagh — Voix du Désert.mp3"        $VPS:$REMOTE_DIR/music/tifinagh.mp3
scp "$MUSIC_SRC/Ya Leil — Âme du Café Oriental.mp3"  $VPS:$REMOTE_DIR/music/ya-leil.mp3

echo "==> Configuration Nginx..."
ssh $VPS "cat > /etc/nginx/sites-available/amazi << 'EOF'
server {
    listen 80;
    server_name DOMAINE_ICI;

    root /var/www/amazi;
    index index.html;

    location / {
        try_files \$uri \$uri/ =404;
    }

    location /music/ {
        add_header Content-Disposition 'attachment';
        add_header Cache-Control 'public, max-age=86400';
    }

    # CORS pour les navigateurs mobiles
    add_header Access-Control-Allow-Origin '*';
}
EOF"

ssh $VPS "ln -sf /etc/nginx/sites-available/amazi /etc/nginx/sites-enabled/amazi && nginx -t && systemctl reload nginx"

echo ""
echo "✅ Déployé ! Remplace DOMAINE_ICI dans /etc/nginx/sites-available/amazi par le bon domaine."
echo "   Puis : certbot --nginx -d ton-domaine.com"
