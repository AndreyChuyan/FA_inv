#!/bin/bash
# Скрипт переносит код из ветки main gitHUB в ветку import gitLAB

# Настройки
# переменные окружения
# `REPO_NAME`, `GITHUB_REPO_URL`, `GITLAB_REPO_URL`
REPO_NAME="${REPO_NAME:-FA_inv}"
GITHUB_REPO_URL="${GITHUB_REPO_URL:-git@github.com:AndreyChuyan/$REPO_NAME.git}"
GITLAB_REPO_URL="${GITLAB_REPO_URL:-git@gitlab.ch.loc:root/$REPO_NAME.git}"
LOCAL_REPO_DIR="${LOCAL_REPO_DIR:-/tmp/git/$REPO_NAME}"
GITHUB_BRANCH="main"                                
GITLAB_BRANCH="import"                             

# Проверяем, существует ли локальный репозиторий
if [ ! -d "$LOCAL_REPO_DIR" ]; then
    echo "Локальный репозиторий не найден. Клонируем репозиторий GitHub..."
    git clone --branch $GITHUB_BRANCH $GITHUB_REPO_URL $LOCAL_REPO_DIR
else
    echo "Локальный репозиторий найден. Обновляем его с GitHub..."
    cd $LOCAL_REPO_DIR
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "$GITHUB_BRANCH" ]; then
        git checkout $GITHUB_BRANCH
    fi
    git pull origin $GITHUB_BRANCH
fi

# Переходим в локальный репозиторий
cd $LOCAL_REPO_DIR

# Добавляем GitLab как удалённый репозиторий, если он ещё не добавлен
if git remote get-url gitlab &> /dev/null; then
    git remote set-url gitlab $GITLAB_REPO_URL
else
    git remote add gitlab $GITLAB_REPO_URL
fi

# Пушим изменения в GitLab
echo "Пушим изменения в GitLab..."
git push -u gitlab $GITHUB_BRANCH:$GITLAB_BRANCH --force
# git push -u gitlab $GITHUB_BRANCH:$GITLAB_BRANCH

# Завершение
echo "Синхронизация завершена!"