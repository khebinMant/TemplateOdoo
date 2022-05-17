pipeline {
    agent any
    environment {
        PROJEC_NAME = "template_sa"
        TAGS = 'sistemaagil'
        ODOO_IMAGE_VERSION = "1.0.7"
    }
    stages {
        stage('Unit Test') {
            agent {
                docker {
                    label 'principal'
                    image 'registry.sistemaagil.net:5000/sonar-client-4.5-py3:1.0.2'
                    args '--network=postgres_net'
                    registryUrl 'http://172.40.0.50:5000'
                    registryCredentialsId 'admin-registry-pass'
                }
            }
            steps {
                sh 'python3 -m xmlrunner unit-tests/test_*.py -o ./junit-reports'
                sh 'coverage run --source=./logic -m unittest unit-tests/test_*.py'
                sh 'coverage xml'
                sh '/root/sonar-scanner-4.5.0.2216-linux/bin/sonar-scanner'
            }
        }
        stage("Resultado SonarQube") {
            agent {
                label 'principal'
            }
            environment {
                SONAR_CREDENTIALS = credentials('sonar-admin')
            }
            steps {
                script {

                    estatus = sh(
                        script: 'curl -u $SONAR_CREDENTIALS_USR:$SONAR_CREDENTIALS_PSW -s http://172.40.0.10:9000/api/qualitygates/project_status?projectKey=${PROJEC_NAME} | jq .projectStatus.status',
                        returnStdout: true
                    ).trim().toUpperCase().replaceAll("[\n\r]", "")

                    if (estatus == '"ERROR"'){
                        throw new Exception("No supera los estandares de calidad..")
                    }

                    if (estatus.isEmpty()){
                        throw new Exception("Not OK")
                    }
                }
            }
        }
        stage ("Odoo Test"){
            agent {
                label 'centurion'
            }
            environment {
                MODULE_PATH = "/mnt/extra-addons/${PROJEC_NAME}"
                CONTAINER = "$PROJEC_NAME"+".sistemaagil.net"
                PGPASSWORD = credentials('centurion-postgres-odoo')
                
            }
            steps{
                sh 'docker create -v odoo-testing-var:/var/lib/odoo -v odoo-testing-etc:/etc/odoo -v odoo-testing-addons:/mnt/extra-addons --name=$CONTAINER --network=postgres_net --ip 172.40.0.80 -it odoo14-sa:${ODOO_IMAGE_VERSION}'
                sh 'docker start $CONTAINER'
                sh 'docker exec -u root $CONTAINER rm -rf $MODULE_PATH'
                sh 'docker exec -u root $CONTAINER mkdir -p $MODULE_PATH'
                sh 'docker cp . $CONTAINER:$MODULE_PATH'
                sh 'docker exec -u root $CONTAINER chown -R root:root $MODULE_PATH'
                sh 'docker exec $CONTAINER nohup odoo --db_host pgMaster13 --db_port 5432 -r $PGPASSWORD_USR -w $PGPASSWORD_PSW --addons-path /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons --test-enable --test-tags $TAGS --update $PROJEC_NAME --database testing --logfile odootesting.log &'
                sleep 30
                sh 'docker cp $CONTAINER:/odootesting.log .'
                script {
                    def fileContents = readFile(file: 'odootesting.log')
                    def pattern = ~/(?im).*Error.*/
                    def matcher = fileContents =~ pattern
                    if (matcher.find()){
                            throw new Exception(matcher[0..-1].toString())
                    }
                }
                sh 'cat odootesting.log'
            }
            post {
                always {
                    sh 'docker stop $CONTAINER'
                    sh 'docker rm $CONTAINER'
                }
            }     
        }
        
        stage ('Dependency-Check Vulnerabilities') {
            agent {
                label 'centurion'
            }
            environment {
                MODULE_PATH = "/mnt/extra-addons/${PROJEC_NAME}"
                CONTAINER = "$PROJEC_NAME"+".sistemaagil.net"         
            }
            steps {

                sh 'docker create -v odoo-testing-var:/var/lib/odoo -v odoo-testing-etc:/etc/odoo -v odoo-addons:/mnt/extra-addons --name=$CONTAINER --network=postgres_net --ip 172.40.0.80 -it odoo14-sa:${ODOO_IMAGE_VERSION}'
                sh 'docker start $CONTAINER'
                sh 'docker exec -u root $CONTAINER rm -rf $MODULE_PATH'
                sh 'docker exec -u root $CONTAINER mkdir -p $MODULE_PATH'
                sh 'docker cp . $CONTAINER:$MODULE_PATH'
                sh 'docker exec -u root $CONTAINER pip3 install -r $MODULE_PATH/requirements.txt'
                sh 'docker exec -u root $CONTAINER bash -c "pip3 freeze | safety check --bare"'
            }
            post {
                always {
                    sh 'docker stop $CONTAINER'
                    sh 'docker rm $CONTAINER'
                }
            } 
        }

        stage("Inicio Despligue en Integración"){
            agent {
                label 'centurion'
            }
            environment {
                MODULE_PATH = "/mnt/extra-addons/${PROJEC_NAME}"
                CONTAINER = sh(
                    returnStdout: true, 
                    script: 'docker ps --filter "name=int" --format "{{.ID}}"'
                ).trim()
                      
            }
            steps{
                sh 'docker restart $CONTAINER'
                sh 'docker exec -u root $CONTAINER rm -rf $MODULE_PATH'
                sh 'docker exec -u root $CONTAINER mkdir -p $MODULE_PATH'
                sh 'docker cp . $CONTAINER:$MODULE_PATH'
                sh 'docker exec -u root $CONTAINER chown -R root:root $MODULE_PATH'
                sh 'docker exec -u root $CONTAINER ls -ltha $MODULE_PATH'
            }    
        }
        stage ("Actualiza DB") {
            agent {
                docker {
                    image 'postgres:13'
                    label 'principal'
                    args '--network=postgres_net'
                }
            }
            environment {
                PG_HOST = 'pgMaster13'
                PG_PORT = '5432'
                PG_DB = 'integracion'
                PGCREDENTIAL = credentials('centurion-postgres-odoo')
            }
            steps {
                sh 'PGPASSWORD=$PGCREDENTIAL_PSW psql -h $PG_HOST -p $PG_PORT -U $PGCREDENTIAL_USR -d $PG_DB -c "update ir_module_module set state = \'to upgrade\' where name = \'$PROJEC_NAME\'"'
            }
        }
        stage ("Reiniciar Odoo"){
            agent {
                label 'centurion'
            }
            environment {
                CONTAINER = sh(
                    returnStdout: true, 
                    script: 'docker ps --filter "name=int" --format "{{.ID}}"'
                ).trim()
            }
            steps {
                sh 'docker restart $CONTAINER'
                sh 'docker exec $CONTAINER nohup odoo &'
            }
        }
    }
}
