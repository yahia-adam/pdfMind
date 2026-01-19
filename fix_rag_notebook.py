import json
import os
import shutil

nb_path = '/home/adam/Documents/adam/pdfMind/rag.ipynb'

try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    changes_made = False

    # 1. Fix OSError by using shutil
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source_lines = cell.get('source', [])
            source_text = "".join(source_lines)
            if "os.removedirs(CHROMA_PATH)" in source_text or "os.remove(CHROMA_PATH)" in source_text:
                new_source = []
                for line in source_lines:
                    if "os.removedirs(CHROMA_PATH)" in line or "os.remove(CHROMA_PATH)" in line:
                        new_source.append("import shutil\n")
                        new_source.append("if os.path.exists(CHROMA_PATH):\n")
                        new_source.append("    shutil.rmtree(CHROMA_PATH)\n")
                    else:
                        new_source.append(line)
                cell['source'] = new_source
                print("Fixed Chroma DB cleanup code.")
                changes_made = True

    # 2. Translate Markdown
    target_text = "## Correctness: Response vs reference answer"
    french_translation = [
        "## Exactitude : Réponse vs réponse de référence\n",
        "- **Objectif** : Mesurer « la similarité/exactitude de la réponse de la chaîne RAG par rapport à une réponse de référence (vérité terrain) »\n",
        "- **Mode** : Nécessite une réponse de référence (vérité terrain) fournie dans un jeu de données\n",
        "- **Évaluateur** : Utiliser un LLM comme juge pour évaluer l'exactitude de la réponse."
    ]

    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            source_lines = cell.get('source', [])
            source_text = "".join(source_lines)
            if target_text in source_text:
                cell['source'] = french_translation
                print("Translated markdown cell.")
                changes_made = True

    if changes_made:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')
        print("Notebook updated successfully.")
    else:
        print("No matching cells found to update.")

except Exception as e:
    print(f"Error updating notebook: {e}")
