#!/bin/bash

# ==============================================================
# rename_pdfs.sh
# Renomme récursivement tous les PDFs d'un dossier :
#   - Caractères accentués → ASCII lisibles (é→e, è→e, à→a…)
#   - Apostrophes, guillemets → supprimés
#   - Espaces, tirets, virgules, points → underscore
#   - Underscores multiples → un seul
#   - Caractères spéciaux restants → supprimés
#
# Usage :
#   ./rename_pdfs.sh [dossier]        # renommage réel
#   ./rename_pdfs.sh [dossier] dry    # simulation (dry run)
# ==============================================================

TARGET_DIR="${1:-.}"
DRY_RUN="${2:-false}"

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "❌ Dossier introuvable : $TARGET_DIR"
    exit 1
fi

echo "📂 Dossier cible : $(realpath "$TARGET_DIR")"
[[ "$DRY_RUN" == "dry" ]] && echo "🔍 Mode DRY RUN (aucun fichier modifié)"
echo "-------------------------------------------"

# Translittération complète via python3
transliterate() {
    python3 - "$1" <<'EOF'
import sys, unicodedata, urllib.parse, re

def clean(text):
    # 1. Décodage URL (%C3%A9 → é)
    text = urllib.parse.unquote(text)
    # 2. Supprime apostrophes/guillemets
    text = re.sub(r"[''\"'`´]", '', text)
    # 3. Normalisation NFD → sépare lettres et diacritiques
    text = unicodedata.normalize('NFD', text)
    # 4. Table manuelle pour cas non couverts par NFD
    table = str.maketrans({'æ':'ae','Æ':'AE','œ':'oe','Œ':'OE',
                           'ß':'ss','ø':'o','Ø':'O','ð':'d','Ð':'D',
                           'þ':'th','Þ':'TH'})
    text = text.translate(table)
    # 5. Supprimer les diacritiques (accents, cédilles…)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # 6. Remplacer tirets, espaces, virgules, points, parenth. → underscore
    text = re.sub(r'[-\s(),;.\[\]{}]+', '_', text)
    # 7. Supprimer tout caractère non alphanumérique ni underscore
    text = re.sub(r'[^a-zA-Z0-9_]', '', text)
    # 8. Réduire underscores multiples → un seul
    text = re.sub(r'_+', '_', text)
    # 9. Supprimer underscore en début/fin
    text = text.strip('_')
    return text

print(clean(sys.argv[1]))
EOF
}

count=0
skipped=0

while IFS= read -r -d '' filepath; do
    dir=$(dirname "$filepath")
    filename=$(basename "$filepath")
    name="${filename%.pdf}"

    new=$(transliterate "$name")
    new_filename="${new}.pdf"

    if [[ "$filename" == "$new_filename" ]]; then
        ((skipped++))
        continue
    fi

    new_filepath="$dir/$new_filename"

    # Gestion des collisions de noms
    if [[ -e "$new_filepath" && "$new_filepath" != "$filepath" ]]; then
        base="$new"; i=1
        while [[ -e "$dir/${base}_${i}.pdf" ]]; do ((i++)); done
        new_filename="${base}_${i}.pdf"
        new_filepath="$dir/$new_filename"
    fi

    echo "  ✏️  $filename"
    echo "   → $new_filename"

    if [[ "$DRY_RUN" != "dry" ]]; then
        mv "$filepath" "$new_filepath"
    fi
    ((count++))

done < <(find "$TARGET_DIR" -type f -iname "*.pdf" -print0)

echo "-------------------------------------------"
echo "✅ $count fichier(s) renommé(s), $skipped ignoré(s) (déjà propres)"
