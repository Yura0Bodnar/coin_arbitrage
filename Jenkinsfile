pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {

        stage('Checkout Code') {
            steps {
                script {
                    echo "Fetching latest code from GitHub..."
                    sh 'git reset --hard'
                    sh 'git pull origin dev_yura'
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    echo "Stopping and removing old containers..."
                    sh 'docker-compose down -v || true'

                    echo "Building and running new containers..."
                    sh 'docker-compose up -d --build --force-recreate'
                }
            }
        }

        stage('Static Analysis') {
            parallel {
                stage('Check Code') {
                    steps {
                        script {
                            def containers = ['coin_arbitrage-main', 'coin_arbitrage-bybit', 'coin_arbitrage-whitebit']
                            for (c in containers) {
                                echo "Running lint check in ${c}"
                                sh "docker exec ${c} poetry run black --check ."
                                sh "docker exec ${c} poetry run flake8 ."
                            }
                        }
                    }
                }

                stage('Security Check') {
                    steps {
                        script {
                            def containers = ['coin_arbitrage-main', 'coin_arbitrage-bybit', 'coin_arbitrage-whitebit']
                            for (c in containers) {
                                echo "Running security check in ${c}"
                                sh "docker exec ${c} poetry run bandit -r ."
                            }
                        }
                    }
                }
            }
        }
        stage('Merge to dev') {
            environment {
                GITHUB_TOKEN = credentials('github-token')
            }
            steps {
                script {
                    echo "Merging dev_yura into dev"
                    sh '''
                        git fetch origin
                        git checkout dev
                        git merge origin/dev_yura --no-edit
                        git push https://${GITHUB_TOKEN}@github.com/Yura0Bodnar/https://github.com/Yura0Bodnar/coin_arbitrage.git dev
                    '''
                }
            }
        }

        /*
        stage('Test') {
            steps {
                script {
                    def containers = ['coin_arbitrage-main', 'coin_arbitrage-bybit', 'coin_arbitrage-whitebit']
                    for (c in containers) {
                        echo "Running tests in ${c}"
                        sh "docker exec ${c} poetry run pytest tests/ --disable-warnings"
                    }
                }
            }
        } */
    }
}