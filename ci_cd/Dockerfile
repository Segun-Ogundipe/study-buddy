FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y \
    && apt-get install -y ca-certificates gnupg curl \
    && curl -fsSL https://get.docker.com -o get-docker.sh \
    && sh ./get-docker.sh \
    && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/kubectl \
    && curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64 \
    && chmod +x /usr/local/bin/argocd \
    && apt-get clean

# Switch back to the Jenkins user
USER jenkins
