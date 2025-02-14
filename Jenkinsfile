pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/Yura0Bodnar/coin_arbitrage.git', branch: 'dev_yura'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
            }
        }
    }
}
