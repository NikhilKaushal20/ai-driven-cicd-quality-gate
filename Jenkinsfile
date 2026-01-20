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
                    // Don't fail immediately — we want AI analysis to still run
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
                    def aiStatus = bat(
                        script: '''
                        powershell -Command "
                        $xmlFile = Get-ChildItem automation-tests/target/surefire-reports/*.xml | Select-Object -First 1;

                        if ($null -eq $xmlFile) {
                            Write-Output 'NO_REPORT'
                            exit 0
                        }

                        $log = Get-Content $xmlFile.FullName -Raw;

                        $response = Invoke-RestMethod `
                          -Uri http://127.0.0.1:8001/analyze `
                          -Method POST `
                          -Body (@{log=$log} | ConvertTo-Json -Depth 5) `
                          -ContentType application/json;

                        Write-Output $response.analysis.status
                        "
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "AI Quality Gate Status: ${aiStatus}"

                    // ✅ Quality Gate Decision
                    if (aiStatus == "FAILURE") {
                        error("Quality gate blocked the pipeline (AI status = FAILURE)")
                    } else if (aiStatus == "UNSTABLE") {
                        currentBuild.result = 'UNSTABLE'
                        echo "Marked build UNSTABLE (AI status = UNSTABLE)"
                    } else {
                        echo "Build PASSED (AI status = SUCCESS or NO_REPORT)"
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
