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
 echo "=============docker run image=============="
      script {
                    def output = sh(script: 'docker run --rm -it python-pars-izm:latest', returnStdout: true).trim()
                    echo "Output from container: $output"
      }
      }  
    }


    
  }
 
}
