pipeline {
  agent {
      node {
          label 'my-defined-label'
          customWorkspace 'F:\MsDP\DevOps\Jenkins'
      }
  }
    stage('Checkout external proj') {
        steps {
            git branch: 'master',
                url: 'https://github.com/grebeus/naukma.git'
        }
    }
}
