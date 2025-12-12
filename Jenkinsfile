pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = "segundavid/studybuddy-repo"
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
    stages {
        stage("Build Docker Image") {
            steps {
                script {
                    echo "Building Docker image..."
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${IMAGE_TAG}")
                }
            }
        }
        stage("Push Image to DockerHub") {
            steps {
                script {
                    echo "Pushing Docker image to DockerHub..."
                    docker.withRegistry("https://registry.hub.docker.com", "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push("${IMAGE_TAG}")
                    }
                }
            }
        }
        stage("Update Deployment YAML with New Tag") {
            steps {
                script {
                    sh """
                    echo 'Updating tag for docker image in deployment.yaml'
                    sed -i 's|image: ${DOCKER_HUB_REPO}:.*|image: ${DOCKER_HUB_REPO}:${IMAGE_TAG}|' ci_cd/deployment.yaml
                    """
                }
            }
        }
        stage("Commit Updated YAML") {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "github-token", usernameVariable: "GIT_USER", passwordVariable: "GIT_PASS")]) {
                        sh """
                        echo 'Pushing changes to GitHub'
                        git config user.name '${GIT_USER}'
                        git config user.email 'segun.d.ogundipe@gmail.com'
                        git add ci_cd/deployment.yaml
                        git commit -m 'Update image tag to ${IMAGE_TAG}' || echo 'No changes to commit'
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/${GIT_USER}/study-buddy.git HEAD:main
                        """
                    }
                }
            }
        }
        // stage("Install Kubectl & ArgoCD CLI Setup") {
        //     steps {
        //         sh '''
        //         echo 'Installing Kubectl & ArgoCD cli...'
        //         curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        //         chmod +x kubectl
        //         mv kubectl /usr/local/bin/kubectl
        //         curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
        //         chmod +x /usr/local/bin/argocd
        //         '''
        //     }
        // }
        stage("apply Kubernetes & Sync App with ArgoCD") {
            steps {
                script {
                    kubeconfig(credentialsId: "kubeconfig", serverUrl: "https://192.168.49.2:8443") {
                        sh '''
                        argocd login 34.61.213.84:31704 --username admin --password $(kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --insecure
                        argocd app sync study-buddy
                        '''
                    }
                }
            }
        }
    }
}