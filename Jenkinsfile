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
        // 初始化参数
        script {
          server = getServer()
        }
        // 在远程主机上删除项目文件
        sshCommand remote: server, command: 'rm -rf /root/lrtest-api'
      }
    }
    stage('远程部署') {
      steps {
        // 将项目部署到远程服务器
        sshPut remote: server, from: '/var/jenkins_home/workspace/lrtest-api', into: '/root'
      }
    }
    stage('重启服务') {
      steps {
        // 进入项目所在目录，修改文件可执行权限，执行run.sh文件
        sshCommand remote: server, command: 'cd /root/lrtest-api && chmod u+x run.sh && ./run.sh'
      }
    }
  }
}


// 定义一个方法，返回ssh连接所需的信息
def getServer() {
    def remote = [:]
    remote.name = "ssh"
    remote.host = "chdxia.com"
    remote.port = 22
    remote.allowAnyHosts = true

    // 这里不展示明文密码，所以在jenkins凭据里提取
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
