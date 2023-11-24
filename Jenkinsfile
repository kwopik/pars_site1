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
 echo "=============build python image python-pars-izm=============="
         sh 'docker build -t python-pars-izm:latest  python/.'
      }  
    }
 stage ('stage docker run') {
      steps {
 echo "=============check and delete old build_app2=============="
        sh 'docker run -it --name python-pars-izm-run python-pars-izm:latest '
      }  
    }


    
  }
 
}
