def dockerImage

pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = "segundavid/studybuddy-repo"
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
        IMAGE_TAG = "v${BUILD_NUMBER}"
        IMAGE_LABEL = "${DOCKER_HUB_REPO}:${IMAGE_TAG}"
    }
    stages {
        stage("Build Docker Image") {
            steps {
                script {
                    echo "${IMAGE_LABEL} build starting..."
                    dockerImage = docker.build("${IMAGE_LABEL}")
                    echo "Done building ${IMAGE_LABEL}"
                }
            }
        }
        stage("Push Image to DockerHub") {
            steps {
                script {
                    echo "Pushing ${IMAGE_LABEL} to Docker Hub..."
                    docker.withRegistry("https://registry.hub.docker.com", "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push("${IMAGE_TAG}")
                    }
                    echo "Successfully pushed ${IMAGE_LABEL} to Docker Hub"
                }
            }
        }
        stage("Update Deployment YAML with New Tag") {
            steps {
                script {
                    echo "Updating tag for docker image in deployment.yaml..."
                    sh "sed -i 's|image: ${DOCKER_HUB_REPO}:.*|image: ${IMAGE_LABEL}|' ci_cd/deployment.yaml"
                    echo "Successfully updated docker tag in deployment.yaml"
                }
            }
        }
        stage("Commit Updated YAML") {
            steps {
                script {
                    echo "Pushing changes to GitHub..."
                    withCredentials([usernamePassword(credentialsId: "github-token", usernameVariable: "GIT_USER", passwordVariable: "GIT_PASS")]) {
                        sh """
                        git config user.name '${GIT_USER}'
                        git config user.email 'segun.d.ogundipe@gmail.com'
                        git add ci_cd/deployment.yaml
                        git commit -m 'Update image tag to ${IMAGE_TAG}' || echo 'No changes to commit'
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/${GIT_USER}/study-buddy.git HEAD:main
                        """
                    }
                    echo "Successfully pushed changes to GitHub..."
                }
            }
        }
        stage("Apply Kubernetes & Sync App with ArgoCD") {
            steps {
                script {
                    echo "Syncing app using ArgoCD..."
                    kubeconfig(credentialsId: "kubeconfig", serverUrl: "https://192.168.49.2:8443") {
                        sh '''
                        argocd login 35.224.91.174:9090 --username admin --password $(kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --insecure
                        argocd app sync study-buddy
                        '''
                    }
                    echo "Successfully synced app using ArgoCD"
                }
            }
        }
    }
}