pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        PROJECT_PATH = "$WORKSPACE"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    try {
                        echo "### Checking if main.py exists ###"
                        sh '[ -f coin_arbitrage/main.py ] && echo "main.py exists" || echo "main.py is MISSING!"'

                        echo "### Running docker-compose ###"
                        sh 'docker-compose up -d --build --force-recreate'
                        sleep(time: 30, unit: "SECONDS")
                    } catch (Exception e) {
                        error "Docker Compose failed!"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

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

        /*
        stage('Security Check') {
            steps {
                script {
                    def containers = ['coin_arbitrage-main', 'coin_arbitrage-bybit', 'coin_arbitrage-whitebit']
                    for (c in containers) {
                        echo "Running security check in ${c}"
                        // Bandit - аналіз безпеки Python-коду
                        sh "docker exec ${c} poetry run bandit -r ."

                        // Safety - перевірка залежностей Python на вразливості
                        sh "docker exec ${c} poetry run safety check"
                    }
                }
            }
        }
        */
        /*
        stage('Merge to dev') {
            steps {
                script {
                    echo "Merging dev_yura into dev"
                    sh '''
                        git config --global user.email "yuriy575721@gmail.com"
                        git config --global user.name "Yura0Bodnar"
                        git checkout dev
                        git merge origin/dev_yura --no-edit
                        git push origin dev
                    '''
                }
            }
        }
        */
    }
}