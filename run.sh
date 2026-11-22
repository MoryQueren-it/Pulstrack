#!/bin/bash
set -e

IMAGE="pulsetrack-app"
CONTAINER="pulsetrack"
PORT=5050

cd "$(dirname "$0")"

if [ ! -f "data.json" ]; then
  echo '{"habits": [], "logs": {}}' > data.json
fi

echo "Build de l'image..."
docker build -t "$IMAGE" .

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "Suppression de l'ancien conteneur..."
  docker rm -f "$CONTAINER" >/dev/null
fi

echo "Lancement du conteneur sur le port $PORT..."
docker run -d \
  --name "$CONTAINER" \
  -p "${PORT}:5000" \
  -v "$(pwd)/data.json:/app/data.json" \
  "$IMAGE"

echo "Application disponible sur http://localhost:${PORT}"
echo "Connexion au conteneur (tape 'exit' pour quitter le shell)..."
docker exec -it "$CONTAINER" /bin/sh