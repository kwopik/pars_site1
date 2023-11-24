properties ([disableConcurrentBuilds()])
pipeline {
    agent {
        label 'master'
    }
 // triggers { pollSCM('* * * * *') }

  stages {

    
    stage ('stage 1') {
      steps {
 echo "=============check and delete old build_app1=============="
        
      }  
    }
  stage ('stage 2') {
      steps {
 echo "=============check and delete old build_app2=============="
        
      }  
    }
stage ('stage 3 docker build') {
      steps {
 echo "=============build python image=============="
         sh 'docker build -t python-pars-izm:latest  python/.'
      }  
    }



    
  }
 
}
