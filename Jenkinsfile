properties ([disableConcurrentBuilds()])
pipeline {
    agent {
        label 'master'
    }
 // triggers { pollSCM('* * * * *') }

  stages {

    
    stage ('stage 1') {
      steps {
 echo "=============docker build mysql_base-init=============="
         sh 'docker build -t mysql_base-init:latest  mysql/.'
      }  
    }
  stage ('stage 1.2 ') {
      steps {
 echo "=============docker run mysql_base-init=============="
        sh 'docker run -d --name mysql-base -p 3306:3306 mysql_base-init '
      }  
    }
    stage ('stage 2.1 docker build test1') {
      steps {
 echo "=============build python image python-pars-osnova=============="
         sh 'docker build -t python-pars-osnova:latest  python/Dockerfile1 .'
      }  
    }
    stage ('stage 2.2 docker run test1') {
      steps {
 echo "=============docker run image python-pars-osnova=============="
     sh 'docker run --rm python-pars-osnova:latest'
      }  
    }

stage ('stage 3 docker build') {
      steps {
 echo "=============build python image python-pars-izm=============="
         sh 'docker build -t python-pars-izm:latest  python/Dockerfile2 .'
      }  
    }
 stage ('stage 3.1 docker run') {
      steps {
 echo "=============docker run image python-pars-izm=============="
     sh 'docker run --rm python-pars-izm:latest'
      }  
    }


    
  }
 
}
