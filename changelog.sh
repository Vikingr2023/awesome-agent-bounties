#!/bin/bash

# Script para gerar CHANGELOG.md estruturado a partir do histórico do Git
# Categoriza commits baseados em Conventional Commits: feat, fix, refactor, etc.

set -e

OUTPUT_FILE="CHANGELOG.md"
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

echo "🚀 Gerando CHANGELOG..."

# Função para extrair commits de uma categoria específica
get_commits() {
    local pattern=$1
    local type=$2
    if [ -z "$LAST_TAG" ]; then
        git log --pretty=format:"- %s (%h)" --grep="^$pattern"
    else
        git log "$LAST_TAG..HEAD" --pretty=format:"- %s (%h)" --grep="^$pattern"
    fi
}

# Início do arquivo
echo "# CHANGELOG" > $OUTPUT_FILE
echo "Gerado automaticamente em $(date +'%Y-%m-%d')" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# Se não houver tag, avisar que pegará todo o histórico
if [ -z "$LAST_TAG" ]; then
    echo "> *Nota: Nenhuma tag encontrada. Gerando a partir do início do histórico.*" >> $OUTPUT_FILE
    echo "" >> $OUTPUT_FILE
else
    echo "> *Desde a última tag: $LAST_TAG*" >> $OUTPUT_FILE
    echo "" >> $OUTPUT_FILE
fi

# Categorização baseada em Conventional Commits
# Added -> feat
# Fixed -> fix
# Changed -> refactor, perf, style
# Removed -> chore, docs (ou conforme lógica de negócio)

# 1. Added
echo "## 🚀 Added" >> $OUTPUT_FILE
COMMITS=$(get_commits "feat" "Added")
if [ -n "$COMMITS" ]; then echo "$COMMITS" >> $OUTPUT_FILE; else echo "_Nenhuma nova funcionalidade._" >> $OUTPUT_FILE; fi
echo "" >> $OUTPUT_FILE

# 2. Fixed
echo "## 🐞 Fixed" >> $OUTPUT_FILE
COMMITS=$(get_commits "fix" "Fixed")
if [ -n "$COMMITS" ]; then echo "$COMMITS" >> $OUTPUT_FILE; else echo "_Nenhum erro corrigido._" >> $OUTPUT_FILE; fi
echo "" >> $OUTPUT_FILE

# 3. Changed
echo "## 🛠️ Changed" >> $OUTPUT_FILE
COMMITS=$(get_commits "refactor\|perf\|style" "Changed")
if [ -n "$COMMITS" ]; then echo "$COMMITS" >> $OUTPUT_FILE; else echo "_Nenhuma alteração de estrutura._" >> $OUTPUT_FILE; fi
echo "" >> $OUTPUT_FILE

# 4. Removed/Other
echo "## 🧹 Removed / Other" >> $OUTPUT_FILE
COMMITS=$(get_commits "chore\|docs\|test" "Removed")
if [ -n "$COMMITS" ]; then echo "$COMMITS" >> $OUTPUT_FILE; else echo "_Nenhuma outra alteração._" >> $OUTPUT_FILE; fi
echo "" >> $OUTPUT_FILE

echo "✅ CHANGELOG.md gerado com sucesso!"
