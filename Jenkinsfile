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

                $log = Get-Content $xmlFile.FullName -Raw

                $body = @{ log = $log } | ConvertTo-Json -Depth 5

                $response = Invoke-RestMethod `
                    -Uri "http://127.0.0.1:8001/analyze" `
                    -Method POST `
                    -Body $body `
                    -ContentType "application/json"

                Write-Output $response.analysis.status
                ''',
                returnStdout: true
            ).trim()

            echo "AI Quality Gate Status: ${aiStatus}"

            if (aiStatus == "FAILURE") {
                error("Quality gate blocked the pipeline (AI status = FAILURE)")
            } else if (aiStatus == "UNSTABLE") {
                currentBuild.result = "UNSTABLE"
                echo "Marked build UNSTABLE (AI status = UNSTABLE)"
            } else {
                echo "Build PASSED (AI status = SUCCESS or NO_REPORT)"
            }
        }
    }
}
