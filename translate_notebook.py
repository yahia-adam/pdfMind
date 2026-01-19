import json

file_path = '/home/adam/Documents/adam/pdfMind/rag.ipynb'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    found = False
    for cell in data['cells']:
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            # Check if this is the target cell
            if len(source) > 0 and "## Correctness: Response vs reference answer" in source[0]:
                print("Found target cell.")
                cell['source'] = [
                    "## Exactitude : Réponse vs réponse de référence\n",
                    "- **Objectif** : Mesurer « la similarité/exactitude de la réponse de la chaîne RAG par rapport à une réponse de référence (vérité terrain) »\n",
                    "- **Mode** : Nécessite une réponse de référence (vérité terrain) fournie dans un jeu de données\n",
                    "- **Évaluateur** : Utiliser un LLM comme juge pour évaluer l'exactitude de la réponse."
                ]
                found = True
                break

    if not found:
        print("Target cell not found.")
        exit(1)

    with open(file_path, 'w', encoding='utf-8') as f:
        # Use indent=1 to match the apparent single-space indentation of the original file
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write('\n') # Add trailing newline

    print("File updated successfully.")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
