pipeline {
  agent {
    label 'master'
  }
  options {
    skipStagesAfterUnstable()
    timeout(time: 1, unit: 'HOURS') 
  }
  stages {
    stage('clone代码') {
      sh 'rm -rf /var/jenkins_home/workspace/lrtest-api/*'
      git branch: 'dev', credentialsId: '0b3a8b2d-b1fc-4935-89ec-516e8dd18b58', url: 'git@github.com:chdxia/lrtest-api.git'
    }
  }
}


def getServer() {
    def remote = [:]
    remote.name = "server"
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
