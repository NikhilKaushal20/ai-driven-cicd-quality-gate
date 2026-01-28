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
                    def aiStatus = powershell(
                        script: '''
                        $xml = Get-ChildItem "automation-tests/target/surefire-reports/*.xml" | Select-Object -First 1
                        if ($null -eq $xml) { "NO_REPORT"; exit 0 }

                        $log = [string](Get-Content $xml.FullName -Raw)
                        $json = @{ log = $log } | ConvertTo-Json -Compress

                        $res = Invoke-RestMethod `
                          -Uri "http://127.0.0.1:8001/analyze" `
                          -Method POST `
                          -Body $json `
                          -ContentType "application/json"

                        $res.analysis.status
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "AI Status: ${aiStatus}"

                    if (aiStatus == "FAILURE") {
                        error("Pipeline blocked by AI quality gate")
                    } else if (aiStatus == "UNSTABLE") {
                        currentBuild.result = "UNSTABLE"
                    }
                }
            }
        }
    }
}
