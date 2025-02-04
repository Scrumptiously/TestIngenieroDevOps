pipeline {

    agent any

    stages {

        stage('Preparar Ambiente') { // Construcción de ambiente de pruebas
            steps {
                sh 'docker pull public.ecr.aws/portswigger/dastardly:latest'
                withCredentials([file(credentialsId: 'Environment', variable: 'Environment')]) {
                    sh 'cp $Environment ${WORKSPACE}/main'
                }
                sh 'docker compose up --build -d'
            }
        }

        stage('Análisis SAST') { // Analisis SAST con SonarQube
            steps {
                script {
                    scannerHome = tool 'SonarCloud'
                }
                withSonarQubeEnv('SonarCloud') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: false //Cambiar a true para detener pipeline
                }
            }
        }

        stage('Análisis SCA') { //Analisis SCA con OWASP Dependency Check
            steps {
                dependencyCheck additionalArguments: '', nvdCredentialsId: 'NVD', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }

        stage('Pruebas unitarias') { // Pruebas Unitarias
            steps {
                sh 'docker compose exec django_app python3 manage.py makemigrations MainApp --no-input'
                sh 'docker compose exec django_app python3 manage.py migrate --no-input'
                sh 'docker compose exec django_app python3 manage.py test'
            }
        }

        stage('Análisis DAST') { // Analisis DAST con Dastardly
            steps {
                sh '''
                    docker run --user $(id -u) --network=host -v ${WORKSPACE}:${WORKSPACE}:rw \
                    -e BURP_START_URL=http://localhost:8000/ \
                    -e BURP_REPORT_FILE_PATH=${WORKSPACE}/dastardly-report.xml \
                    public.ecr.aws/portswigger/dastardly:latest
                '''

            }
        }
        
        stage('Despliegue') { // Despliegue en EC2 Producción
            steps {
                sshagent(credentials: ['SSHEC2PROD']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${PROD_HOST}'
                            docker stop django_app || true &&
                            docker rm django_app || true &&
                            docker rmi django_app || true &&
                            rm -rf /home/ubuntu/TestIngenieroDevOps || true &&
                            git clone git@github.com:Scrumptiously/TestIngenieroDevOps.git &&
                            cd /home/ubuntu/TestIngenieroDevOps &&
                            docker compose up --build -d
                            docker compose exec django_gunicorn python3 manage.py makemigrations MainApp --no-input
                            docker compose exec django_gunicorn python3 manage.py migrate --no-input
                            docker compose exec django_gunicorn python3 manage.py collectstatic --no-input
                        '
                    '''
                }
            }
        }
    }

    post {
 
        always { // Limpieza del entorno de pruebas
            cleanWs()
            sh 'docker stop django_app || true'
            sh 'docker rm django_app || true'
            sh 'docker rmi django_app || true'
        }

        failure { // Correo electronico notificando error
            echo "Piepeline ${env.JOB_NAME} detenida"
            mail bcc: '', 
                body: "La pipeline ${env.JOB_NAME} ha finalizado con estado ${currentBuild.result}. Por favor revisar la consola para mas detalles.", 
                cc: '', 
                from: 'Jenkins <devops@fakedomain.cl>', 
                replyTo: '', 
                subject: "Piepeline ${env.JOB_NAME} detenida", 
                to: 'engineer@fakedomain.cl'
        }

        success { // Correo electronico notificando ejecución exitosa
            echo "Piepeline ${env.JOB_NAME} ejecutada con exito"
            mail bcc: '', 
                body: "La pipeline ${env.JOB_NAME} ha finalizado con estado ${currentBuild.result}.", 
                cc: '', 
                from: 'Jenkins <devops@fakedomain.cl>', 
                replyTo: '', 
                subject: "Piepeline ${env.JOB_NAME} ejecutada con exito", 
                to: 'engineer@fakedomain.cl'
        }
    }
}