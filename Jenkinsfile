properties ([disableConcurrentBuilds()])
pipeline {
    agent {
        label 'master'
    }
 // triggers { pollSCM('* * * * *') }

  stages {

    stage ('stage 0 kill sql') {
      steps {
 echo "=============docker build mysql_base-init=============="
         sh 'docker ps -q -f name=mysql-base && docker kill mysql-base || echo "Ęîíňĺéíĺđ mysql-base íĺ íŕéäĺí čëč íĺ çŕďóůĺí." '
      }  
    }

     stage ('stage 0 delete sql') {
      steps {
 echo "=============docker build mysql_base-init=============="
         sh 'docker ps -a -q -f name=mysql-base && docker rm mysql-base || echo "Ęîíňĺéíĺđ mysql-base íĺ íŕéäĺí čëč íĺ çŕďóůĺí."'
      }  
    }
 //    stage ('stage 0 delete image sql ') {
//      steps {
// echo "=============docker build mysql_base-init=============="
 //        sh 'docker rmi  mysql_base-init:latest'
 //     }  
 //   }
    stage ('stage 1 build mysql_base-init') {
      steps {
 echo "=============docker build mysql_base-init=============="
         sh 'docker build -t mysql_base-init:latest  mysql/.'
      }  
    }
  stage ('stage 1.2 run mysql_base-init') {
      steps {
 echo "=============docker run mysql_base-init=============="
        sh 'docker run -d --name mysql-base -p 3306:3306 mysql_base-init '
      }  
    }
    stage ('stage 2.1 docker build test1') {
      steps {
 echo "=============build python image python-pars-osnova=============="
         sh 'docker build -t python-pars-osnova:latest python/.'
      }  
    }
    stage ('stage 2.2 docker run test1') {
      steps {
        script {
              echo "=============docker run image python-pars-osnova=============="
               def containerId = sh(script: 'docker run --name python-first-pars1 --rm  python-pars-osnova:latest', returnStatus: true).trim()
               
                 waitUntil {
                  def status = sh(script: "docker inspect -f '{{.State.Status}}' ${containerId}", returnStatus: true).trim()
                  return status == 'exited'
                 }
       }
      }  
     }

stage ('stage 3 docker build') {
      steps {
 echo "=============build python image python-pars-izm=============="
         sh 'docker build -t python-pars-izm:latest python2/.'
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
