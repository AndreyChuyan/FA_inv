
# Gitlub settings
## vscode
```bash
.ssh/config
#>
Host gitlab
  HostName 192.168.2.41
  User vagrant
  IdentityFile ~/.ssh/id_rsa.pub
#<>
#--- настройка ключей
# На Windows powershell
scp $env:USERPROFILE\.ssh\id_rsa.pub vagrant@192.168.2.41:~/temp_key.pub
ssh vagrant@192.168.2.41 'mkdir -p ~/.ssh; \
cat ~/temp_key.pub >> ~/.ssh/authorized_keys; \ 
rm ~/temp_key.pub; chmod 600 ~/.ssh/authorized_keys'
#пароль
sudo cat /etc/gitlab/initial_root_password
#powerShell
ssh -L 81:localhost:80 vagrant@192.168.2.41
http://localhost:81
root / cfW8TSHrP16OT6j5YmPiLf+BhXlxU5XDMsYsKot9zRA=
```

```bash
nano ~/.netrc
#>
machine gitlab.ch.loc
login Administrator
password glft-bWfjdyiyyyeXgEhoV1wX
#<>
chmod 600 ~/.netrc
```


## Загрузка образа докер в гитлаб
```bash
registry.gitlab.ch.loc/admin/fa-inv:latest
```
Чтобы создать PAT: → GitLab → **Settings > Access Tokens**.
glpat-Bt9DwvynvxJStxzA3GSE
## Шаг 2. Авторизация для работы с GitLab Registry
```bash
ssh vagrant@192.168.2.41
sudo nano /etc/gitlab/gitlab.rb
#>
registry_external_url 'http://gitlab.ch.loc:5050'
#<>
sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart
sudo netstat -tuln | grep 5050
# на удаленной машине
nano /etc/hosts
#>
192.168.2.41    gitlab.ch.loc
#<>
sudo nano /etc/docker/daemon.json
#>
{
      "insecure-registries": ["gitlab.ch.loc:5050"]
}
#<>
sudo systemctl restart docker

#авторизация
docker login gitlab.ch.loc:5050
# Username
# root
# Password
# glpat-Bt9DwvynvxJStxzA3GSE

# Сборка на удаленный репозиторий
docker build -t gitlab.ch.loc:5050/root/fa-inv:latest .
# загрузка образа в Gitlab
docker push gitlab.ch.loc:5050/root/fa-inv:latest
# Administrator - fa-inv - Container Registry
```



# Ranners
## ssh in docker
```bash
docker run -d -m 1g --name shell-gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:latest

# docker run --rm -t -i gitlab/shell-gitlab-runner --help
docker exec -it shell-gitlab-runner \
  gitlab-runner register  --url http://192.168.2.41  --token glrt-t1_Pw38bBBxpx7vcy8qczpf

#ssh-docker
#shell
docker exec -it shell-gitlab-runner \
  echo "192.168.2.41 gitlab.ch.loc" >> /etc/hosts
docker exec -it shell-gitlab-runner \
  gitlab-runner restart
docker exec -it shell-gitlab-runner \
  cat /home/gitlab-runner/build.txt

docker exec -it shell-gitlab-runner /bin/bash
```

## docker in docker
```bash
docker volume create did-gitlab-runner-config
docker run -d -m 1g --name did-gitlab-runner --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v did-gitlab-runner-config:/etc/gitlab-runner \
  gitlab/gitlab-runner:latest
docker exec -it did-gitlab-runner \
  gitlab-runner register --url http://192.168.2.41 \
  --registration-token oT97tRKApzBG1RRj3vzm
#did-docker
#docker
#docker:dind
docker exec -it did-gitlab-runner /bin/bash
  echo "192.168.2.41 gitlab.ch.loc" >> /etc/hosts
docker exec -it did-gitlab-runner \
  gitlab-runner restart
sudo nano /var/lib/docker/volumes/did-gitlab-runner-config/_data/config.toml
  # [runners.docker]
  #>volumes = ["/cache"]
  volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
  extra_hosts = ["gitlab.ch.loc:192.168.2.41"]
  #<>
docker restart did-gitlab-runner
```

# Code
```bash
ssh -T git@gitlab.ch.loc
/home/ladmin/gitlab/deus/.gitlab-ci.yml
#>
stages:
  - build
  - test
  - deploy

Docker build:
  stage: build
  script:
    - echo 'docker build is successful'
  tags:
    - docker

Unit tests:
  stage: test
  script:
    - echo 'this is unit test!'
  tags:
    - docker

Linters:
  stage: test
  script:
    - echo 'this is linter test!'
  tags:
    - docker

Deploy to Dev:
  stage: deploy
  script:
    - echo "${CI_PROJECT_NAME} from branch ${CI_COMMIT_REF_SLUG} [#${CI_COMMIT_SHORT_SHA}]" >> ~/build.txt
  tags:
    - docker
#<>

docker exec -it gitlab-runner /bin/bash -c "cat /home/gitlab-runner/build.txt"
```

# Git-import
https://docs.gitlab.com/ee/ci/ci_cd_for_external_repos/github_integration.html
```bash











```