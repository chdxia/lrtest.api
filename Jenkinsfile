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
        sshCommand remote: server, command: "ls -a"
      }
    }
  }
}


def getServer() {
    def remote = [:]
    remote.name = "ssh"
    remote.host = "ssh.chdxia.com"
    remote.port = "22"
    remote.allowAnyHosts = true

    withCredentials([usernamePassword(
        credentialsId: 'a477bfd8-880b-4d82-ae37-eecaa6e0133d',
        usernameVariable: 'UserName',
        passwordVariable: 'Password'
    )]) {
        remote.user = "${UserName}"
        remote.password = "${Password}"
    }
    return remote
}
