#!/bin/bash
# Скрипт переносит код из ветки main GitLab в ветку import GitHub

# Настройки
# Переменные окружения: REPO_NAME, GITHUB_REPO_URL, GITLAB_REPO_URL
REPO_NAME="${REPO_NAME:-FA_inv}"
GITHUB_REPO_URL="${GITHUB_REPO_URL:-git@github.com:AndreyChuyan/$REPO_NAME.git}"
GITLAB_REPO_URL="${GITLAB_REPO_URL:-git@gitlab.ch.loc:root/$REPO_NAME.git}"
LOCAL_REPO_DIR="${LOCAL_REPO_DIR:-/tmp/git/$REPO_NAME}"
GITHUB_BRANCH="import"
GITLAB_BRANCH="main"

# Проверяем, существует ли локальный репозиторий
if [ ! -d "$LOCAL_REPO_DIR" ]; then
    echo "Локальный репозиторий не найден. Клонируем репозиторий GitLab..."
    git clone --branch $GITLAB_BRANCH $GITLAB_REPO_URL $LOCAL_REPO_DIR
else
    echo "Локальный репозиторий найден. Обновляем его с GitLab..."
    cd $LOCAL_REPO_DIR
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "$GITLAB_BRANCH" ]; then
        echo "Переключаемся на ветку $GITLAB_BRANCH..."
        git checkout $GITLAB_BRANCH || { echo "Ошибка: Не удалось переключиться на ветку $GITLAB_BRANCH"; exit 1; }
    fi
    git pull origin $GITLAB_BRANCH || { echo "Ошибка: Не удалось выполнить git pull с удалённого $GITLAB_REPO_URL"; exit 1; }
fi

# Переходим в локальный репозиторий
cd $LOCAL_REPO_DIR

# Добавляем GitHub как удалённый репозиторий, если он ещё не добавлен
if git remote get-url github &> /dev/null; then
    echo "GitHub уже добавлен как удалённый. Обновляем URL..."
    git remote set-url github $GITHUB_REPO_URL
else
    echo "Добавляем GitHub как удалённый репозиторий..."
    git remote add github $GITHUB_REPO_URL
fi

# Проверяем, существует ли ветка GITLAB_BRANCH локально
if ! git show-ref --verify --quiet refs/heads/$GITLAB_BRANCH; then
    echo "Ошибка: Ветка $GITLAB_BRANCH отсутствует в локальном репозитории."
    exit 1
fi

# Пушим изменения в GitLab
echo "Пушим изменения в Github..."
git push -u github $GITLAB_BRANCH:$GITHUB_BRANCH --force


# Завершение
echo "Синхронизация завершена!"