# Git Changelog Generator

Uma ferramenta leve em Bash para gerar um `CHANGELOG.md` estruturado automaticamente a partir do histórico de commits do Git, utilizando o padrão de *Conventional Commits*.

## 🚀 Setup (3 Passos)

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repo>
   cd <nome-do-repo>
   ```

2. **Dê permissão de execução ao script:**
   ```bash
   chmod +x changelog.sh
   ```

3. **Execute o script:**
   ```bash
   ./changelog.sh
   ```

## 🛠️ Como funciona

O script analisa os commits desde a última `git tag` encontrada e os categoriza da seguinte forma:

- **Added**: Commits que começam com `feat:`.
- **Fixed**: Commits que começam com `fix:`.
- **Changed**: Commits que começam com `refactor:`, `perf:` ou `style:`.
- **Removed / Other**: Commits que começam com `chore:`, `docs:` ou `test:`.

## 📝 Exemplo de Saída

```markdown
# CHANGELOG
Gerado automaticamente em 2023-10-27

> *Desde a última tag: v1.0.0*

## 🚀 Added
- add user authentication feature (a1b2c3d)
- implement dark mode support (e5f6g7h)

## 🐞 Fixed
- resolve memory leak in worker (i9j0k1l)

## 🛠️ Changed
- refactor database connection logic (m2n3o4p)

## 🧹 Removed / Other
- update documentation (q5r6s7t)
