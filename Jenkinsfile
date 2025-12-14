def dockerImage

pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = "segundavid/studybuddy-repo"
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
        IMAGE_TAG = "v${BUILD_NUMBER}"
        IMAGE_LABEL = "${DOCKER_HUB_REPO}:${IMAGE_TAG}"
        GKE_CLUSTER = "study-buddy"
        GKE_REGION = "us-central1"
        GKE_PROJECT_ID = "mineral-brand-478714-v4"
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
        stage("Deploy Application on GKE") {
            steps {
                script {
                    echo "Deploying app on GKE..."
                    withCredentials([file(credentialsId: "gke-file", variable: "GKE_CREDENTIAL")]) {
                        sh """
                        gcloud auth activate-service-account --key-file=$GKE_CREDENTIAL
                        gcloud container clusters get-credentials ${GKE_CLUSTER} --region ${GKE_REGION} --project ${GKE_PROJECT_ID}

                        kubectl apply -f ci_cd/deployment.yaml --validate=false
                        kubectl apply -f ci_cd/service.yaml --validate=false

                        kubectl rollout restart deployment study-app
                        """
                    }
                    echo "App deployed successfully"
                }
            }
        }
    }
}