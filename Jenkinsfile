pipeline {
    agent any

    tools {
        maven 'Maven'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run UI Automation Tests') {
            steps {
                dir('automation-tests') {
                    bat 'mvn clean test || exit 0'
                }
            }
        }

        stage('AI Failure Analysis') {
            steps {
                script {
                    def aiResult = bat(
                        script: '''
                        powershell -Command "
                        $log = Get-Content automation-tests/target/surefire-reports/TEST-TestSuite.xml -Raw;
                        $response = Invoke-RestMethod `
                          -Uri http://localhost:8001/analyze `
                          -Method POST `
                          -Body (@{log=$log} | ConvertTo-Json) `
                          -ContentType application/json;
                        Write-Output $response.analysis
                        "
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "AI Classification: ${aiResult}"

                    if (aiResult == "ENVIRONMENT_ISSUE") {
                        error("Pipeline blocked: Environment issue detected")
                    } else if (aiResult == "APPLICATION_BUG") {
                        error("Pipeline blocked: Application bug detected")
                    } else {
                        echo "Test failure only – marking build as UNSTABLE"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'automation-tests/target/surefire-reports/**/*'
        }
    }
}
