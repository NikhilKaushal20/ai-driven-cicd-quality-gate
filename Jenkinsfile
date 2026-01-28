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

        stage('Verify Test Reports') {
            steps {
                bat '''
                echo "Listing surefire reports:"
                dir automation-tests\\target\\surefire-reports
                '''
            }
        }

        stage('AI Failure Analysis') {
            steps {
                script {
                    def aiStatus = powershell(
                        script: '''
                        $xmlFile = Get-ChildItem "automation-tests/target/surefire-reports/*.xml" | Select-Object -First 1

                        if ($null -eq $xmlFile) {
                            Write-Output "NO_REPORT"
                            exit 0
                        }

                        # Force XML content to pure string
                        $log = [string](Get-Content $xmlFile.FullName -Raw)

                        # Escape quotes to build valid JSON
                        $escapedLog = $log -replace '"', '\\"'

                        # Manually build JSON payload
                        $json = "{""log"":""$escapedLog""}"

                        $response = Invoke-RestMethod `
                            -Uri "http://127.0.0.1:8001/analyze" `
                            -Method POST `
                            -Body $json `
                            -ContentType "application/json"

                        Write-Output $response.analysis.status
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "AI Quality Gate Status: ${aiStatus}"

                    if (aiStatus == "FAILURE") {
                        error("Quality gate blocked the pipeline")
                    } else if (aiStatus == "UNSTABLE") {
                        currentBuild.result = "UNSTABLE"
                        echo "Build marked UNSTABLE"
                    } else {
                        echo "Build PASSED"
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
