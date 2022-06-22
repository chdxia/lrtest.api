pipeline {
  agent {label 'master'}
  options {
    skipStagesAfterUnstable()
    timeout(time: 1, unit: 'HOURS') 
  }
  environment {def server = ''}
  stages {
    stage('init_ssh') {
      steps {
        script {
          server = getServer()
        }
      }
    }
    stage('停止服务') {
      steps {
        sshCommand remote: server, command: "pkill gunicorn && rm -rf /root/lrtest-api/*"
      }
    }
    stage('清理文件') {
      steps {
        sshCommand remote: server, command: "rm -rf /root/lrtest-api/*"
      }
    }
    stage('部署文件') {
      steps {
        sshPut remote: server, from: '', into: '/root/lrtest-api'
      }
    }
    stage('启动服务') {
      steps {
        sshCommand remote: server, command: "cd /root/lrtest-api && pipenv install && pipenv run gunicorn app.main:app"
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
        credentialsId: 'a477bfd8-880b-4d82-ae37-eecaa6e0133d',
        usernameVariable: 'UserName',
        passwordVariable: 'Password'
    )]) {
        remote.user = "${UserName}"
        remote.password = "${Password}"
    }
    return remote
}
