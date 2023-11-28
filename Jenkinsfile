properties ([disableConcurrentBuilds()])
pipeline {
    agent {
        label 'master'
    }
 // triggers { pollSCM('* * * * *') }

  stages {
  
/*    stage ('stage 0 kill sql') {
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
    */
     //    stage ('stage 0 delete image sql ') {
//      steps {
// echo "=============docker build mysql_base-init=============="
 //        sh 'docker rmi  mysql_base-init:latest'
 //     }  
 //   }
    stage ('stage 1 build mysql_base-init') {
     steps {
                script {
                    echo "===============pipe number: ${BUILD_NUMBER}================"
                    // Проверяем, запущен ли контейнер
                    def isContainerRunning = sh(script: 'docker ps -q -f name=mysql-base', returnStatus: true)
                    if (isContainerRunning != 0) {
                        // Контейнер не запущен, выполняем сборку Docker-образа
                        echo "=============docker build mysql_base-init=============="
                        sh 'docker build -t 127.0.0.1:8082/mysql_base-init  mysql/.'
                    } else {
                        // Контейнер уже запущен, пропускаем шаг сборки
                        echo "Container 'mysql-base' is already running. Skipping build."
                    }
                } 
     }
    }
  stage ('stage 1.2 run mysql_base-init') {
  //    dependsOn 'stage 1 build mysql_base-init' // Зависимость от этапа сборки
    steps {
                script {
                    // Проверяем, запущен ли контейнер
                    def isContainerRunning = sh(script: 'docker ps -q -f name=mysql-base', returnStatus: true)
                    if (isContainerRunning != 0) {
                        // Контейнер не запущен, выполняем запуск
                        echo "=============docker run mysql_base-init=============="
                        sh 'docker run -d --name mysql-base -p 3306:3306 127.0.0.1:8082/mysql_base-init '
                    } else {
                        // Контейнер уже запущен, пропускаем шаг запуска
                        echo "Container 'mysql-base' is already running. Skipping run."
                    }
                } 
        }
    } 
   stage('Wait up SQL') {
    steps {
         script {
                    // Проверяем, запущен ли контейнер
                    def isContainerRunning = sh(script: 'docker ps -q -f name=mysql-base', returnStatus: true)
                    if (!isContainerRunning) {
                        // Контейнер не запущен, выполняем запуск
                        echo "=============docker run mysql_base-init=============="
                         sleep time: 20, unit: 'SECONDS'
                    } else {
                        // Контейнер уже запущен, пропускаем шаг запуска
                        echo "Container 'mysql-base' is already running. Skipping waiting."
                    }
                }
       
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
        echo "=============docker run image python-pars-osnova=============="
        sh 'docker run --name python-first-pars4 --rm  python-pars-osnova:latest'  
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
        script {
            // Запуск докер-контейнера и захват вывода
            def containerOutput = sh(script: 'docker run --rm python-pars-izm:latest', returnStdout: true).trim()

            // Отправка сообщения в Telegram
            def TELEGRAM_BOT_TOKEN = '6950234094:AAHXDBrECclmKvYvaQhRTVG7aPWGPbKjkG8'
            def TELEGRAM_CHAT_ID = '-1002094674672'
            def MESSAGE_TEXT = "Docker Container Output:\n${containerOutput} in pipe: ${BUILD_NUMBER}"

            // Использование curl для отправки сообщения в Telegram
            sh "curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage -d text='${MESSAGE_TEXT}' -d chat_id=${TELEGRAM_CHAT_ID}"
        }
    } 
    }


    
  }
 
}
