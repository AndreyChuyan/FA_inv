#!/bin/bash

# Скрипт синхронизирует код между GitHub и GitLab

# Настройки
REPO_NAME="${REPO_NAME:-FA_inv}"
GITHUB_REPO_URL="${GITHUB_REPO_URL:-git@github.com:AndreyChuyan/$REPO_NAME.git}"
GITLAB_REPO_URL="${GITLAB_REPO_URL:-git@gitlab.ch.loc:root/$REPO_NAME.git}"
LOCAL_REPO_DIR="/tmp/git/$REPO_NAME"

# Функция для синхронизации из GitHub в GitLab
sync_github_to_gitlab() {
    GITHUB_BRANCH="main"
    GITLAB_BRANCH="import"
    echo "Синхронизируем из GitHub ($GITHUB_BRANCH) в GitLab ($GITLAB_BRANCH)..."
    
    # Проверяем, существует ли локальный репозиторий
    if [ ! -d "$LOCAL_REPO_DIR" ]; then
        echo "Локальный репозиторий не найден. Клонируем репозиторий GitHub..."
        git clone --branch "$GITHUB_BRANCH" "$GITHUB_REPO_URL" "$LOCAL_REPO_DIR"
    else
        echo "Локальный репозиторий найден. Обновляем его с GitHub..."
        cd "$LOCAL_REPO_DIR" || exit
        current_branch=$(git branch --show-current)
        if [ "$current_branch" != "$GITHUB_BRANCH" ]; then
            git checkout "$GITHUB_BRANCH"
        fi
        git pull origin "$GITHUB_BRANCH"
    fi

    # Переходим в локальный репозиторий
    cd "$LOCAL_REPO_DIR" || exit

    # Добавляем GitLab как удалённый репозиторий, если он ещё не добавлен
    if git remote get-url gitlab &> /dev/null; then
        git remote set-url gitlab "$GITLAB_REPO_URL"
    else
        git remote add gitlab "$GITLAB_REPO_URL"
    fi

    # Пушим изменения в GitLab
    echo "Пушим изменения в GitLab..."
    git push -u gitlab "$GITHUB_BRANCH":"$GITLAB_BRANCH" --force

    echo "Синхронизация из GitHub в GitLab завершена!"
}

# Функция для синхронизации из GitLab в GitHub
sync_gitlab_to_github() {
    GITHUB_BRANCH="import"
    GITLAB_BRANCH="main"
    echo "Синхронизируем из GitLab ($GITLAB_BRANCH) в GitHub ($GITHUB_BRANCH)..."
    
    # Проверяем, существует ли локальный репозиторий
    if [ ! -d "$LOCAL_REPO_DIR" ]; then
        echo "Локальный репозиторий не найден. Клонируем репозиторий GitLab..."
        git clone --branch "$GITLAB_BRANCH" "$GITLAB_REPO_URL" "$LOCAL_REPO_DIR"
    else
        echo "Локальный репозиторий найден. Обновляем его с GitLab..."
        cd "$LOCAL_REPO_DIR" || exit
        current_branch=$(git branch --show-current)
        if [ "$current_branch" != "$GITLAB_BRANCH" ]; then
            git checkout "$GITLAB_BRANCH"
        fi
        git pull origin "$GITLAB_BRANCH"
    fi

    # Переходим в локальный репозиторий
    cd "$LOCAL_REPO_DIR" || exit

    # Добавляем GitHub как удалённый репозиторий, если он ещё не добавлен
    if git remote get-url github &> /dev/null; then
        git remote set-url github "$GITHUB_REPO_URL"
    else
        git remote add github "$GITHUB_REPO_URL"
    fi

    # Пушим изменения в GitHub
    echo "Пушим изменения в GitHub..."
    git push -u github "$GITLAB_BRANCH":"$GITHUB_BRANCH" --force

    echo "Синхронизация из GitLab в GitHub завершена!"
}

# Помощь
usage() {
    echo "Использование: $0 [option]"
    echo "Опции:"
    echo "  to-gitlab     Синхронизировать из GitHub в GitLab"
    echo "  to-github     Синхронизировать из GitLab в GitHub"
    echo "  help          Показать это сообщение помощи"
}

# Главная часть скрипта
case "$1" in
    to-gitlab)
        sync_github_to_gitlab
        ;;
    to-github)
        sync_gitlab_to_github
        ;;
    help|--help|-h|"")
        usage
        ;;
    *)
        echo "Неизвестная опция: $1"
        usage
        exit 1
        ;;
esac