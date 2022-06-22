pipeline {
  agent {label 'master'}
  options {
    skipStagesAfterUnstable()
    timeout(time: 1, unit: 'HOURS') 
  }
  environment {def server = ''}
  stages {
    stage('init_server') {
      steps {
        script {
          server = getServer()
        }
      }
    }
    stage('停止服务') {
      steps {
        script {
          sshCommand remote: server, command: "sudo wd"
        }
      }
    }
  }
}


def getServer() {
    def remote = [:]
    remote.name = "root"
    remote.host = "ssh.chdxia.com"
    remote.port = "22"
    remote.allowAnyHosts = true

    withCredentials([usernamePassword(
        credentialsId: 'a477bfd8-880b-4d82-ae37-eecaa6e0133d',
        usernameVariable: 'userName',
        passwordVariable: 'password'
    )]) {
        remote.user = "${userName}"
        remote.password = "${password}"
    }
    return remote
}
