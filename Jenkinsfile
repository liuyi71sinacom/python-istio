pipeline {

  agent {
   label 'maven'
  }
    
   parameters { 
        string(name: 'TAG_NAME',defaultValue: '1.5',description: '')
     }

    environment {
        DOCKER_CREDENTIAL_ID = 'aliyun-id'
        GITEE_CREDENTIAL_ID = 'gitee-id'
        KUBECONFIG_CREDENTIAL_ID = 'demo-kubeconfig'
        REGISTRY = 'registry.cn-hangzhou.aliyuncs.com'
        DOCKERHUB_NAMESPACE = 'liuyik8s'
        GITEE_ACCOUNT = 'liuyik8s'
        BRANCH_NAME = 'master'
        APP_NAME = 'python-istio'
        }

    stages {
        stage ('checkout scm') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'gitee-id', url: 'https://gitee.com/liuyik8s/python-istio.git']]])
  
            }
        }
 
        stage('checking'){
            steps {
                sh '''
                pwd
                echo "webhook"
                echo "webhook"
                ls -l
                sleep 2
                echo "$[app]"
                '''
            }    
      }

        stage('Unit Testing'){
          steps {
            echo "Unit Testing..."
          }
    }
    
     
        stage ('build & push') {
            steps {
                container ('maven') {
                    sh 'cat app-demo.py'
                    sh 'sleep 1'
                    sh 'env'
                    sh 'docker build  -t $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:SNAPSHOT-$BRANCH_NAME-$TAG_NAME .'
                    withCredentials([usernamePassword(passwordVariable : 'DOCKER_PASSWORD' ,usernameVariable : 'DOCKER_USERNAME' ,credentialsId : "$DOCKER_CREDENTIAL_ID" ,)]) {
                        sh 'echo "$DOCKER_PASSWORD" | docker login $REGISTRY -u "$DOCKER_USERNAME" --password-stdin'
                        sh 'docker push  $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:SNAPSHOT-$BRANCH_NAME-$TAG_NAME'
                    }
                }
            }
        }
    
        stage('push latest'){
           when{
             branch 'master'
           }
           steps{
                container ('maven') {
                  sh 'docker tag  $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:SNAPSHOT-$BRANCH_NAME-$TAG_NAME $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:latest '
                  sh 'docker push  $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:latest '
                }
           }
       }
      
       stage('deploy to dev') {
          when{
            branch 'master'
          }
          steps {
             container ('maven'){
       //     input(id: 'deploy-to-dev', message: 'deploy to dev?')
              sh "cat deploy.yaml"
              sh "sleep 1"
              sh "ls -l "
              sh "sleep 1"
             
             sh '''
             echo "changing parameter"
            
             '''
           
             sh "sleep 10"
             sh "cat deploy.yaml"
             sh 'kubectl apply -f deploy.yaml -n testing'
           }
          }
        }

        stage('push with tag'){
          
            steps {
              container ('maven') {
         //       input(id: 'release-image-with-tag', message: 'release image with tag?')
                  withCredentials([usernamePassword(credentialsId: "$GITEE_CREDENTIAL_ID", passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh 'git config --global user.email "liuyi71@sina.com" '
                    sh 'git config --global user.name "liuyi71k8s" '
                    sh 'git tag -a $TAG_NAME -m "$TAG_NAME" '
                    sh 'git push http://$GIT_USERNAME:$GIT_PASSWORD@gitee.com/$GITEE_ACCOUNT/$APP_NAME.git --tags --ipv4'
                    }
            
                  sh 'docker tag  $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:SNAPSHOT-$BRANCH_NAME-$TAG_NAME $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:$TAG_NAME '
                  sh 'docker push  $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:$TAG_NAME '
               }
           }
        }
 
       stage('deploy to production') {
       
          steps {
           container ('maven') {
   //         input(id: 'deploy-to-production', message: 'deploy to production?')
  //           sh 'kubectl delete -f k8s.yaml -n production'
             sh "sleep 10"
             sh "cat deploy.yaml"
             sh 'kubectl apply -f deploy.yaml -n production'
          }
        }
     }

    }

}
