pipeline {
  agent {label 'master'}
  options {
    skipStagesAfterUnstable()
    timeout(time: 1, unit: 'HOURS') 
  }
  environment {def server = ''}
  stages {
    stage('清理文件') {
      steps {
        script {
          server = getServer()
        }
        sshCommand remote: server, command: "rm -rf /root/lrtest-api"
      }
    }
    stage('远程部署') {
      steps {
        sshPut remote: server, from: "/var/jenkins_home/workspace/lrtest-api", into: "/root"
      }
    }
    stage('重启服务') {
      steps {
        sshCommand remote: server, command: "cd /root/lrtest-api && chmod u+x run.sh && ./run.sh"
      }
    }
  }
}


def getServer() {
    def remote = [:]
    remote.name = "ssh"
    remote.host = "ssh.chdxia.com"
    remote.port = 22
    remote.allowAnyHosts = true

    withCredentials([usernamePassword(
        credentialsId: "a477bfd8-880b-4d82-ae37-eecaa6e0133d",
        usernameVariable: "username",
        passwordVariable: "password"
    )]) {
        remote.user = "${username}"
        remote.password = "${password}"
    }
    return remote
}
